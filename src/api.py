from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

from src.adjudicator import evaluate_claim_from_dict, AdjudicationResult

app = FastAPI(title="GenAI Policy Adjudicator API", version="1.0.0")

class ClaimRequest(BaseModel):
    claim_id: str
    description: str
    incident_date: str
    claim_type: str

@app.post("/adjudicate", response_model=AdjudicationResult)
async def adjudicate_claim(claim: ClaimRequest):
    """
    Evaluates an insurance claim and returns the adjudication decision.
    """
    try:
        claim_dict = claim.model_dump()
        result = evaluate_claim_from_dict(claim_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Infrastructure monitoring endpoint.
    """
    return {"status": "ok"}
