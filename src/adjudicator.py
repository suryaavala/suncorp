import json
from enum import Enum
from pydantic import BaseModel, Field
import mlflow
import json
import os
from google import genai
from src.vector_store import ChromaVectorStore
from src.reranker import rerank_chunks

# Define Data Models
class Decision(str, Enum):
    APPROVE = "Approve"
    DENY = "Deny"
    ESCALATE = "Escalate"

class AdjudicationResult(BaseModel):
    decision: Decision
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    cited_policy_clause: str

def evaluate_claim_from_dict(claim_data: dict) -> AdjudicationResult:
    """Evaluates an insurance claim from a dictionary based on the policy manual, tracked via MLflow."""
    mlflow.set_experiment("Policy_Adjudication")
    
    with mlflow.start_run():
        claim_description = claim_data.get("description", "")
        
        ai_client = genai.Client()
        embedding_model = 'gemini-embedding-001'
        llm_model = 'gemini-2.5-flash'
        temperature = 0.0

        # Log parameters
        mlflow.log_params({
            "embedding_model": embedding_model,
            "llm_model": llm_model,
            "temperature": temperature,
            "claim_type": claim_data.get("claim_type", "unknown")
        })

        # 2. Query the vector store
        query_embedding_response = ai_client.models.embed_content(
            model=embedding_model,
            contents=claim_description
        )
        query_embedding = query_embedding_response.embeddings[0].values

        # Retrieve broader context (top 10) from vector store
        vector_store = ChromaVectorStore()
        retrieved_chunks_top10 = vector_store.query(
            query_embeddings=[query_embedding],
            n_results=10
        )
        
        # Re-rank to get the top 2 most relevant chunks
        top_2_chunks = rerank_chunks(query=claim_description, chunks=retrieved_chunks_top10, top_k=2)
        
        policy_context = "\n\n---\n\n".join(top_2_chunks)

        # 3. Construct prompt
        prompt = f"""You are an expert insurance claims adjudicator. Given the following insurance policy excerpts and a claim description, determine whether the claim should be Approved, Denied, or Escalated.
        
Policy Context:
{policy_context}

Claim Data:
{json.dumps(claim_data, indent=2)}

Evaluate the claim accurately based only on the policy context provided. If you do not have enough specific information, Escalate. Provide reasoning and cite the specific policy clause that supports your decision.
"""
        
        # Save prompt to artifact
        if not os.path.exists("mlruns_artifacts"):
            os.makedirs("mlruns_artifacts")
        with open("mlruns_artifacts/prompt.txt", "w") as f:
            f.write(prompt)
        mlflow.log_artifact("mlruns_artifacts/prompt.txt")

        # 4. Call Gemini with Pydantic schema
        response = ai_client.models.generate_content(
            model=llm_model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": AdjudicationResult,
                "temperature": temperature
            }
        )

        # Parse JSON back into our model
        result_dict = json.loads(response.text)
        
        # Save result to artifact
        with open("mlruns_artifacts/result.json", "w") as f:
            json.dump(result_dict, f, indent=2)
        mlflow.log_artifact("mlruns_artifacts/result.json")
        
        return AdjudicationResult(**result_dict)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        claim_path = sys.argv[1]
        with open(claim_path, 'r') as f:
            claim_data = json.load(f)
        res = evaluate_claim_from_dict(claim_data)
        print(res.model_dump_json(indent=2))
