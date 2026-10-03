# Product Requirements Document (PRD)

## Fixie — Multimodal Agentic Service Discovery Assistant

**Version:** 1.0
**Status:** MVP / Hackathon Build
**Target Build Time:** 6–7 hours
**Primary Platform:** Web Application
**Frontend:** Next.js
**Backend:** FastAPI
**Agent Orchestration:** LangGraph
**Database:** MongoDB
**AI:** Multimodal LLM + Speech-to-Text
**Primary MVP Domain:** Local Home & Appliance Services

---

# 1. Executive Summary

**Fixie** is an AI-powered multimodal service discovery platform that helps users find the **right service for a problem**, even when the user does not know what service they need.

Traditional service marketplaces generally require users to first identify the service:

> "I need an AC technician."

FixFind AI reverses this interaction:

> **"My AC is leaking. Here's a picture. I need someone today."**

The system understands the user's problem using **text, voice, image, and location**, identifies the likely service category and requirements, asks clarification questions when necessary, discovers suitable nearby service providers, calculates a deterministic **Service Fit Score**, explains the recommendations using AI, and allows the user to initiate a service request.

The platform combines:

* Multimodal AI
* Agentic AI
* Conversational interaction
* Geospatial discovery
* Provider matching
* Deterministic ranking
* AI-generated explanations
* Service-request workflows

The MVP will use a controlled service-provider catalogue rather than attempting to build a full-scale marketplace.

---

# 2. Product Vision

### Vision

> **Make local service discovery problem-first instead of service-first.**

Users should not need to understand service terminology, diagnose their problem, or know which professional to search for.

They should simply be able to:

> **Show us the problem. Tell us what happened. We'll figure out the service.**

---

# 3. Product Mission

FixFind AI aims to reduce the friction between:

**A user's real-world problem**

and

**the service provider capable of solving it.**

The system should transform an unstructured problem into an actionable service request.

```text
User Problem
     ↓
AI Understanding
     ↓
Service Identification
     ↓
Provider Discovery
     ↓
Intelligent Matching
     ↓
Recommendation
     ↓
Service Request
```

---

# 4. Problem Statement

## 4.1 Existing problem

Local service discovery often requires users to know:

* what service category they need
* what their problem is called
* what type of technician to search for
* which providers specialize in the specific problem
* whether providers are available
* what a reasonable price is
* which provider is geographically convenient

For example:

> "My washing machine is making a strange noise."

A user may not know whether they need:

* appliance repair
* washing machine repair
* motor repair
* drum repair
* electrical repair

The user must figure this out before finding a provider.

---

# 5. Proposed Solution

FixFind AI introduces a **problem-first service discovery workflow**.

The user provides:

### Text

> "My refrigerator isn't cooling."

### Voice

> "It started yesterday and there is a strange sound."

### Image

Photo of the refrigerator.

### Location

Current or selected location.

The system combines these inputs and generates:

```text
Problem:
Refrigerator cooling issue

Likely service:
Refrigerator Repair

Possible specialization:
Cooling / compressor-related issue

Urgency:
Medium

Preferred time:
Today
```

The system then discovers suitable providers and ranks them.

---

# 6. Target Users

## 6.1 Primary User — Consumer

People who need local services but may not know the correct service category.

Examples:

* students
* families
* renters
* homeowners
* working professionals
* elderly users
* non-technical users

---

## 6.2 Secondary User — Service Provider

Local technicians/service businesses who want to receive relevant service requests.

Examples:

* AC technicians
* electricians
* plumbers
* appliance repair professionals
* cleaning providers
* vehicle service providers

---

## 6.3 Admin

Platform administrator responsible for:

* provider management
* service catalogue
* provider verification
* availability
* analytics
* service categories

---

# 7. Product Scope

## 7.1 MVP Scope

The MVP will support:

