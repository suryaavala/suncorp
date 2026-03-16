import src.mock_data as mock_data
import src.vector_store as vector_store
from src.adjudicator import evaluate_claim

def main():
    print("--- 1. Generating Mock Data...")
    mock_data.generate_mock_data()
    
    print("\n--- 2. Populating Vector Store...")
    vector_store.populate_vector_store()
    
    print("\n--- 3. Evaluating Claim 1 (Clear-cut Approve)...")
    res_1 = evaluate_claim("data/claim_1.json")
    print(res_1.model_dump_json(indent=2))
    
    print("\n--- 4. Evaluating Claim 2 (Ambiguous Escalate)...")
    res_2 = evaluate_claim("data/claim_2.json")
    print(res_2.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
