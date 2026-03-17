import pytest
from unittest.mock import patch, MagicMock
from google.genai.errors import APIError
from src.adjudicator import evaluate_claim_from_dict


def test_api_timeout_handling():
    """
    Mocks the Google GenAI API to simulate a timeout/error and
    verifies the adjudicator handles it (either by raising a specific error or failing fast).
    """
    claim_payload = {
        "claim_id": "C-ERR",
        "description": "Valid claim description",
        "incident_date": "2023-01-01",
        "claim_type": "Fire",
    }

    # We mock the entire `genai.Client` to raise an Exception when embedding is called,
    # and we also mock `rerank_chunks` just in case the pipeline gets that far.
    with patch("src.adjudicator.genai.Client") as mock_client, patch(
        "src.adjudicator.rerank_chunks"
    ) as mock_rerank_chunks:
        mock_instance = mock_client.return_value

        # Simulate a 504 Gateway Timeout or similar API Error when embeddings are requested
        mock_instance.models.embed_content.side_effect = Exception("API Timeout")

        with pytest.raises(Exception, match="API Timeout"):
            evaluate_claim_from_dict(claim_payload)
