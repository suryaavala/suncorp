# Antigravity V2 Implementation Plan: Enterprise Adjudicator

## Context
We are upgrading the GenAI Policy Adjudicator POC into a production-ready microservice. To simulate an enterprise environment and maintain strict version control, this upgrade will be executed in four distinct Pull Requests (PRs). 

## Execution Rules for Antigravity Agent
* Stop and wait for user review after completing the checklist for each PR.
* Do not proceed to the next PR until the user explicitly commands it.
* Maintain clean, modular Python architecture. Write Google-style docstrings for all new functions.

---

### PR 1: Core System Embedding (FastAPI Microservice)
**Branch:** `feature/fastapi-integration`
**Goal:** Wrap the local RAG script into a RESTful API service so core systems can interact with it.
- [ ] Install `fastapi` and `uvicorn` and add them to `requirements.txt`.
- [ ] Create `src/api.py`.
- [ ] Define Pydantic request models (`ClaimRequest`) and response models (`AdjudicationResponse`).
- [ ] Create a `POST /adjudicate` endpoint that accepts a JSON claim, calls the `evaluate_claim` function from `src/adjudicator.py`, and returns the structured decision.
- [ ] Create a `GET /health` endpoint for infrastructure monitoring.
- [ ] Update `run.py` to start the Uvicorn server instead of running a static script.

### PR 2: Cloud Migration Prep (MLflow Experiment Tracking)
**Branch:** `feature/mlflow-tracking`
**Goal:** Introduce experiment tracking to version prompts, models, and parameters, preparing for a Databricks environment.
- [ ] Install `mlflow` and add it to `requirements.txt`.
- [ ] Update `src/adjudicator.py` to initialize an MLflow run at the start of `evaluate_claim`.
- [ ] Log parameters during the run: LLM model name, temperature, and embedding model name.
- [ ] Log the generated prompt and the final `AdjudicationResult` dictionary as artifacts.
- [ ] Refactor `src/vector_store.py` to use an abstract base class, allowing the local `chromadb` to be easily swapped for Databricks Vector Search in the future.

### PR 3: Advanced Evaluation & Guardrails
**Branch:** `feature/evaluation-suite`
**Goal:** Implement automated testing to quantitatively measure hallucination rates and accuracy.
- [ ] Create a `tests/` directory.
- [ ] Write `tests/test_api.py` using `pytest` and `FastAPI.testclient` to verify the `/adjudicate` and `/health` endpoints return 200 OK.
- [ ] Create `tests/eval_ragas.py`. Write a lightweight "LLM-as-a-judge" function that takes the system's output, compares it against a known "ground truth" for `claim_1.json`, and asserts that the `cited_policy_clause` is correct.
- [ ] Mock the Google GenAI API response in a new test `tests/test_adjudicator.py` to ensure the system handles API timeouts gracefully.

### PR 4: Governance & CI/CD Automation
**Branch:** `chore/ci-cd-pipeline`
**Goal:** Establish the baseline for team enablement and best-practice frameworks by automating checks.
- [ ] Create `.github/workflows/ci.yml`.
- [ ] Configure a GitHub Actions workflow that triggers on every push to `main` and every Pull Request.
- [ ] Set the workflow to check out the code, set up Python 3.10, and install `requirements.txt`.
- [ ] Add a step in the workflow to run a linter (e.g., `flake8` or `ruff`) to enforce code quality.
- [ ] Add a step in the workflow to execute `pytest tests/` to ensure no PR breaks existing logic.