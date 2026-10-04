"""Chat and conversational agent API routes."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from backend.app.graph.workflow import build_graph
from backend.app.models.state import ServiceState
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")
graph = build_graph()

# Simplest memory session storage for hackathon
_sessions: Dict[str, ServiceState] = {}

class LocationInput(BaseModel):
    lat: float
    lng: float
    locality: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    text: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    location: Optional[LocationInput] = None

class ProviderResponse(BaseModel):
    id: str
    name: str
    services: List[str]
    specializations: List[str]
    distance_km: float
    rating: float
    price_min: float
    price_max: float
    availability_status: str
    availability_slots: List[str]
    verified: bool
    fit_score: float
    score_breakdown: Dict[str, float]

class ChatResponse(BaseModel):
    session_id: str
    workflow_status: str
    message: str
    clarification_question: Optional[str] = None
    problem: Optional[Dict[str, Any]] = None
    service: Optional[Dict[str, str]] = None
    providers: List[ProviderResponse] = []
    recommendation: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id
    
    state = _sessions.get(session_id)
    if not state:
        state = ServiceState(
            session_id=session_id,
            messages=[],
            missing_information=[]
        )
    
    if "messages" not in state:
        state["messages"] = []
        
    if req.text:
        state["text_input"] = req.text
        state["messages"].append({"role": "user", "content": req.text})
    if req.image_url:
        state["image_input"] = req.image_url
    if req.audio_url:
        state["audio_input"] = req.audio_url
        
    if req.location:
        state["location"] = req.location.model_dump()
    else:
        state["location"] = {
            "lat": 17.3850,
            "lng": 78.4867,
            "locality": "Hyderabad"
        }
        
    try:
        new_state = graph.invoke(state)
        _sessions[session_id] = new_state
        state = new_state
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        raise HTTPException(status_code=500, detail="Internal workflow error")
        
    status = state.get("workflow_status", "error")
    
    if status == "clarification_required":
        question = state.get("clarification_question")
        if question:
            state["messages"].append({"role": "assistant", "content": question})
        return ChatResponse(
            session_id=session_id,
            workflow_status=status,
            message="I need one more detail.",
            clarification_question=question
        )
    elif status == "no_match":
        return ChatResponse(
            session_id=session_id,
            workflow_status=status,
            message="We couldn't find a suitable provider nearby.",
            providers=[]
        )
    elif status == "completed":
        ranked = state.get("ranked_providers", [])
        formatted_providers = []
        for p in ranked:
            formatted_providers.append(ProviderResponse(
                id=p.get("provider_id") or p.get("id", ""),
                name=p.get("name", ""),
                services=p.get("services", []),
                specializations=p.get("specializations", []),
                distance_km=p.get("distance_km", 0.0),
                rating=p.get("rating", 0.0),
                price_min=p.get("price_min", 0.0),
                price_max=p.get("price_max", 0.0),
                availability_status=p.get("availability_status", "unknown"),
                availability_slots=p.get("availability_slots", []),
                verified=p.get("verified", False),
                fit_score=p.get("fit_score", 0.0),
                score_breakdown=p.get("score_breakdown", {}) if isinstance(p.get("score_breakdown"), dict) else p.get("score_breakdown", {}).model_dump() if hasattr(p.get("score_breakdown", {}), "model_dump") else {}
            ))
            
        service_info = None
        if state.get("service"):
            service_info = {
                "category": state.get("service_category", ""),
                "service": state.get("service", ""),
                "specialization": state.get("specialization", "")
            }
            
        return ChatResponse(
            session_id=session_id,
            workflow_status=status,
            message="We found providers that match your problem.",
            problem=state.get("problem"),
            service=service_info,
            providers=formatted_providers,
            recommendation=state.get("recommendation", {}).get("recommendation", state.get("recommendation", {}))
        )
    else:
        return ChatResponse(
            session_id=session_id,
            workflow_status=status,
            message="Workflow reached an unknown or error state."
        )

@router.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    if session_id in _sessions:
        del _sessions[session_id]
    return {"status": "cleared"}
