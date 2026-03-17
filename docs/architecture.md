# Architecture Documentation: Final

## Overview
The **GenAI Policy Adjudicator** is a robust, production-ready microservice built in Python. The system processes raw, unstructured claim dictionaries, searches a Vector DB for relevant insurance policy clauses, and orchestrates an LLM to automatically decision the claim.

## Architecture Diagram
```mermaid
flowchart TD
    %% Define Styles
    classDef apiFill fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef logicFill fill:#cce5ff,stroke:#007bff,stroke-width:2px;
    classDef datastoreFill fill:#fff3cd,stroke:#ffc107,stroke-width:2px;
    classDef externalFill fill:#f8d7da,stroke:#dc3545,stroke-width:2px,stroke-dasharray: 5 5;

    %% Nodes
    User(["Client / Core System"])
    
    subgraph FastAPI Microservice
        API["POST /adjudicate\n(src/api.py)"]:::apiFill
        Pydantic["Pydantic Validator\n(ClaimRequest)"]:::apiFill
    end
    
    subgraph Execution & Tracking
        Adjudicator["Adjudication Engine\n(src/adjudicator.py)"]:::logicFill
        MLflow[("MLflow Tracking Server\n(mlruns/)")]:::datastoreFill
    end
    
    subgraph Vector Search Strategy
        VectorBase{"VectorStore (ABC)\n(src/vector_store.py)"}:::logicFill
        Chroma[("ChromaDB / SQLite\n(Local Storage)")]:::datastoreFill
    end

    %% External APIs
    GeminiLLM{{"Google Gemini SDK\n(gemini-2.5-flash)"}}:::externalFill
    GeminiEmbed{{"Google Gemini SDK\n(gemini-embedding-001)"}}:::externalFill

    %% Flow/Relationships
    User -->|"{claim_id, description, ...}"| API
    API -->|Validates Input| Pydantic
    Pydantic -->|Valid Dict| Adjudicator
    
    Adjudicator -->|"1. Embed Claim"| GeminiEmbed
    GeminiEmbed -->|"Vector [0.1, 0.4...]"| Adjudicator
    
    Adjudicator -->|"2. Query Configured Store"| VectorBase
    VectorBase -.->|Current Impl| Chroma
    Chroma -->|"3. Top 2 Policy Clauses"| Adjudicator
    
    Adjudicator -->|"4. Execute Prompt + JSON Schema"| GeminiLLM
    GeminiLLM -->|"5. AdjudicationResult object"| Adjudicator
    
    Adjudicator -->|"6. Log Trace & Metadata"| MLflow
    Adjudicator -->|"7. Return {decision, score}"| API
    API -->|HTTP 200| User
```

## Core Components
1. **API Layer (`src/api.py`)** -> Designed using FastApi to sit effectively behind enterprise Firewalls or load balancers.
2. **Instrumentation Layer (`src/adjudicator.py` + MLflow)** -> All claim evaluations, prompts, inference arguments, and model signatures are immutably tracked in MLflow for governance and continuous refinement. 
3. **Reasoning Layer (`src/adjudicator.py`)** -> An execution pipeline that takes chunks from a Vector DB and injects them alongside a Pydantic Schema model to enforce that the LLM (`gemini-2.5-flash`) only returns pure, structured JSON arrays containing the decision, confidence score, cited policy extraction string, and reasoning.
4. **Knowledge Store (`src/vector_store.py`)** -> Leverages Google's `gemini-embedding-001` to vectorize text logic. It uses the `VectorStore` Abstract Base Class, currently implementing the `ChromaVectorStore` concrete class for portability, but acts as a seam to swap in a scalable datastore (e.g. Databricks Vector Search or generic SQL via `pgvector`) in less than 20 lines of code.

## Cloud Target & Extension
* **Cloud Deployment:** This service evaluates perfectly inside a container. The `uvicorn` entry point can be effortlessly mounted to GCP Cloud Run or Azure Container Apps in a completely serverless manner.
* **Continuous Integration:** Using `FastAPI.testclient` allows the CI pipeline to perfectly simulate incoming application load without needing real compute loops, running on GitHub Linux VMs natively.

