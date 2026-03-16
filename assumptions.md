# Assumptions & Simplifications (For Local Laptop Execution)

* Compute Offloading: Running a 70B parameter model locally will crash a standard laptop. We will use the Google GenAI SDK (Gemini 3.1 Pro/Flash) via API for all heavy reasoning and embeddings.

* Memory-Efficient Storage: We will bypass heavy databases (like Neo4j or Postgres with pgvector) and use chromadb. It runs locally, stores vectors in a lightweight SQLite file, and requires negligible RAM.

* Synthetic Data: Rather than setting up complex data pipelines, we will use a Python script to generate a synthetic Markdown policy document and JSON claim files.

* Framework Minimalism: We will avoid bloated frameworks like LangChain. Writing raw API calls and orchestration logic directly demonstrates "strong Python programming skills" and proves you understand the underlying mechanics of the pipeline.