* User registration/profile
* Text-based service discovery
* Voice-based queries
* Image-based service discovery
* Multimodal problem understanding
* Service classification
* Requirement extraction
* Conversational clarification
* Location-based provider discovery
* Provider catalogue
* Provider profiles
* Service filtering
* Distance filtering
* Availability
* Pricing
* Ratings
* AI recommendations
* Service-fit scoring
* Recommendation explanations
* Provider comparison
* Shortlisting
* Service request initiation
* Conversation/session history
* Basic provider dashboard
* Basic admin management

---

# 8. Out of Scope for MVP

To remain achievable within the 6–7 hour hackathon window:

* Real payment processing
* Full provider onboarding system
* Real-time technician GPS tracking
* Complex review moderation
* Production notification infrastructure
* Provider mobile application
* Advanced dynamic pricing
* Full-scale marketplace integrations
* Insurance processing
* Background verification infrastructure
* Automated dispute resolution
* Real-world payment settlement
* Training custom AI models

These can be future extensions.

---

# 9. Core User Journey

## Primary User Journey

```text
Open FixFind
      ↓
Enter problem
      ↓
Optional image/voice
      ↓
Provide location
      ↓
AI understands problem
      ↓
Requirements complete?
      │
      ├── No → Ask clarification
      │          ↓
      │       User response
      │          ↓
      │       Re-analyze
      │
      └── Yes
             ↓
      Identify required service
             ↓
      Discover providers
             ↓
      Calculate service-fit score
             ↓
      Rank providers
             ↓
      Generate AI explanations
             ↓
      User compares providers
             ↓
      Select provider
             ↓
      Create service request
             ↓
      Confirmation
```

---

# 10. Example End-to-End Scenario

### Input

User uploads:

**Image:** leaking AC

Text:

> "My AC started leaking yesterday. I need someone to fix it today."

Location:

> User location

---

### AI Understanding

```json
{
  "asset": "air_conditioner",
  "issue": "water_leakage",
  "service_category": "ac_repair",
  "specialization": "leakage_drainage",
  "urgency": "medium",
  "preferred_time": "today"
}
```

---

### Provider discovery

The system finds:

```text
CoolCare
2.1 km
4.7 rating
Available today
₹400–₹700

QuickFix
3.4 km
4.5 rating
Available today
₹350–₹600

AC Experts
5.2 km
4.8 rating
Available tomorrow
₹500–₹800
```

---

### Ranking

```text
CoolCare      95.4%
QuickFix      89.2%
AC Experts    84.7%
```

---

### AI explanation

> CoolCare is a strong match because they specialize in AC leakage and drainage repairs, are 2.1 km away, have same-day availability, and fall within the expected price range.

---

### User action

**Request Service**

---

# 11. Functional Requirements

## FR-01 — User Registration

Users should be able to create an account.

### Required fields

* Name
* Email/phone
* Optional profile information
* Location permission/preference

### MVP implementation

Can use lightweight authentication to save development time.

---

# 12. FR-02 — User Profile

User profile should contain:

* Name
* Contact information
* Preferred location
* Saved providers
* Service history
* Search history

---

# 13. FR-03 — Text Search

User can enter natural-language queries.

Examples:

> "My AC is leaking."

> "Need someone to fix my washing machine."

> "There is water coming from my kitchen pipe."

The system must not require predefined keywords.

---

# 14. FR-04 — Voice Search

User can record a voice request.

Pipeline:

```text
Voice
 ↓
Speech-to-Text
 ↓
Natural Language
 ↓
Agentic Workflow
```

The transcript becomes part of the conversation context.

---

# 15. FR-05 — Image Search

User can upload an image.

Supported examples:

* appliance
* visible leakage
* broken component
* wall damage
* electrical issue
* vehicle problem

The multimodal model analyzes the image.

---

# 16. FR-06 — Multimodal Understanding

The system should combine:

```text
Text
+
Image
+
Voice transcript
+
Location
```

rather than processing each input independently.

Output should contain structured observations.

---

# 17. FR-07 — Problem Identification

The Problem Analyst should identify:

* object/asset
* problem
* symptoms
* likely service
* specialization
* urgency
* preferred time
* budget where available

Example:

