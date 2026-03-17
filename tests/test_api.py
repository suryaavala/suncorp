from unittest.mock import patch
from fastapi.testclient import TestClient
from src.api import app
from src.adjudicator import AdjudicationResult, Decision

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_adjudicate_endpoint() -> None:
    """Tests the /adjudicate endpoint contract by mocking the adjudicator pipeline."""
    payload = {
        "claim_id": "C-TEST",
        "description": "A tree fell on my roof during a storm, causing water damage.",
        "incident_date": "2023-10-15",
        "claim_type": "Roof Damage",
    }
    mock_result = AdjudicationResult(
        decision=Decision.APPROVE,
        confidence_score=0.95,
        reasoning="Storm-induced roof damage is an insured event under Section 3.",
        cited_policy_clause="Section 3: Roof Leaks – covers damage from fallen trees during storms.",
    )

    with patch("src.api.evaluate_claim_from_dict", return_value=mock_result):
        response = client.post("/adjudicate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "decision" in data
    assert "confidence_score" in data
    assert "reasoning" in data
    assert "cited_policy_clause" in data
