# FixFind AI

> Don't search for a service. Describe the problem.

FixFind AI is a multimodal, agentic service discovery assistant that connects users directly to the right local service providers based on unstructured descriptions, voice notes, damage photos, and GPS location.

---

## What is FixFind?

Traditional service marketplaces require users to know what service they need beforehand. FixFind AI reverses this paradigm: users simply describe their issue, show a picture, or record a voice note. The AI pipeline diagnoses the root problem, identifies the right service category, queries nearby service providers, calculates deterministic Service Fit Scores, and explains the best recommendations in plain language.

---

## Architecture

```text
User Problem (Text / Voice / Image / GPS)
                    ↓
          FastAPI Backend Gateway
                    ↓
       LangGraph Multi-Agent System
  ┌─────────────────┼─────────────────┐
  ▼                 ▼                 ▼
Multimodal       Problem        Clarification
  Agent          Analyst            Agent
  └─────────────────┼─────────────────┘
                    ↓
        Provider Discovery Engine
                    ↓
       Deterministic Ranking (Fit Score)
                    ↓
          Recommendation Agent
                    ↓
          Service Booking & MongoDB
```

---

## Tech Stack

* **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS
* **Backend:** FastAPI, Python, Uvicorn, Pydantic v2
* **AI & Agents:** LangGraph, LangChain, Multimodal LLM
* **Database:** MongoDB (with GeoJSON `2dsphere` geospatial indexing)

---

## Team Structure & Ownership

This repository is developed by a 3-person hackathon team with separated code ownership:

* **Developer 1 — AI / Agentic System**
  * `backend/app/agents/`
  * `backend/app/graph/`
  * `backend/app/models/state.py`
* **Developer 2 — Backend / Provider Engine**
  * `backend/app/api/`
  * `backend/app/services/`
  * `backend/app/database/`
  * `backend/app/models/provider.py`
  * `backend/app/models/request.py`
  * `seed/`
* **Developer 3 — Frontend**
  * `frontend/`

*For full details on boundaries and coordination protocols, see [TEAM_CONTRACT.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/TEAM_CONTRACT.md).*

---

## Documentation

* [PRD.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/PRD.md) — Product Requirements Document
* [ARCHITECTURE.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/ARCHITECTURE.md) — System Architecture & Fit Score Formula
* [API.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/API.md) — API Contracts & Payloads
* [TEAM_CONTRACT.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/TEAM_CONTRACT.md) — Module Ownership & Guidelines
* [DEMO_FLOW.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/DEMO_FLOW.md) — Primary Hackathon Demo Walkthrough

---

## Local Setup

### Prerequisites
* Python 3.10+
* Node.js 18+
* MongoDB instance (local or MongoDB Atlas)

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](file:///c:/Users/Bhargav/Desktop/Fixie/LICENSE) file for details.