```json
{
  "asset": "washing_machine",
  "issue": "not_draining",
  "service": "washing_machine_repair",
  "specialization": "drainage",
  "urgency": "medium"
}
```

---

# 18. FR-08 — Requirement Extraction

The system should extract relevant requirements from natural language.

Possible fields:

```text
service
problem
asset
urgency
budget
preferred date
preferred time
location
specialization
```

Not all fields are required.

---

# 19. FR-09 — Clarification

If required information is missing, the system must ask a targeted question.

Example:

User:

> "My washing machine isn't working."

AI:

> "What happens when you turn it on?"

Possible answers:

* Doesn't turn on
* Turns on but doesn't drain
* Makes unusual noise
* Leaks
* Other

---

# 20. FR-10 — Context Preservation

The clarification process must preserve previous context.

Example:

```text
User:
My washing machine isn't working.

AI:
What happens when you turn it on?

User:
It turns on but doesn't drain.
```

The system understands:

```text
"it" = washing machine
```

because previous conversation state is available.

---

# 21. FR-11 — Service Classification

The system should map the problem to the service catalogue.

Example:

```text
AC leaking
       ↓
Appliance Repair
       ↓
AC Repair
       ↓
Leakage / Drainage Specialist
```

---

# 22. FR-12 — Provider Discovery

The system searches the provider catalogue using:

* service category
* specialization
* location
* service area
* availability

---

# 23. FR-13 — Geospatial Search

The system should identify providers near the user.

Example:

```text
User
 │
 ├── 2.1 km → Provider A
 ├── 3.4 km → Provider B
 └── 5.2 km → Provider C
```

MongoDB's geospatial functionality will be used for the MVP.

---

# 24. FR-14 — Provider Profiles

Each provider profile should contain:

* name
* services
* specializations
* rating
* price range
* location
* distance
* availability
* verification status
* service area
* experience

---

# 25. FR-15 — Provider Filtering

Users should be able to filter results by:

* distance
* rating
* price
* availability
* service specialization

---

# 26. FR-16 — Provider Ranking

Providers should be ranked using a deterministic **Service Fit Score**.

Proposed scoring:

| Factor                | Weight |
| --------------------- | -----: |
| Problem compatibility |    35% |
| Specialization        |    20% |
| Availability          |    15% |
| Distance              |    15% |
| Rating                |    10% |
| Price                 |     5% |

Formula:

```text
Fit Score =
Problem Match × 0.35
+
Specialization × 0.20
+
Availability × 0.15
+
Distance × 0.15
+
Rating × 0.10
+
Price × 0.05
```

---

# 27. FR-17 — AI Recommendation

The system should present the most relevant providers based on the calculated scores.

Important:

**The LLM should not arbitrarily determine the ranking.**

Ranking is calculated by backend logic.

The LLM explains the result.

---

# 28. FR-18 — Recommendation Explanation

Each recommendation should contain:

### Why this provider?

Example:

> This provider specializes in AC leakage repairs, is 2.1 km away, has availability today, and fits your expected price range.

The explanation must be generated from actual provider data.

---

# 29. FR-19 — Provider Comparison

User should be able to compare shortlisted providers.

Example:

|              | CoolCare | QuickFix |
| ------------ | -------- | -------- |
| Service Fit  | 95%      | 89%      |
| Distance     | 2.1 km   | 3.4 km   |
| Rating       | 4.7      | 4.5      |
| Availability | Today    | Today    |
| Price        | ₹400–700 | ₹350–600 |

---

# 30. FR-20 — Save Provider

User can save a provider for later.

---

# 31. FR-21 — Service Request

User can select a provider and initiate a request.

Request should contain:

* user
* provider
* service
* problem
* location
* preferred time
* budget
* status

---

# 32. FR-22 — Service Request Status

Initial MVP states:

```text
Pending
Accepted
Rejected
Completed
Cancelled
```

---

# 33. FR-23 — Service History

User can see:

```text
Previous searches
Previous requests
Selected providers
Request status
```

---

# 34. FR-24 — Provider Dashboard

Provider should be able to:

