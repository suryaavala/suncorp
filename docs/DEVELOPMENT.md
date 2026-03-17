# DEVELOPMENT.md — Operational Runbook

This document is the definitive guide for operating, observing, debugging, and tuning the **GenAI Policy Adjudicator** microservice. It is written for competent Python developers who may be new to this specific domain (LLMs, RAG pipelines, and this repository's architecture).

For a high-level overview, see [README.md](../README.md).

---

## 1. System Architecture & Data Flow

Every insurance claim follows a strict, four-stage pipeline from ingestion to decision.

```
┌──────────────┐     ┌───────────────────┐     ┌─────────────────┐     ┌──────────────┐
│  FastAPI      │────▶│  Two-Stage        │────▶│  LLM            │────▶│  MLflow       │
│  Ingestion    │     │  Retrieval        │     │  Orchestration  │     │  Telemetry    │
│  (src/api.py) │     │  (vector_store +  │     │  (adjudicator)  │     │  (mlruns/)    │
│               │     │   reranker)       │     │                 │     │              │
└──────────────┘     └───────────────────┘     └─────────────────┘     └──────────────┘
```

### Stage 1: Ingestion via FastAPI (`src/api.py`)

A JSON claim payload is submitted to `POST /adjudicate`. FastAPI validates the request body against the `ClaimRequest` Pydantic model, which enforces the presence of `claim_id`, `description`, `incident_date`, and `claim_type`. The validated dictionary is passed to the orchestrator.

### Stage 2: Two-Stage Retrieval

1.  **Dense Embedding Search:** The claim description is embedded using Google's `gemini-embedding-001` model. The resulting vector is used to query a local ChromaDB collection, retrieving the **top 10** most semantically similar policy chunks.
2.  **Cross-Encoder Re-ranking (`src/reranker.py`):** The 10 candidate chunks are re-scored by a `cross-encoder/ms-marco-MiniLM-L-6-v2` model. This model evaluates the (query, chunk) pair directly, producing a much more precise relevance score. The **top 2** chunks are selected as the final context.

### Stage 3: LLM Orchestration (`src/adjudicator.py`)

The top 2 policy chunks and the raw claim JSON are assembled into a prompt. The prompt is sent to `gemini-2.5-flash` via the Google GenAI SDK. The response is constrained to a structured JSON schema (`AdjudicationResult`) using Pydantic, forcing the model to return a `decision` (Approve/Deny/Escalate), `confidence_score`, `reasoning`, and `cited_policy_clause`.

### Stage 4: MLflow Telemetry

Every invocation is wrapped in an `mlflow.start_run()` context. The following are logged:
-   **Parameters:** `embedding_model`, `llm_model`, `temperature`, `claim_type`.
-   **Artifacts:** The raw prompt text (`prompt.txt`) and the structured JSON result (`result.json`).

All telemetry data is persisted to the local `mlflow.db` SQLite database and the `mlruns/` directory.

---

## 2. Accessing External UIs

The system exposes three local interfaces for inspection and debugging.

### FastAPI Swagger Docs — `http://localhost:8000/docs`

Once the server is running (`python run.py` or `make up`), navigate to this URL to access the interactive API documentation.

**How to use it:**
1.  Expand the `POST /adjudicate` endpoint.
2.  Click **"Try it out"**.
3.  Paste a claim JSON payload into the request body (copy one from `data/claim_1.json`).
4.  Click **"Execute"** to fire the claim into the pipeline and inspect the response directly in the browser.

The `GET /health` endpoint is also available for infrastructure monitoring.

### MLflow Tracking UI — `http://localhost:5000`

MLflow provides a web dashboard for reviewing experiment runs, comparing parameters, and inspecting logged artifacts.

**How to launch it:**
```bash
source .venv/bin/activate
mlflow ui --port 5000
```

Navigate to `http://localhost:5000` and select the **"Policy_Adjudication"** experiment. Each row in the table represents a single claim evaluation. Click on a run to see:
-   **Parameters:** The model versions and temperature used.
-   **Artifacts:** The full `prompt.txt` sent to Gemini and the structured `result.json` response.

### ChromaDB Storage — `./data/chroma_db/`

ChromaDB is running as an embedded SQLite database. The data file is located at `data/chroma_db/chroma.sqlite3`.

**To inspect the collection directly from a Python shell:**
```python
import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("policy_chunks")

# View all stored documents
print(collection.peek())

# Query by text
results = collection.query(query_texts=["water damage from burst pipe"], n_results=3)
print(results["documents"])
```

---

## 3. Common Issues & Debugging

### Gemini API `429 Resource Exhausted` or `503 Service Unavailable`

**Symptoms:** The `/adjudicate` endpoint returns HTTP 503 with `"LLM Provider Error"`.

**Resolution:**
1.  Verify your `.env` file contains a valid `GEMINI_API_KEY`:
    ```bash
    cat .env  # Should show GEMINI_API_KEY=your_key_here
    ```
2.  Check your quota in the [Google Cloud Console](https://console.cloud.google.com/apis/dashboard) under the Generative Language API.
3.  If rate-limited, wait 60 seconds and retry. The Gemini free tier has a per-minute request cap.

### ChromaDB SQLite Lock Errors During Concurrent Testing

**Symptoms:** `sqlite3.OperationalError: database is locked` when running parallel tests.

**Resolution:**
ChromaDB's embedded mode uses a single SQLite file and does not support concurrent write access. To resolve:
1.  Ensure only one process is accessing the database at a time.
2.  If using Docker, restart the container to release the lock:
    ```bash
    make down && make up
    ```
3.  For local development, kill any stale Python processes:
    ```bash
    pkill -f "uvicorn"
    ```

### RAGAS Evaluation Pipeline Failing

**Symptoms:** `tests/eval_ragas.py` assertions fail unexpectedly (e.g., `Expected Approve, got Deny`).

**Resolution:**
1.  Verify the synthetic ground truth data in `data/eval_batch/` has not drifted from the current policy document at `data/policy.md`.
2.  Re-generate the mock data to ensure consistency:
    ```bash
    python -c "from src.mock_data import generate_mock_data; generate_mock_data()"
    ```
3.  Re-populate the vector store:
    ```bash
    python -c "from src.vector_store import populate_vector_store; populate_vector_store()"
    ```
4.  Re-run the evaluation:
    ```bash
    PYTHONPATH=$(pwd) pytest tests/eval_ragas.py -v
    ```

### Cross-Encoder Model Download Failures

**Symptoms:** `OSError` or `ConnectionError` when importing `src.reranker`.

**Resolution:**
The `cross-encoder/ms-marco-MiniLM-L-6-v2` model is downloaded from Hugging Face on first use. Ensure you have internet access. To pre-download:
```bash
python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"
```

---

## 4. Tuning & Prompts

### Modifying the AI's Behavior

The system prompt that governs every adjudication decision is defined as a string literal in [`src/adjudicator.py`](../src/adjudicator.py), inside the `evaluate_claim_from_dict` function (around line 75). The prompt is constructed using Python string concatenation:

```python
prompt = (
    "You are an expert insurance claims adjudicator. "
    "Given the following insurance policy excerpts and a claim description, "
    "determine whether the claim should be Approved, Denied, or Escalated.\n"
    f"\nPolicy Context:\n{policy_context}"
    f"\nClaim Data:\n{json.dumps(claim_data, indent=2)}"
    "\n\nEvaluate the claim accurately based only on the policy context provided. "
    "If you do not have enough specific information, Escalate. "
    "Provide reasoning and cite the specific policy clause that supports your decision."
)
```

To change the AI's behavior (e.g., make it more conservative, add new instructions), edit these string lines directly.

### Configurable Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(required)* | Your Google GenAI API key. |
| `EMBEDDING_MODEL` | `gemini-embedding-001` | The model used for dense vector embeddings. |
| `LLM_MODEL` | `gemini-2.5-flash` | The model used for claim adjudication reasoning. |
| `TEMPERATURE` | `0.0` | Controls randomness. `0.0` = deterministic. Increase for more creative responses. |

### Human-in-the-Loop (HITL) Threshold

The `CONFIDENCE_THRESHOLD = 0.85` is the business-critical variable that controls the escalation rate. It is enforced in the evaluation notebook (`notebooks/evaluation_dashboard.ipynb`).

-   **Raising the threshold** (e.g., to `0.95`): More claims are escalated to human adjusters. This increases operational costs but reduces the risk of automated errors.
-   **Lowering the threshold** (e.g., to `0.70`): Fewer claims are escalated. This reduces human workload but increases the chance that borderline claims are decided by the AI without human oversight.

The optimal threshold should be calibrated against historical claim data and the organization's risk appetite.
