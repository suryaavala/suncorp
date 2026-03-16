import json
from enum import Enum
from pydantic import BaseModel, Field
import chromadb
from google import genai

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

def get_chroma_collection():
    chroma_client = chromadb.PersistentClient(path="data/chroma_db")
    return chroma_client.get_collection(name="policy_chunks")

def evaluate_claim(claim_path: str) -> AdjudicationResult:
    """Evaluates an insurance claim from a JSON file based on the policy manual."""
    with open(claim_path, 'r') as f:
        claim_data = json.load(f)
    return evaluate_claim_from_dict(claim_data)

def evaluate_claim_from_dict(claim_data: dict) -> AdjudicationResult:
    """Evaluates an insurance claim from a dictionary based on the policy manual."""
    claim_description = claim_data.get("description", "")
    
    ai_client = genai.Client()

    # 2. Query the vector store
    query_embedding_response = ai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=claim_description
    )
    query_embedding = query_embedding_response.embeddings[0].values

    # Retrieve from chroma
    collection = get_chroma_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    
    # Extract the text chunks
    retrieved_chunks = results['documents'][0]
    policy_context = "\n\n---\n\n".join(retrieved_chunks)

    # 3. Construct prompt
    prompt = f"""You are an expert insurance claims adjudicator. Given the following insurance policy excerpts and a claim description, determine whether the claim should be Approved, Denied, or Escalated.
    
Policy Context:
{policy_context}

Claim Data:
{json.dumps(claim_data, indent=2)}

Evaluate the claim accurately based only on the policy context provided. If you do not have enough specific information, Escalate. Provide reasoning and cite the specific policy clause that supports your decision.
"""

    # 4. Call Gemini with Pydantic schema
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": AdjudicationResult,
            "temperature": 0.0
        }
    )

    # Parse JSON back into our model
    result_dict = json.loads(response.text)
    return AdjudicationResult(**result_dict)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        res = evaluate_claim(sys.argv[1])
        print(res.model_dump_json(indent=2))