* view requests
* accept/reject
* update availability
* view basic customer requirement
* update request status

---

# 35. FR-25 — Admin

Admin should be able to manage:

* providers
* service categories
* services
* provider availability
* provider verification
* basic analytics

---

# 36. Agent Architecture

## Agentic Layer

### Agent 1 — Supervisor

Responsibilities:

* route workflow
* invoke agents
* handle conditional paths
* manage clarification loop

---

### Agent 2 — Multimodal Understanding Agent

Responsibilities:

* interpret images
* combine text and visual observations
* consume voice transcript
* produce structured observations

---

### Agent 3 — Problem Analyst Agent

Responsibilities:

* identify asset
* identify problem
* identify service
* extract requirements
* identify missing information

---

### Agent 4 — Clarification Agent

Responsibilities:

* determine useful clarification question
* ask concise question
* incorporate user response
* preserve context

---

### Agent 5 — Recommendation Agent

Responsibilities:

* consume deterministic provider rankings
* explain recommendations
* personalize presentation
* summarize trade-offs

---

# 37. What Is NOT an Agent

These should remain conventional services:

```text
Provider Search
Location Search
Distance Calculation
Availability
Filtering
Service Catalogue
Ranking
Database
Authentication
Request Creation
Request Status
```

This is deliberate.

---

# 38. LLM Responsibilities

LLM is used for:

### 1. Multimodal interpretation

```text
Image + Text → Observations
```

### 2. Problem reasoning

```text
Natural language → Structured problem
```

### 3. Clarification

```text
Incomplete requirements → Question
```

### 4. Recommendation explanation

```text
Ranked provider data → Human explanation
```

---

# 39. Non-LLM Responsibilities

Normal backend code handles:

```text
Database queries
Geospatial queries
Distance
Filtering
Availability
Scoring
Authentication
Requests
History
```

Core principle:

> **LLM for ambiguity and reasoning; deterministic code for facts and transactions.**

---

# 40. LangGraph State

The shared state should approximately contain:

```python
class ServiceState(TypedDict):

    session_id: str

    messages: list

    text_input: str | None
    image_input: str | None
    audio_input: str | None

    location: dict | None

    transcription: str | None
    vision_result: dict | None

    problem: dict | None
    requirements: dict | None

    missing_information: list
    clarification_question: str | None

    service_category: str | None

    candidate_providers: list
    ranked_providers: list

    recommendation: dict | None

    selected_provider: dict | None
    service_request: dict | None
```

---

# 41. Agent Workflow

```text
START
  │
  ▼
SUPERVISOR
  │
  ├── Image → MULTIMODAL
  │
  ├── Voice → STT
  │
  └── Text → PROBLEM ANALYST
                    │
                    ▼
              Requirements?
                /       \
              NO         YES
              │           │
              ▼           ▼
        CLARIFICATION   SERVICE
              │         DISCOVERY
              │           │
              └───────────┘
                          │
                          ▼
                     GEO FILTER
                          │
                          ▼
                     AVAILABILITY
                          │
                          ▼
                       RANKING
                          │
                          ▼
                   RECOMMENDATION
                          │
                          ▼
                     USER SELECT
                          │
                          ▼
                   SERVICE REQUEST
                          │
                          ▼
                         END
```

---

# 42. Database Architecture

## MongoDB Collections

```text
users
providers
services
conversations
service_requests
search_history
```

---

## Users

```json
{
  "_id": "U101",
  "name": "User",
  "email": "user@example.com",
  "phone": "...",
  "location": {
    "type": "Point",
    "coordinates": [78.4867, 17.3850]
  },
  "saved_providers": [],
  "preferences": {}
}
```

---

## Providers

```json
{
  "_id": "P102",
  "name": "CoolCare Services",

  "services": [
    "ac_repair"
  ],

  "specializations": [
    "water_leakage",
    "drainage"
  ],

  "location": {
    "type": "Point",
    "coordinates": [78.4800, 17.3900]
  },

  "rating": 4.7,

  "pricing": {
    "min": 400,
    "max": 700
  },

  "availability": {
    "status": "available",
    "slots": ["16:00", "18:00"]
  },

  "verified": true
}
```

