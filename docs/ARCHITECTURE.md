# FixFind AI — System Architecture

## Overview

FixFind AI is a multimodal, agentic service discovery assistant designed to make service discovery **problem-first** rather than **service-first**. Users describe their issues using text, voice, images, or location, and the system coordinates AI reasoning with deterministic backend services to deliver transparent, ranked recommendations.

---

## 1. High-Level Architecture Diagram

```text
                         USER
                           │
                           ▼
                    NEXT.JS FRONTEND
                           │
                           ▼
                     FASTAPI BACKEND
                           │
                           ▼
                  LANGGRAPH ORCHESTRATOR
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   MULTIMODAL         PROBLEM          CLARIFICATION
     AGENT            ANALYST              AGENT
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                 PROVIDER DISCOVERY
                           │
                           ▼
                  DETERMINISTIC RANKING
                           │
                           ▼
                 RECOMMENDATION AGENT
                           │
                           ▼
                    SERVICE REQUEST
                           │
                           ▼
                        MONGODB
```

---

## 2. Core Architectural Principle

> **"LLMs handle ambiguity, interpretation, reasoning, and explanation.**  
> **Deterministic backend code handles providers, locations, availability, ranking, database operations, and transactions."**

### Critical Safeguards:
1. **No Hallucinated Providers:** The LLM is never allowed to invent, fabricate, or hallucinate provider names, ratings, pricing, or distance. All candidate providers originate exclusively from MongoDB database queries.
2. **Deterministic Ranking:** The ranking score is computed strictly by a deterministic mathematical formula in Python. The LLM does NOT decide numerical rankings.
3. **AI Explanations Only:** The Recommendation Agent receives already-ranked provider data and only generates natural language justifications explaining *why* the provider fits the user's specific problem.

---

## 3. Subsystem Breakdown

### 3.1 Frontend (Next.js)
* **Framework:** Next.js (App Router), React, TypeScript, Tailwind CSS.
* **Capabilities:** Multimodal inputs (audio recording via MediaRecorder, image upload drag-and-drop, geolocation API), responsive conversation view, dynamic fit score badges, provider details modal.

### 3.2 Backend & API (FastAPI)
* **Framework:** FastAPI, Uvicorn, Pydantic v2.
* **Role:** REST gateway validating payloads, managing sessions, bridging frontend requests to the LangGraph orchestrator, and exposing CRUD endpoints for providers and bookings.

### 3.3 Agentic Layer (LangGraph & LangChain)
* **Supervisor Agent:** Controls routing between diagnostic agents, clarification cycles, and provider lookup.
* **Multimodal Agent:** Interprets visual damage (e.g., pipe cracks, dripping water, burnt switches) and audio transcriptions.
* **Problem Analyst Agent:** Maps user problems into structured requirements (object, fault, urgency, service category).
* **Clarification Agent:** Identifies missing information and prompts the user with targeted questions.
* **Recommendation Agent:** Formulates transparent explanations for top matches based on calculated scores.

### 3.4 Provider Discovery & Deterministic Ranking Engine
* **Geospatial Discovery:** MongoDB `$nearSphere` GeoJSON queries filtering active providers within the search radius.
* **Ranking Engine:** Evaluates candidate providers against the user requirements using deterministic multi-factor weighting.

### 3.5 Database (MongoDB)
* **Collections:**
  * `providers`: Provider profiles with GeoJSON `2dsphere` location indexes, services list, specializations, pricing, and ratings.
  * `services`: Hierarchical service catalogue and common problem taxonomies.
  * `requests`: Confirmed service bookings and status updates.
  * `conversations`: Chat sessions and message histories.

---

## 4. Deterministic Service Fit Score Engine

The Fit Score is calculated with the following deterministic weights:

| Metric | Weight | Description |
| :--- | :--- | :--- |
| **Problem Compatibility** | **35%** | Direct match between diagnosed issue and provider capabilities |
| **Specialization** | **20%** | Proven expertise in the specific sub-fault (e.g., water leakage) |
| **Availability** | **15%** | Ability to service within the requested timeframe (e.g., today) |
| **Distance** | **15%** | Proximity to the user's geolocation coordinates |
| **Rating** | **10%** | Normalized provider review score (out of 5.0) |
| **Price** | **5%** | Affordability relative to category average |

### Formula:
```text
Fit Score =
    (ProblemMatch × 0.35)
  + (Specialization × 0.20)
  + (Availability × 0.15)
  + (Distance × 0.15)
  + (Rating × 0.10)
  + (Price × 0.05)
```
*(Total normalized to a 0–100 scale).*
