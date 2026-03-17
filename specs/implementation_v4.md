# Antigravity V4 Implementation Plan: Containerization & Deployment

## Context
To transition this POC into a true "production-grade" artifact, we need to containerize the FastAPI microservice. This ensures environmental consistency and allows the application to be easily deployed to modern cloud infrastructure (like Kubernetes or AWS ECS/GCP Cloud Run). Given the local memory constraints, we will use lightweight base images and Docker Compose to orchestrate the service alongside a persistent volume for the Chroma vector database.

## Execution Rules for Antigravity Agent
* Stop and wait for user review after completing the checklist.
* Ensure the Dockerfile follows security and size best practices (e.g., using slim images, not running as root if possible).
* Keep the architecture memory-efficient so it can run smoothly on a local laptop.

---

### PR 7: Containerization & Reproducibility
**Branch:** `chore/docker-containerization`
**Goal:** Package the application using Docker and Docker Compose to demonstrate production readiness and reproducible environments.

- [ ] Create a `.dockerignore` file. Add `__pycache__`, `.venv`, `.git`, `*.sqlite3`, `notebooks/`, `tests/`, and local `chroma_db/` directories to prevent bloating the container image.
- [ ] Create a `Dockerfile` in the root directory:
    - Use `python:3.10-slim` as the base image.
    - Set the working directory to `/app`.
    - Copy `requirements.txt` and install dependencies using `pip install --no-cache-dir`.
    - Copy the `src/` directory and `run.py` into the container.
    - Expose port `8000`.
    - Set the entrypoint command to run the FastAPI server via Uvicorn: `CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]`.
- [ ] Create a `docker-compose.yml` file:
    - Define a service named `adjudicator-api`.
    - Build from the current directory context.
    - Map port `8000:8000` to the host.
    - Pass in environment variables (like `GEMINI_API_KEY`) from a local `.env` file.
    - Create a named Docker volume `chroma_data` and mount it to `/app/chroma_db` inside the container. This ensures that the vector embeddings are not lost every time the container restarts, saving API calls and time.
- [ ] Create a `Makefile` to simplify terminal commands for the engineering team. Include targets for:
    - `build`: Runs `docker-compose build`
    - `up`: Runs `docker-compose up -d`
    - `down`: Runs `docker-compose down`
    - `logs`: Runs `docker-compose logs -f`
- [ ] Update the `README.md` under a new "Deployment" section. Explain how to run the application using the new `Makefile` commands and explicitly state the assumption that the `GEMINI_API_KEY` must be provided in a `.env` file.