---

# 43. Conversations

```json
{
  "_id": "SESSION123",
  "user_id": "U101",

  "messages": [],

  "state": {
    "asset": "air_conditioner",
    "issue": "water_leakage",
    "leak_location": "indoor_unit"
  }
}
```

This provides persistence for the conversational workflow.

---

# 44. Service Requests

```json
{
  "_id": "REQ1001",

  "user_id": "U101",

  "provider_id": "P102",

  "service": "ac_repair",

  "problem": {
    "issue": "water_leakage",
    "specialization": "drainage"
  },

  "preferred_time": "today",

  "status": "pending"
}
```

---

# 45. API Requirements

## Authentication

```text
POST /auth/register
POST /auth/login
```

---

## Conversation

```text
POST /chat/session
POST /chat/message
GET  /chat/{session_id}
```

---

## Multimodal

```text
POST /upload/image
POST /upload/audio
```

---

## Service discovery

```text
POST /services/analyze
GET  /services
GET  /services/{id}
```

---

## Providers

```text
GET /providers
GET /providers/{id}
GET /providers/nearby
```

---

## Recommendations

```text
POST /recommendations
```

---

## Requests

```text
POST /requests
GET  /requests
GET  /requests/{id}
PATCH /requests/{id}/status
```

---

# 46. Non-Functional Requirements

## Performance

For MVP:

* Initial UI response should be fast.
* AI processing should display clear progress states.
* Provider search should return within a few seconds after AI analysis.
* Avoid unnecessary LLM calls.

---

## Reliability

The system should:

* validate LLM structured output
* handle failed AI calls
* handle missing images
* handle missing location
* prevent invalid provider requests
* avoid hallucinated provider information

---

# 47. AI Reliability Requirements

The LLM must **not invent**:

* providers
* ratings
* prices
* availability
* distance
* service capabilities

All provider facts must originate from our database or external verified sources.

The LLM may explain those facts.

---

# 48. Privacy Requirements

User location is sensitive.

The system should:

* request location permission
* avoid unnecessary location storage
* only use location for service discovery
* protect personal information
* avoid exposing exact user location to unrelated providers unless required for the service request
* use secure API communication

---

# 49. Error Handling

### If image analysis fails

Fallback:

> "I couldn't confidently understand the image. Could you describe the problem?"

### If location unavailable

Ask:

> "Please select your location so I can find nearby providers."

### If requirements incomplete

Trigger clarification.

### If no provider exists

Show:

> "We couldn't find a suitable provider nearby."

Offer:

* larger radius
* alternative service category
* different availability

---

# 50. Empty-State Handling

If no provider matches:

```text
No exact matches found.

Try:
[Expand search radius]
[View related services]
[Change preferred time]
```

This prevents the system from hallucinating a provider.

---

# 51. Security Requirements

The application should implement:

* authenticated API requests
* input validation
* file type validation
* upload size limits
* secure password handling if password auth is used
* environment variables for API keys
* server-side API key protection
* authorization for provider/admin operations

---

# 52. MVP Dataset

Because we have only 6–7 hours, we should seed realistic data.

Target:

```text
6 service categories
20–30 service types
50–100 providers
```

Each provider should contain:

* location
* services
* specializations
* pricing
* rating
* availability

This gives us enough data to demonstrate meaningful discovery.

---

# 53. MVP Service Categories

```text
Home Services
│
├── Appliance Repair
│   ├── AC Repair
│   ├── Washing Machine Repair
│   ├── Refrigerator Repair
│   └── TV Repair
│
├── Plumbing
│   ├── Pipe Leakage
│   ├── Tap Repair
│   └── Drainage
│
├── Electrical
│   ├── Fan Repair
│   ├── Switch Repair
│   └── Wiring
│
├── Home Maintenance
│   ├── Painting
│   └── Furniture Repair
│
├── Vehicle Assistance
│   ├── Battery
│   └── Tyre
│
└── Cleaning
    ├── Home Cleaning
    ├── Sofa Cleaning
    └── AC Cleaning
```

