"""Shared LangGraph Agent State Contract for FixFind AI."""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class ServiceState(TypedDict, total=False):
    """Core state object passed across agents in the LangGraph workflow."""

    session_id: str
    messages: list

    text_input: Optional[str]
    image_input: Optional[str]
    audio_input: Optional[str]
    transcription: Optional[str]

    location: Optional[Dict[str, float]]

    vision_result: Optional[dict]
    problem: Optional[dict]
    requirements: Optional[dict]

    missing_information: list
    clarification_question: Optional[str]

    service_category: Optional[str]
    service: Optional[str]
    specialization: Optional[str]

    candidate_providers: list
    ranked_providers: list

    recommendation: Optional[dict]

    selected_provider: Optional[dict]
    service_request: Optional[dict]

    error: Optional[str]

    # Orchestration & Workflow State
    ready_for_discovery: bool
    workflow_status: Optional[str]
