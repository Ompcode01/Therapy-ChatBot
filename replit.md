# Therapy ChatBot for IGD & BDD Support

## Overview

An AI-powered mental health support system designed to provide empathetic
conversational assistance for individuals experiencing Internet Gaming Disorder
(IGD) and Body Dysmorphic Disorder (BDD).

This is the demo / scaffolding version of the project: the Streamlit frontend
renders a chat UI with placeholder responses, and the FastAPI backend plus the
PostgreSQL/pgvector data layer are stubbed in for future integration with
LLM providers (Gemini / Groq).

## Project Structure

```
.
├── frontend.py            # Streamlit UI (chat demo)
├── main.py                # FastAPI backend entry point (uvicorn launcher)
├── requirements.txt
├── .streamlit/config.toml # Streamlit server config (host/port for Replit)
└── app/
    ├── app.py             # FastAPI app instance
    ├── core/              # Security / config helpers (HMAC)
    ├── db/                # SQLAlchemy + pgvector models, engine, session
    ├── schemas/           # Pydantic schemas (public / internal)
    └── services/          # Business logic (symptom embeddings, etc.)
```

## Replit Environment Setup

- **Language:** Python 3.12
- **Frontend:** Streamlit, served on `0.0.0.0:5000` (port 5000 is the only port
  the Replit preview iframe proxies).
- **Workflow:** `Start application` runs
  `streamlit run frontend.py --server.address=0.0.0.0 --server.port=5000 --server.headless=true`.
- **Streamlit config (`.streamlit/config.toml`)** disables CORS / XSRF and
  binds to `0.0.0.0:5000` so the Replit proxy can reach it from any host.
- **Backend (FastAPI):** Skeleton only — no routes are registered yet and the
  Streamlit frontend does not call it, so no separate workflow is configured.
  When backend endpoints are added, run it on `localhost` and a port other
  than 5000 (e.g. 8000).
- **Database:** The SQLAlchemy engine reads `DATABASE_URL` from the environment
  and uses `pgvector` for 384-dim symptom embeddings. Provision a Postgres
  database (with the `vector` extension) and set `DATABASE_URL` before using
  any DB-backed code paths. `SECRET_KEY` is required by `app/core/security.py`
  for HMAC generation.

## Deployment

Configured for Replit Autoscale deployment running:

```
streamlit run frontend.py --server.address=0.0.0.0 --server.port=5000 --server.headless=true
```

## Pages

The Streamlit app is multipage (Streamlit auto-discovers files in `pages/`):

1. **💬 Therapy Chatbot** (`frontend.py`) — colorful chat UI that calls the
   Groq LLM. Uses `st.chat_input` and the system prompt in `system.md`. Sidebar
   shows the API-key status, a model picker, and a **Clear conversation** button.
2. **📊 Health Dashboard** (`pages/2_📊_Health_Dashboard.py`) — simulated
   wearable-device dashboard. Pick a watch, click **Connect**, and see SpO₂,
   blood pressure, heart rate, skin temperature, a derived **stress score
   (1–10)**, and a live trend chart. Supports **auto-refresh every 3s**.

## LLM Integration (Groq)

- The `groq` Python SDK is wrapped in `app/services/llm.py` (`generate_reply`).
- The system prompt lives in `system.md`.
- The default model is `llama-3.3-70b-versatile`; the sidebar lets the user
  choose between several Groq-hosted models.
- API key resolution order: explicit key passed in (sidebar override) →
  `GROQ_API_KEY` env var → `.env` file (loaded via `python-dotenv`).
  On Replit, store the key in **Secrets** as `GROQ_API_KEY`.
  See `.env.example` for the full list of supported variables.

## Recent Changes

- 2026-04-24: Initial Replit setup — installed Python deps, added
  `.streamlit/config.toml`, replaced the deprecated `st.experimental_rerun()`
  with `st.rerun()`, configured the `Start application` workflow on port 5000,
  and configured autoscale deployment.
- 2026-04-24: Added Groq LLM integration (`app/services/llm.py`, `system.md`,
  Groq Python SDK). Made the chat UI colorful with gradient backgrounds and
  styled chat bubbles. Added a second page `pages/2_📊_Health_Dashboard.py`
  for simulated wearable-device vitals and a derived stress score. Added
  `.env.example` documenting `GROQ_API_KEY`.