---

# 54. Primary Hackathon Demo

The strongest demo should be:

## AC Water Leakage

### Step 1

Upload AC image.

### Step 2

Say:

> "My AC started leaking yesterday and I need someone today."

### Step 3

AI analyzes.

### Step 4

System identifies:

```text
AC Repair
+
Leakage/Drainage
```

### Step 5

Nearby providers appear.

### Step 6

Fit scores appear.

### Step 7

AI explains recommendation.

### Step 8

User requests service.

### Step 9

Provider dashboard shows new request.

This demonstrates nearly every major part of the architecture.

---

# 55. Secondary Demo

Use a conversation requiring clarification.

### User:

> "My washing machine isn't working."

AI:

> "What happens when you turn it on?"

User:

> "It turns on but doesn't drain."

AI:

> "Got it. I found washing machine drainage specialists near you."

Then results.

This demonstrates **agent memory + clarification loop**.

---

# 56. Product Differentiation

FixFind's differentiation is not:

> "We use AI."

Instead:

### Traditional marketplace

```text
Know service
     ↓
Search
     ↓
Provider
```

### FixFind

```text
Have problem
     ↓
Describe/show problem
     ↓
AI understands
     ↓
AI identifies service
     ↓
Finds suitable provider
     ↓
Explains match
     ↓
Request service
```

---

# 57. Key Product Differentiators

### 1. Problem-first discovery

Users don't need to know the service terminology.

### 2. Multimodal input

Text + image + voice + location.

### 3. Clarification loop

AI asks questions instead of guessing.

### 4. Service Fit Score

Provider selection is based on multiple real factors.

### 5. Explainable recommendations

Users know why a provider was recommended.

### 6. Agentic workflow

The system dynamically decides what information/action is needed next.

---

# 58. Success Metrics for MVP

Since this is a hackathon MVP, the most important metrics are functional.

### Primary

**Problem-to-Service Accuracy**

Percentage of test cases where the system identifies the appropriate service category.

### Secondary

**Provider Match Relevance**

Whether returned providers actually support the identified service/specialization.

### Conversational Completion

Percentage of incomplete requests successfully completed through clarification.

### End-to-End Completion

Percentage of test flows reaching:

```text
Problem → Provider → Request
```

### Response Quality

Human evaluation of recommendation explanations.

---

# 59. Acceptance Criteria

The MVP is considered successful if:

### AC-01

User can enter a natural-language service problem.

### AC-02

User can upload an image.

### AC-03

User can submit voice input.

### AC-04

System can combine multimodal inputs.

### AC-05

System identifies a service category.

### AC-06

System asks clarification when required.

### AC-07

Clarification maintains previous context.

### AC-08

System searches nearby providers.

### AC-09

System considers provider specialization.

### AC-10

System considers availability.

### AC-11

System calculates Service Fit Score.

### AC-12

System explains recommendation.

### AC-13

User can select provider.

### AC-14

User can create service request.

### AC-15

Request appears in provider dashboard.

### AC-16

Conversation/request persists in MongoDB.

---

# 60. Hackathon Build Priority

Because we only have 6–7 hours, features should be divided into priorities.

## P0 — Absolutely required

```text
Frontend
Backend
MongoDB
LangGraph
Text input
Image input
Problem analysis
Clarification
Provider database
Provider search
Location filtering
Ranking
Recommendation
Service request
```

---

## P1 — Important

```text
Voice
Map
Provider dashboard
History
Saved providers
Comparison
```

---

## P2 — Nice to have

```text
Advanced admin
Reviews
Notifications
Advanced personalization
Complex analytics
```

If time runs out, **P2 is sacrificed first**.

---

# 61. 7-Hour Build Strategy

## Hour 1 — Foundation

* Repository
* Next.js
* FastAPI
* MongoDB
* Environment configuration
* Basic UI

---

## Hour 2 — Database + APIs

