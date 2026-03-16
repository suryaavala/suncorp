# Antigravity Implementation Plan: GenAI Policy Adjudicator

## Context
We are building a minimal, memory-efficient RAG pipeline for insurance claims adjudication. The system must run on a local laptop using `chromadb` for vector storage and the Google GenAI API for embeddings and LLM generation. 

## Architectural Rules
* Do not use LangChain or LlamaIndex. Write raw, modular Python.
* Use `pydantic` to enforce structured JSON outputs from the LLM.
* Ensure all functions have Google-style docstrings and type hints.

## Task List
- [ ] **Task 1: Project Scaffolding**
  - Create the `src/` directory.
  - Install dependencies from `requirements.txt`.
- [ ] **Task 2: Data Generation (`src/mock_data.py`)**
  - Write a script that creates a `data/` folder.
  - Generate a file `data/policy.md` containing a synthetic, 500-word insurance policy with specific rules for water damage, roof leaks, and deductibles.
  - Generate a file `data/claim_1.json` representing a clear-cut approved claim.
  - Generate a file `data/claim_2.json` representing an ambiguous claim that should be escalated.
- [ ] **Task 3: Vector Store (`src/vector_store.py`)**
  - Initialize a local `chromadb` client.
  - Write a function to read `data/policy.md`, split it into chunks of 200 words, embed them using the Google GenAI embedding model, and store them in the Chroma collection.
- [ ] **Task 4: Adjudication Engine (`src/adjudicator.py`)**
  - Define a Pydantic model `AdjudicationResult` with fields: `decision` (Enum: Approve, Deny, Escalate), `confidence_score` (float), `reasoning` (string), and `cited_policy_clause` (string).
  - Write a function `evaluate_claim(claim_path: str)` that:
    1. Loads the claim JSON.
    2. Queries the vector store using the claim description to get the top 2 relevant policy chunks.
    3. Constructs a prompt containing the claim data and the retrieved policy chunks.
    4. Calls Gemini to generate the response strictly matching the Pydantic schema.
- [ ] **Task 5: Execution Pipeline (`run.py`)**
  - Write the main entry point that runs the data generation, populates the vector store, evaluates both claims, and pretty-prints the JSON results to the terminal.