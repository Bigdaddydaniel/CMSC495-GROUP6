# CMSC 495 Group 6 - Customer Service Platform Alpha

This repository contains the Unit 5 Alpha release for Group 6's AI-powered customer service platform.

## Team roles
- **Ethan Scampone - Lead Architect:** architecture diagrams, module boundaries, capacity assumptions, and architecture documentation.
- **Tanvi Gupta - Interface Designer:** API specifications, request/response schemas, validation, and interface documentation.
- **Daniel Sandoval - Integration Lead:** AI workflow, integration, human handoff, failure recovery, and feedback workflow.

## What the Alpha demonstrates
The Alpha is a small integrated MVP with:
- a FastAPI customer chat endpoint;
- a grounded AI retrieval component using TF-IDF similarity against approved knowledge;
- automatic human handoff when the answer is uncertain or the request requires staff action;
- conversation history;
- feedback capture;
- support ticket creation;
- automated tests; and
- a GitHub Actions CI workflow.

This prototype intentionally uses local/in-memory components so the team can prove the core workflow before production infrastructure is added.

## Run locally
1. Create a virtual environment: `python -m venv .venv`
2. Activate the environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Start the API: `uvicorn app.main:app --reload`
5. Open `http://127.0.0.1:8000` for the Alpha landing page.
6. Open `http://127.0.0.1:8000/docs` to test the API.

## Run tests
`pytest -q`

## Core endpoints
- `GET /health` - basic release health check
- `POST /chat` - submit a customer question
- `GET /conversations/{conversation_id}` - retrieve conversation history
- `POST /feedback` - record customer feedback
- `GET /tickets` - view tickets created by the Alpha handoff flow

## Known technical debt
- In-memory storage is used instead of PostgreSQL.
- Authentication and role-based authorization are not enabled in this Alpha.
- The local retrieval component stands in for the planned production model/RAG adapter.
- A production queue/outbox, monitoring, secrets management, and load testing remain future work.
- The earlier 10,000-concurrent-user architecture target has not been validated by this Alpha.

These items are documented intentionally and should not be interpreted as production-ready features.