* MongoDB collections
* Provider seed data
* Service catalogue
* Provider APIs
* Request APIs

---

## Hour 3 — Agentic Core

* LangGraph
* ServiceState
* Supervisor
* Problem Analyst
* Structured output

---

## Hour 4 — Multimodal + Clarification

* Image input
* Vision
* Voice/STT if feasible
* Clarification loop
* Context persistence

---

## Hour 5 — Discovery + Ranking

* Geospatial search
* Provider filtering
* Availability
* Fit-score engine
* Recommendation explanations

---

## Hour 6 — Frontend Integration

* Chat
* Upload
* AI processing
* Results
* Provider cards
* Request screen

---

## Hour 7 — Demo + Polish

* Provider dashboard
* Error handling
* UI polish
* Seed data
* Test complete flow
* Demo preparation

---

# 62. Recommended Repository Structure

```text
fixfind-ai/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   └── types/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   │   ├── supervisor.py
│   │   │   ├── multimodal.py
│   │   │   ├── problem_analyst.py
│   │   │   ├── clarification.py
│   │   │   └── recommendation.py
│   │   │
│   │   ├── services/
│   │   │   ├── provider_service.py
│   │   │   ├── discovery_service.py
│   │   │   ├── location_service.py
│   │   │   ├── ranking_service.py
│   │   │   └── request_service.py
│   │   │
│   │   ├── models/
│   │   │   ├── state.py
│   │   │   ├── provider.py
│   │   │   └── request.py
│   │   │
│   │   ├── database/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── seed/
│   ├── providers.json
│   └── services.json
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── API.md
│
└── README.md
```

---

# 63. Final System Architecture

```text
                         FIXFIND AI
              "Don't search. Describe the problem."
                              │
                              ▼
                    ┌───────────────────┐
                    │     Next.js       │
                    │    Frontend       │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │      FastAPI      │
                    │      Backend      │
                    └─────────┬─────────┘
                              │
                              ▼
             ╔════════════════════════════════╗
             ║         LANGGRAPH              ║
             ║                                ║
             ║       ┌──────────────┐         ║
             ║       │  Supervisor  │         ║
             ║       └──────┬───────┘         ║
             ║              │                  ║
             ║    ┌─────────┼─────────┐        ║
             ║    ▼         ▼         ▼        ║
             ║ Multimodal Problem  Clarify     ║
             ║   Agent    Analyst    Agent      ║
             ║              │                  ║
             ║              ▼                  ║
             ║       Recommendation            ║
             ║           Agent                 ║
             ╚══════════════╪═══════════════════╝
                            │
                            ▼
             ┌──────────────────────────────┐
             │   DETERMINISTIC ENGINE      │
             │                              │
             │ Service Discovery            │
             │ Geospatial Search            │
             │ Availability                 │
             │ Filtering                    │
             │ Service Fit Score            │
             │ Request Management           │
             └──────────────┬───────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   MongoDB    │
                    │              │
                    │ Users        │
                    │ Providers    │
                    │ Services     │
                    │ Conversations│
                    │ Requests     │
                    └──────────────┘
```

---

# 64. Final Product Definition

### **FixFind AI**

> **A multimodal agentic service discovery assistant that transforms an unstructured real-world problem into an actionable local service request.**

The user doesn't need to know:

> "What service should I search for?"

They simply need to say:

> **"This is my problem."**

FixFind handles:

```text
UNDERSTAND
     ↓
CLARIFY
     ↓
IDENTIFY
     ↓
DISCOVER
     ↓
MATCH
     ↓
EXPLAIN
     ↓
CONNECT
```

And technically, our architecture follows a very deliberate boundary:

> **AI handles ambiguity and reasoning.
> Deterministic software handles search, location, ranking, data, and transactions.
> LangGraph manages the agentic workflow and shared context.
> MongoDB persists the application and conversation state.**

That gives us a **genuine multi-agent system**, a meaningful multimodal capability, a practical service marketplace workflow, and—most importantly for the hackathon—a scope that can actually be completed end-to-end rather than a collection of disconnected AI demos.
