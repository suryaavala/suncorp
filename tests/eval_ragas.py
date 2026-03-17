import json
from google import genai
from src.adjudicator import evaluate_claim_from_dict


def test_eval_ragas():
    """Evaluates the adjudicator using an LLM-as-a-judge approach.

    Runs the adjudicator and uses Gemini to verify whether the cited
    policy clause logically supports the system's decision.
    """
    # 1. Load the claim data
    with open("data/claim_1.json", "r") as f:
        claim_data = json.load(f)

    result = evaluate_claim_from_dict(claim_data)

    # 2. Assert basic ground truths based on our synthetic definitions
    assert result.decision == "Approve", f"Expected Approve, got {result.decision}"
    assert (
        result.confidence_score > 0.8
    ), f"Expected high confidence, got {result.confidence_score}"

    # 3. Use an LLM to evaluate if the cited policy clause makes sense for the claim
    prompt = f"""You are a strict evaluation judge.
    A user submitted this claim: {claim_data['description']}
    The automated system cited this clause to approve it: {result.cited_policy_clause}

    Does the cited clause explicitly cover the event described in the claim? Reply ONLY with 'YES' or 'NO'.
    """

    ai_client = genai.Client()
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt, config={"temperature": 0.0}
    )

    judge_verdict = response.text.strip().upper()
    assert (
        "YES" in judge_verdict
    ), f"LLM Judge rejected the system's citation. Found: {judge_verdict}"
