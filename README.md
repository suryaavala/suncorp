# GenAI Policy Adjudicator: V2 Enterprise Microservice

## 1. Background and Goal
Insurance claims processing often suffers from high manual overhead during the initial triage phase, where adjusters must cross-reference unstructured claim reports against dense Product Disclosure Statements (PDS). 

**The Goal:** Build an Enterprise-grade, lightweight, agentic Retrieval-Augmented Generation (RAG) microservice that automatically ingests a claim, retrieves the relevant policy clauses, and outputs a structured adjudication decision (Approve/Deny/Escalate). This prototype demonstrates how to reduce cycle times while maintaining strict explainability guardrails, testing suites, and experiment tracking APIs.

## 2. V2 Enterprise Features
* **FastAPI Microservice:** The core adjudication engine is wrapped in a RESTful API (`POST /adjudicate`) allowing seamless integration with core insurance systems.
* **MLflow Governance:** Every evaluation tracks model versions, parameters, and logs the raw LLM prompts and json results as artifacts for perfect auditability and experiment tracking.
* **LLM-as-a-Judge Evaluation:** Robust Pytest suite featuring quantitative LLM evaluation tools (`eval_ragas.py`) that strictly assert the agent's logic and citations against the raw claim data.
* **CI/CD Automation:** A GitHub Actions pipeline guarantees code quality and logic preservation across all future PRs.
* **Abstract Data Layer:** The vector store utilizes the Strategy Pattern, allowing the local `ChromaDB` logic to be hot-swapped for a Databricks Vector Search implementation in the future.

## 3. Structure and Implementation
The codebase is designed for extreme modularity and scalability.
* `requirements.txt`: Dependencies for the API, ML Tracking, and Testing framework.
* `.env`: (User created) Environment file for storing `GEMINI_API_KEY`.
* `src/api.py`: FastAPI endpoints for health monitoring and claim adjudication processing.
* `src/adjudicator.py`: The core orchestration script pulling vectors, executing Gemini with Pydantic structured schemas, and tracking metrics in MLflow.
* `src/vector_store.py`: Abstract Base Class for ChromaDB local storage of Gemini text embeddings.
* `src/mock_data.py`: Generates synthetic PDS markdown files and claim JSONs.
* `tests/`: Contains `pytest` files for API validation, LLM-as-a-judge quantitative validation, and mocking tools for timeout handling.
* `run.py`: The Uvicorn entry point that starts the local API server and initializes dummy data.

## 4. Execution
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .env # ensure GEMINI_API_KEY is exported
python run.py
```
After running the script, the Uvicorn server will host the API on port 8000. 
You can test the endpoint using `curl`:
```bash
curl -X POST http://localhost:8000/adjudicate \
     -H "Content-Type: application/json" \
     -d @data/claim_1.json
```