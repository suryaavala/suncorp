from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_adjudicate_endpoint() -> None:
    payload = {
        "claim_id": "C-TEST",
        "description": "A tree fell on my roof during a storm, causing water damage.",
        "incident_date": "2023-10-15",
        "claim_type": "Roof Damage",
    }
    response = client.post("/adjudicate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "decision" in data
    assert "confidence_score" in data
    assert "reasoning" in data
    assert "cited_policy_clause" in data
