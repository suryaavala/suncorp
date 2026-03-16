# GenAI Policy Adjudicator: Automated Claims Triage POC

## 1. Background and Goal
Insurance claims processing often suffers from high manual overhead during the initial triage phase, where adjusters must cross-reference unstructured claim reports against dense Product Disclosure Statements (PDS). 

**The Goal:** Build a lightweight, agentic Retrieval-Augmented Generation (RAG) system that automatically ingests a claim, retrieves the relevant policy clauses, and outputs a structured adjudication decision (Approve/Deny/Escalate). This prototype demonstrates how to reduce cycle times while maintaining strict explainability guardrails.

## 2. Project Outcomes
* **Automated Reasoning:** The system successfully evaluates claims against synthetic policy rules with high accuracy.
* **Explainability Trace:** Every AI decision outputs a JSON payload containing the exact policy text cited, ensuring the reasoning is fully auditable.
* **Confidence Guardrails:** The model returns a confidence score. Claims falling into "gray areas" are automatically flagged for Human-in-the-Loop (HITL) review, preventing autonomous hallucinations on complex claims.
* **Future Improvements:** To transition this from a POC to "scalable, production-grade solutions embedded in core systems", the local `chromadb` would be migrated to Databricks Vector Search, and the execution logic would be wrapped in a serverless API (e.g., FastAPI on Cloud Run).

## 3. Structure and Implementation
The codebase is designed for extreme modularity and local efficiency, avoiding heavy frameworks to maintain full control over the AI pipeline.
* `requirements.txt`: Minimal dependencies for rapid local execution.
* `src/mock_data.py`: Generates synthetic PDS markdown files and claim JSONs.
* `src/vector_store.py`: Handles document chunking and local embedding storage using `chromadb`.
* `src/adjudicator.py`: The core orchestration script that executes the RAG retrieval and formats the prompt for the LLM.
* `run.py`: The entry point that executes the end-to-end pipeline.