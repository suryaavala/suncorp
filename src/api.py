from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.genai.errors import APIError

from src.adjudicator import evaluate_claim_from_dict, AdjudicationResult

app = FastAPI(title="GenAI Policy Adjudicator API", version="1.0.0")


class ClaimRequest(BaseModel):
    claim_id: str
    description: str
    incident_date: str
    claim_type: str


@app.post("/adjudicate", response_model=AdjudicationResult)
async def adjudicate_claim(claim: ClaimRequest) -> AdjudicationResult:
    """Evaluates an insurance claim and returns the adjudication decision.

    Args:
        claim (ClaimRequest): The incoming claim data payload.

    Returns:
        AdjudicationResult: The computed AI decision and policy citation.

    Raises:
        HTTPException: If the LLM provider fails or a general processing error occurs.
    """
    try:
        claim_dict = claim.model_dump()
        result = evaluate_claim_from_dict(claim_dict)
        return result
    except APIError as e:
        # Handle specific GenAI API timeouts/errors
        raise HTTPException(status_code=503, detail=f"LLM Provider Error: {str(e)}")
    except Exception as e:
        # Generic catch-all for local processing or dict parsing errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/health")
async def health_check() -> dict:
    """Infrastructure monitoring endpoint.

    Returns:
        dict: A simple status dictionary confirming the API is active.
    """
    return {"status": "ok"}
