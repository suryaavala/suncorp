import pytest
from unittest.mock import patch, MagicMock
from google.genai.errors import APIError
from src.adjudicator import evaluate_claim_from_dict


def test_api_timeout_handling():
    """Verifies the adjudicator handles GenAI API timeouts gracefully.
    
    Mocks the Google GenAI Client and the reranker to force a timeout Exception
    and asserts that the pipeline bubbles up the error correctly.
    """
    claim_payload = {
        "claim_id": "C-ERR",
        "description": "Valid claim description",
        "incident_date": "2023-01-01",
        "claim_type": "Fire",
    }

    with patch("src.adjudicator.genai.Client") as mock_client, patch(
        "src.adjudicator.rerank_chunks"
    ) as mock_rerank_chunks:
        mock_instance = mock_client.return_value

        mock_instance.models.embed_content.side_effect = Exception("API Timeout")

        with pytest.raises(Exception, match="API Timeout"):
            evaluate_claim_from_dict(claim_payload)
