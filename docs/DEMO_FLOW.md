# FixFind AI — Primary Hackathon Demo Flow

This document details the primary end-to-end demonstration flow for the hackathon presentation.

---

## 1. Demo Scenario Overview

### User Scenario
* **User Action:** Uploads an image of an air conditioner leaking water onto a wall.
* **User Input (Voice or Text):**
  > "My AC started leaking yesterday. I need someone to fix it today."
* **Geolocation:** User shares location via browser (Hyderabad coordinates: `lat: 17.385, lng: 78.486`).

---

## 2. Step-by-Step Conceptual Execution Flow

```text
Image + Text + Location
        ↓
Multimodal Understanding
        ↓
Problem Analysis
        ↓
Identify:
    object = air_conditioner
    issue = water_leakage
    service = ac_repair
    urgency = medium
    preferred_time = today
        ↓
Provider Discovery
        ↓
Fit Score Ranking
        ↓
AI explains best matches
        ↓
User selects provider
        ↓
Service Request Created
        ↓
Confirmation
```

---

## 3. Detailed Walkthrough of Stages

### Stage 1: Multimodal Ingestion & Processing
1. Frontend captures the uploaded picture of the indoor AC split unit with dripping water drops and wall dampness.
2. Frontend sends text, image URL, and location to `POST /api/chat`.
3. The **Multimodal Agent** analyzes the image:
   * Detects indoor split AC unit.
   * Identifies water dripping from the bottom casing.
   * Cross-references user text: *"started leaking yesterday... fix it today"*.

### Stage 2: Problem Analysis & Classification
1. The **Problem Analyst Agent** extracts structured attributes into `ServiceState`:
   * `object`: `"air_conditioner"`
   * `issue`: `"water_leakage"`
   * `service`: `"ac_repair"`
   * `urgency`: `"medium"`
   * `preferred_time`: `"today"`
2. Validates whether sufficient details exist (No clarification needed for this primary happy-path demo).

### Stage 3: Deterministic Provider Discovery & Geospatial Search
1. The **Discovery Service** executes a geospatial query against MongoDB:
   * Finds providers within radius offering `ac_repair`.
   * Filters for availability matching `"today"`.
2. Candidate providers are retrieved (e.g., *CoolCare Solutions*, *Hyderabad Swift AC & Chill*).

### Stage 4: Deterministic Fit Score Ranking
1. The **Ranking Engine** applies the deterministic weighting formula:
   * **Problem Compatibility (35%)** + **Specialization (20%)** + **Availability (15%)** + **Distance (15%)** + **Rating (10%)** + **Price (5%)**.
2. Ranks providers in descending order of score.

### Stage 5: AI Recommendation & Explanation
1. The **Recommendation Agent** inspects the ranked candidate list and generates clear natural-language justifications:
   * *"Hyderabad Swift AC & Chill is ranked #1 (Fit Score 95.4) because they specialize specifically in AC water leakage, are only 2.1 km away, and have available slots for this afternoon."*
2. UI displays interactive cards with badges, breakdown metrics, and the AI explanation.

### Stage 6: Selection & Request Confirmation
1. User clicks **"Request Service"** on the top-ranked provider.
2. Frontend calls `POST /api/requests`.
3. Database creates a confirmed `ServiceRequest` entity.
4. UI renders the **Success Confirmation Screen** with booking ID and provider contact preview.
