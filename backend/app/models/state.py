"""Shared LangGraph Agent State Contract for FixFind AI."""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class ServiceState(TypedDict, total=False):
    """Core state object passed across agents in the LangGraph workflow.

    Defines the shared data contract between the Supervisor, Multimodal,
    Problem Analyst, Clarification, and Recommendation agents.
    """

    # Session & Conversational Context
    session_id: str
    messages: List[Dict[str, Any]]

    # Multimodal Inputs
    text_input: Optional[str]
    image_input: Optional[str]
    audio_input: Optional[str]
    transcription: Optional[str]

    # Geospatial Context
    location: Optional[Dict[str, float]]  # e.g., {"lat": 17.385, "lng": 78.486}

    # AI Diagnostics & Analysis
    vision_result: Optional[Dict[str, Any]]
    problem: Optional[Dict[str, Any]]
    requirements: Optional[Dict[str, Any]]

    # Clarification Engine
    missing_information: Optional[List[str]]
    clarification_question: Optional[str]

    # Service Classification
    service_category: Optional[str]

    # Provider Discovery & Ranking (Deterministic Provider Engine)
    candidate_providers: Optional[List[Dict[str, Any]]]
    ranked_providers: Optional[List[Dict[str, Any]]]

    # AI Recommendation & Explanation
    recommendation: Optional[Dict[str, Any]]

    # Booking & Request
    selected_provider: Optional[Dict[str, Any]]
    service_request: Optional[Dict[str, Any]]
