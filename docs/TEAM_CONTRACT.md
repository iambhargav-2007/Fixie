# Team Contract & Ownership Directory

This document defines code ownership, module boundaries, and coordination protocols for the 3-person hackathon team building **FixFind AI**.

---

## 1. Team Ownership Breakdown

### Developer 1 — AI / Agentic System
**Directory & File Ownership:**
```text
backend/app/agents/
backend/app/graph/
backend/app/models/state.py
```

**Upcoming Responsibilities:**
* **Supervisor Agent:** Orchestrates flow, determines node routing, and maintains conversational context.
* **Multimodal Understanding Agent:** Processes and interprets image, text, and voice/audio transcriptions.
* **Problem Analyst Agent:** Diagnoses root causes, identifies physical objects, determines urgency, and maps issues to service requirements.
* **Clarification Agent:** Generates targeted clarification questions when user intent or diagnostics are ambiguous.
* **Recommendation Agent:** Translates deterministic ranking data into compelling, human-friendly match explanations.
* **LangGraph Workflow:** Builds and compiles the state graph workflow (`backend/app/graph/workflow.py`).
* **Shared Agent State:** Maintains `ServiceState` in `backend/app/models/state.py`.
* **Prompt Engineering:** Manages system prompts and model parameters.

*Note: Do NOT implement agent logic during initial setup.*

---

### Developer 2 — Backend / Provider Engine
**Directory & File Ownership:**
```text
backend/app/api/
backend/app/services/
backend/app/database/
backend/app/models/provider.py
backend/app/models/request.py
seed/
```

**Upcoming Responsibilities:**
* **MongoDB Integration:** Connection pooling, lifecycle events, and index initialization (`connection.py`, `collections.py`).
* **Geospatial Discovery:** MongoDB GeoJSON `2dsphere` queries for radius-based search (`location_service.py`).
* **Service & Provider Catalogue:** Schema enforcement, queries, and seeding (`provider_service.py`, `seed/`).
* **Deterministic Ranking Engine:** Calculates numerical Service Fit Scores strictly via code formula (`ranking_service.py`).
* **Service Request API:** Booking lifecycle and request management (`request_service.py`, `backend/app/api/requests.py`).
* **FastAPI Routers:** Implements `/api/chat`, `/api/providers`, and `/api/requests`.

*Note: Do NOT implement backend engine logic during initial setup.*

---

### Developer 3 — Frontend
**Directory & File Ownership:**
```text
frontend/
```

**Upcoming Responsibilities:**
* **Next.js & React UI:** Build modern, responsive interface using TypeScript and Tailwind CSS.
* **Multimodal Input Capture:** Text input, image upload dropzone, microphone voice recorder, and geolocation access.
* **AI Processing States:** Engaging loading indicators, thought-process micro-animations, and status banners.
* **Conversational Clarification UI:** Seamless chat bubbles and clarification selection chips.
* **Provider Discovery View:** Ranked provider cards showing Fit Score, distance, price range, and AI explanations.
* **Provider Details Modal/Page:** Full specs, ratings, reviews, and service options.
* **Service Request UI:** Booking sheet, contact input, and confirmation state.

*Note: Do NOT create implementations during initial setup.*

---

## 2. Shared Core Files (Coordination Required)

The following files are shared infrastructure and **must NOT be modified casually without cross-team consensus**:

```text
README.md
docs/API.md
docs/ARCHITECTURE.md
docs/TEAM_CONTRACT.md
backend/app/main.py
backend/app/config/
backend/requirements.txt
backend/.env.example
```

### Protocol for Modifying Shared Files:
1. Propose change in team communication channel before editing.
2. Confirm that change will not break other developers' local environments or contracts.
3. Keep commits atomic and pull shared updates promptly.

---

## 3. Branching & Commit Conventions

* **Branching Model:**
  * `main`: Production-ready, stable hackathon demo branch.
  * Feature branches:
    * `feat/agent-<feature-name>` (Developer 1)
    * `feat/backend-<feature-name>` (Developer 2)
    * `feat/frontend-<feature-name>` (Developer 3)
* **Commit Messages:** Follow Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`).
