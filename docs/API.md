# FixFind AI — API Contract

This document defines the REST API contract between the Next.js Frontend and the FastAPI Backend.
All endpoints are prefixed with `/api`.

---

## 1. Chat & Conversational Agent

### `POST /api/chat`
Sends multimodal user problem input to the agentic workflow (LangGraph) for reasoning, analysis, and discovery.

#### Request Body
```json
{
  "session_id": "S001",
  "text": "My AC is leaking water",
  "image_url": null,
  "audio_url": null,
  "location": {
    "lat": 17.385,
    "lng": 78.486
  }
}
```

#### Response (Success - 200 OK)
```json
{
  "session_id": "S001",
  "status": "completed",
  "service_category": "ac_repair",
  "analysis": {
    "object": "air_conditioner",
    "issue": "water_leakage",
    "urgency": "medium",
    "preferred_time": "today"
  },
  "needs_clarification": false,
  "clarification_question": null,
  "providers": [
    {
      "id": "P102",
      "name": "Hyderabad Swift AC & Chill",
      "distance_km": 2.1,
      "rating": 4.7,
      "price_min": 400,
      "price_max": 750,
      "availability": "today",
      "fit_score": 95.4,
      "ai_recommendation": "Ranked #1 because they specialize directly in water leakage, are available today within 2.1 km, and have strong customer ratings."
    }
  ]
}
```

#### Response (Clarification Needed - 200 OK)
```json
{
  "session_id": "S001",
  "status": "needs_clarification",
  "needs_clarification": true,
  "clarification_question": "Is the water leaking from the indoor AC unit or the outdoor compressor unit?",
  "providers": []
}
```

---

## 2. Provider Engine

### `POST /api/providers/discover`
Deterministic search and ranking endpoint to query providers matching diagnosed criteria.

#### Request Body
```json
{
  "service": "ac_repair",
  "specialization": "water_leakage",
  "location": {
    "lat": 17.385,
    "lng": 78.486
  },
  "preferred_time": "today"
}
```

#### Response (Success - 200 OK)
```json
{
  "providers": [
    {
      "id": "P102",
      "name": "CoolCare Services",
      "distance_km": 2.1,
      "rating": 4.7,
      "price_min": 400,
      "price_max": 700,
      "availability": "today",
      "fit_score": 95.4
    }
  ]
}
```

---

### `GET /api/providers/{provider_id}`
Retrieve complete profile, reviews, verified badges, and availability slots for a specific provider.

#### Path Parameters
* `provider_id` (string, required): Unique identifier of the provider (e.g., `P102`).

#### Response (Success - 200 OK)
```json
{
  "id": "P102",
  "name": "CoolCare Services",
  "services": ["ac_repair", "ac_cleaning"],
  "specializations": ["water_leakage", "compressor_issues"],
  "location": {
    "type": "Point",
    "coordinates": [78.4867, 17.3850]
  },
  "rating": 4.7,
  "pricing": {
    "min": 400,
    "max": 700
  },
  "availability": {
    "status": "available",
    "slots": ["today_afternoon", "today_evening"]
  },
  "verified": true
}
```

---

## 3. Service Requests

### `POST /api/requests`
Submits a booking request from the user for a selected provider.

#### Request Body
```json
{
  "provider_id": "P102",
  "service": "ac_repair",
  "problem": {
    "issue": "water_leakage"
  },
  "preferred_time": "today"
}
```

#### Response (Success - 201 Created)
```json
{
  "request_id": "REQ-98421",
  "provider_id": "P102",
  "service": "ac_repair",
  "problem": {
    "issue": "water_leakage"
  },
  "preferred_time": "today",
  "status": "confirmed",
  "created_at": "2026-10-03T18:00:00Z"
}
```

---

### `GET /api/requests/{request_id}`
Fetch status and details of an existing service request.

#### Path Parameters
* `request_id` (string, required): Unique service request ID.

#### Response (Success - 200 OK)
```json
{
  "request_id": "REQ-98421",
  "provider_id": "P102",
  "provider_name": "CoolCare Services",
  "service": "ac_repair",
  "status": "confirmed",
  "created_at": "2026-10-03T18:00:00Z"
}
```

---

## 4. Service Fit Score Calculation Contract

The Fit Score is computed **strictly by deterministic backend code** (`ranking_service.py`) and is never invented or modified by the LLM.

### Metric Weights:
* **Problem Compatibility:** 35%
* **Specialization:** 20%
* **Availability:** 15%
* **Distance:** 15%
* **Rating:** 10%
* **Price:** 5%

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
*(Values normalized to 0–100 scale).*
