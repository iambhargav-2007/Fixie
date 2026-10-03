# Product Requirements Document (PRD)

## FixFind AI — Multimodal Agentic Service Discovery Assistant

**Version:** 1.0  
**Status:** MVP / Hackathon Build  
**Tagline:** *Don't search for a service. Describe the problem.*  

---

## 1. Product Overview
FixFind AI is an intelligent, multimodal local service discovery platform that reverses the traditional directory model. Instead of forcing users to guess technical categories (e.g., "HVAC technician" or "drain auger specialist"), FixFind AI allows users to describe their issue using natural language, voice recordings, photos, and current location. The system diagnoses the issue, discovers nearby providers, scores them using deterministic business logic, and explains matches transparently.

---

## 2. Problem Statement
Traditional local service marketplaces suffer from significant user friction:
* **Taxonomy Confusion:** Users do not know whether a strange washing machine sound requires a motor repair technician, drum specialist, or general electrician.
* **Ambiguous Problem Descriptions:** Text alone often fails to convey the extent of physical damage (e.g., leaks, cracks, scorch marks).
* **Provider Mismatch:** Users waste time contacting providers who are unavailable, out of geographical range, or not specialized in the specific sub-issue.

---

## 3. Solution
FixFind AI provides an agentic, problem-first discovery workflow:
* **Multimodal Problem Intake:** Accepts text, voice notes, damage photos, and GPS location.
* **Agentic Diagnosis:** AI agents identify the affected object, diagnose the probable cause, assess urgency, and determine the exact service category.
* **Conversational Clarification:** Asks concise follow-up questions only when essential information is missing.
* **Deterministic Provider Matching:** Calculates transparent Service Fit Scores using verified business logic rather than AI hallucination.
* **AI-Powered Explanations:** Explains in plain English why a specific provider is recommended.

---

## 4. Target Users
1. **Consumers / Homeowners / Renters:** Individuals experiencing home appliance, plumbing, or electrical breakdowns who need quick, reliable resolution.
2. **Service Providers:** Local technicians seeking high-intent, pre-diagnosed service leads with clear customer problem context.
3. **Platform Administrators:** Operators managing service catalogues, provider verifications, and platform health.

---

## 5. Core User Journey
1. **Intake:** User describes the issue via voice/text and uploads a photo of the damaged appliance or pipe.
2. **Analysis:** The AI pipeline identifies the equipment, symptoms, and urgency, confirming location.
3. **Clarification (if needed):** AI prompts for specific missing details (e.g., "Is it the indoor or outdoor unit?").
4. **Discovery & Ranking:** Backend queries active local providers and computes deterministic Fit Scores.
5. **Review:** User views ranked provider cards with AI match rationales.
6. **Request:** User clicks "Request Service" to book the provider.

---

## 6. MVP Scope
* **Supported Categories:** Appliance Repair, Plumbing, Electrical, Home Maintenance, Vehicle Assistance, Cleaning.
* **Multimodal Intake:** Text, image upload, voice audio input, GPS location.
* **Agentic Engine:** Supervisor, Multimodal, Problem Analyst, Clarification, and Recommendation agents.
* **Deterministic Ranking:** Multi-factor scoring formula (compatibility, specialization, availability, distance, rating, price).
* **Booking:** Direct service request generation with confirmation screen.
* **Out of Scope for MVP:** In-app payments, live GPS vehicle tracking, multi-vendor bidding wars.

---

## 7. Functional Requirements
* **FR-01 (Multimodal Input):** System shall ingest text, image files, audio recordings, and latitude/longitude.
* **FR-02 (Diagnostic Analysis):** AI shall extract object name, fault type, estimated urgency, and required service ID.
* **FR-03 (Interactive Clarification):** AI shall ask targeted single-turn clarification if confidence is low.
* **FR-04 (Geospatial Discovery):** System shall retrieve providers within a configured radius using MongoDB GeoJSON `2dsphere` indexes.
* **FR-05 (Deterministic Scoring):** System shall compute a 0–100 Fit Score using defined multi-criteria weights.
* **FR-06 (Match Explanation):** Recommendation agent shall articulate why top providers match the user's specific context.
* **FR-07 (Service Request Booking):** System shall store confirmed service bookings with provider and customer details.

---

## 8. Agent Architecture
Built using **LangGraph**:
* **Supervisor Agent:** Flow orchestration and conditional branching.
* **Multimodal Agent:** Vision and audio transcription analysis.
* **Problem Analyst Agent:** Symptom classification and service mapping.
* **Clarification Agent:** Ambiguity resolution and follow-up generation.
* **Recommendation Agent:** Natural language translation of deterministic ranking data.

---

## 9. Backend Architecture
Built with **Python & FastAPI**:
* Modular layered structure: `api/` (routes), `services/` (business logic), `database/` (MongoDB connection & queries), `models/` (Pydantic schemas & TypedDict state).
* Asynchronous execution for LLM orchestration and database I/O.
* Separation of concerns: LLMs reason and explain; backend code calculates and stores.

---

## 10. Frontend Architecture
Built with **Next.js & React (TypeScript & Tailwind CSS)**:
* Responsive single-page application with conversational and card-based discovery views.
* Native browser API integrations: Geolocation API, MediaStream/MediaRecorder API for voice input, Drag-and-Drop File API.
* Micro-animations for agent processing states and confidence rating indicators.

---

## 11. Database
**MongoDB** NoSQL Document Store:
* `providers`: GeoJSON `2dsphere` indexed profiles, service tags, pricing, and availability.
* `services`: Hierarchy of categories, services, and diagnostic keywords.
* `requests`: Bookings with status tracking (`pending`, `confirmed`, `completed`).
* `conversations`: Persisted session histories.

---

## 12. API Contract
* `POST /api/chat`: Primary conversational and diagnostic endpoint.
* `POST /api/providers/discover`: Deterministic search and ranking endpoint.
* `GET /api/providers/{provider_id}`: Detailed provider profile retrieval.
* `POST /api/requests`: Service booking submission.
* `GET /api/requests/{request_id}`: Service booking status lookup.

*(Full specifications in [docs/API.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/API.md)).*

---

## 13. Non-Functional Requirements
* **Latency:** Diagnostic response within < 3.5 seconds; provider discovery query within < 300 ms.
* **Reliability:** Graceful fallbacks if image recognition or LLM APIs encounter timeouts.
* **Accuracy & Safety:** Zero fabricated providers; deterministic calculation of all financial and ranking metrics.
* **Usability:** Mobile-first layout with high visual contrast and accessible touch targets.

---

## 14. Demo Flow
* **Scenario:** User uploads a photo of an AC leaking water inside their home with the prompt: *"My AC started leaking yesterday. I need someone to fix it today."*
* **Execution:** Multimodal vision identifies water dripping from an indoor split AC unit -> Problem analyst classifies as `ac_repair` (`water_leakage`, medium urgency, today) -> Discovery service queries Hyderabad providers -> Ranking engine scores matches -> Recommendation agent explains top fit -> User books provider.
*(Full script in [docs/DEMO_FLOW.md](file:///c:/Users/Bhargav/Desktop/Fixie/docs/DEMO_FLOW.md)).*

---

## 15. Future Scope
* Dynamic real-time provider bid negotiation.
* Native mobile applications (iOS/Android) with push notifications.
* Integrated escrow payments and customer dispute resolution.
* Tele-diagnosis video calls with AI assistant sidecar.
