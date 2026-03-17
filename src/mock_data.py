import os
import json


def generate_mock_data():
    """Generates synthetic insurance policy and claim files."""
    os.makedirs("data", exist_ok=True)

    # 1. Generate Policy Document
    policy_content = """# Suncorp Home Insurance Policy

## 1. Introduction
This policy outlines the terms and conditions of your Suncorp Home Insurance. Please read carefully to understand what is covered and what is excluded.

## 2. Water Damage Cover
We cover loss or damage caused by sudden and accidental escape of water from fixed water pipes, appliances, or tanks inside your home.

### 2.1 Exclusions for Water Damage
- Damage resulting from gradual wear and tear or gradual leakage over time.
- Damage caused by lack of maintenance, such as failing to repair known plumbing issues.
- Water damage from flooding (requires separate Flood Cover).

## 3. Roof Leaks
We cover loss or damage to your home and contents caused by a leaking roof, provided the leak is the direct result of an insured event such as a severe storm, hail, or fallen tree.

### 3.1 Exclusions for Roof Leaks
- Damage caused by a roof that has not been properly maintained or is in a state of disrepair prior to the incident.
- Gradual deterioration of roofing materials.

## 4. Deductibles and Excess
- A standard excess of $500 applies to all claims unless otherwise specified below.
- Earthquakes and natural disasters carry an additional $500 excess.
"""
    with open("data/policy.md", "w") as f:
        f.write(policy_content)

    # 2. Generate Claim 1 (Clear-cut Appproved Claim)
    claim_1 = {
        "claim_id": "C-1001",
        "description": "During a severe thunderstorm yesterday, a large tree branch fell onto my roof, causing a sudden and significant leak. Water poured into the living room, damaging the ceiling and floor.",
        "incident_date": "2023-10-15",
        "claim_type": "Roof Leak and Water Damage",
    }
    with open("data/claim_1.json", "w") as f:
        json.dump(claim_1, f, indent=4)

    # 3. Generate Claim 2 (Ambiguous/Escalated Claim)
    claim_2 = {
        "claim_id": "C-1002",
        "description": "I noticed some water damage on the bathroom ceiling. Looks like the pipes might have been slowly dripping for a few months, and now the drywall is ruined. I need it fixed.",
        "incident_date": "Uncertain, noticed 2023-11-01",
        "claim_type": "Water Damage",
    }
    with open("data/claim_2.json", "w") as f:
        json.dump(claim_2, f, indent=4)

    print("Mock data generated successfully in data/")


if __name__ == "__main__":
    generate_mock_data()
