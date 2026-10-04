"""LangGraph workflow definition and state graph orchestration builder."""

import logging
from langgraph.graph import StateGraph, START, END

from backend.app.models.state import ServiceState
from backend.app.agents.multimodal import multimodal_agent
from backend.app.agents.problem_analyst import problem_analyst_agent
from backend.app.agents.clarification import clarification_agent
from backend.app.agents.recommendation import recommendation_agent
from backend.app.services.service_catalogue import ServiceCatalogue
from backend.app.services.discovery_service import DiscoveryService, DiscoveryRequirement
from backend.app.services.ranking_service import MatchingEngine

logger = logging.getLogger(__name__)


def supervisor_node(state: ServiceState) -> dict:
    """Supervisor node validates state and marks workflow as analyzing."""
    logger.info("Supervisor node executing.")
    # In a real app we might validate session_id or other fields.
    if state.get("error"):
        return {"workflow_status": "error"}
    return {"workflow_status": "analyzing"}


def check_multimodal_needed(state: ServiceState) -> str:
    """Deterministic routing from supervisor to either Multimodal or Problem Analyst."""
    if state.get("error"):
        return "error"
        
    image_input = state.get("image_input")
    vision_result = state.get("vision_result")
    
    # Process if there is an image, but it hasn't been processed yet
    if image_input and not vision_result:
        logger.info("Routing to Multimodal Agent.")
        return "multimodal"
        
    logger.info("Routing to Problem Analyst.")
    return "problem_analyst"


def route_after_analysis(state: ServiceState) -> str:
    """Deterministic routing after the Problem Analyst."""
    if state.get("error"):
        return "error"
        
    if state.get("is_relevant") is False:
        logger.info("Irrelevant query detected.")
        return "irrelevant_topic"
        
    if state.get("problem", {}).get("requirements_complete"):
        logger.info("Requirements complete. Routing to validation.")
        return "validate_service"
        
    logger.info("Requirements incomplete. Routing to clarification.")
    return "clarification"


def validate_service_node(state: ServiceState) -> dict:
    """Validate service with Service Catalogue."""
    problem = state.get("problem", {})
    service = problem.get("service")
    specialization = problem.get("specialization")
    category = problem.get("service_category")
    
    catalogue = ServiceCatalogue()
    result = catalogue.validate(service_category=category, service=service, specialization=specialization)
    
    if not result.valid:
        # We could route to clarification, but for now just fail or ask for clarification
        return {
            "error": result.reason,
            "workflow_status": "error"
        }
    
    return {
        "service_category": result.service_category,
        "service": result.service,
        "specialization": result.specialization
    }

def provider_discovery_node(state: ServiceState) -> dict:
    """Discover candidates."""
    service = state.get("service")
    specialization = state.get("specialization")
    loc = state.get("location")
    
    if not service or not loc:
        return {"error": "Missing service or location", "workflow_status": "error"}
        
    req = DiscoveryRequirement(
        service=service,
        specialization=specialization,
        location=loc,
        preferred_time=state.get("requirements", {}).get("preferred_time")
    )
    
    ds = DiscoveryService()
    candidates = ds.discover(req)
    
    # Store candidates as dicts in state since they are Pydantic models
    # Wait, the state doesn't need to be JSON serializable here, but let's dump them to dicts
    return {
        "candidate_providers": [c.model_dump() for c in candidates]
    }

def check_after_discovery(state: ServiceState) -> str:
    if state.get("error"):
        return "error"
    if not state.get("candidate_providers"):
        return "no_match"
    return "match"

def no_match_node(state: ServiceState) -> dict:
    return {
        "workflow_status": "no_match",
        "candidate_providers": [],
        "ranked_providers": []
    }

def matching_node(state: ServiceState) -> dict:
    """Rank candidates."""
    from backend.app.services.discovery_service import DiscoveredProvider
    
    candidates_dicts = state.get("candidate_providers", [])
    candidates = [DiscoveredProvider(**c) for c in candidates_dicts]
    
    service = state.get("service")
    specialization = state.get("specialization")
    loc = state.get("location")
    req = DiscoveryRequirement(
        service=service,
        specialization=specialization,
        location=loc,
        preferred_time=state.get("requirements", {}).get("preferred_time")
    )
    
    me = MatchingEngine()
    result = me.match(req, candidates)
    
    return {
        "ranked_providers": [p.model_dump() for p in result.providers],
        "workflow_status": "providers_found" if result.providers else "no_match"
    }

def set_completed(state: ServiceState) -> dict:
    return {"workflow_status": "completed"}


def set_clarification(state: ServiceState) -> dict:
    """Node that sets clarification status after Clarification Agent runs."""
    return {
        "workflow_status": "clarification_required"
    }


def handle_error(state: ServiceState) -> dict:
    """Terminal node for errors."""
    return {
        "workflow_status": "error",
        "ready_for_discovery": False
    }

def irrelevant_topic_node(state: ServiceState) -> dict:
    """Handles off-topic or irrelevant questions."""
    return {
        "workflow_status": "irrelevant",
        "clarification_question": "Please ask relevant questions like repair works related to mechanical and electrical to the system."
    }


def check_clarification_error(state: ServiceState) -> str:
    """Check if clarification agent threw an error."""
    if state.get("error"):
        return "error"
    return "set_clarification"


def build_graph():
    """Constructs and returns the compiled LangGraph workflow."""
    logger.info("Building LangGraph workflow.")
    
    workflow = StateGraph(ServiceState)
    
    # Add all nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("multimodal_agent", multimodal_agent)
    workflow.add_node("problem_analyst", problem_analyst_agent)
    workflow.add_node("clarification_agent", clarification_agent)
    
    workflow.add_node("validate_service", validate_service_node)
    workflow.add_node("provider_discovery", provider_discovery_node)
    workflow.add_node("matching", matching_node)
    workflow.add_node("recommendation", recommendation_agent)
    workflow.add_node("no_match", no_match_node)
    
    # Helper nodes to update final state status before END
    workflow.add_node("set_completed", set_completed)
    workflow.add_node("set_clarification", set_clarification)
    workflow.add_node("handle_error", handle_error)
    workflow.add_node("irrelevant_topic", irrelevant_topic_node)
    
    # Construct edges
    workflow.add_edge(START, "supervisor")
    
    # From supervisor, condition: do we need multimodal?
    workflow.add_conditional_edges(
        "supervisor",
        check_multimodal_needed,
        {
            "multimodal": "multimodal_agent",
            "problem_analyst": "problem_analyst",
            "error": "handle_error"
        }
    )
    
    # From multimodal to problem analyst (or error)
    def check_multimodal_error(state):
        return "error" if state.get("error") else "problem_analyst"
        
    workflow.add_conditional_edges(
        "multimodal_agent",
        check_multimodal_error,
        {
            "problem_analyst": "problem_analyst",
            "error": "handle_error"
        }
    )
    
    # From problem analyst, condition: is analysis complete?
    workflow.add_conditional_edges(
        "problem_analyst",
        route_after_analysis,
        {
            "validate_service": "validate_service",
            "clarification": "clarification_agent",
            "irrelevant_topic": "irrelevant_topic",
            "error": "handle_error"
        }
    )
    
    def check_validation(state):
        return "error" if state.get("error") else "provider_discovery"

    workflow.add_conditional_edges("validate_service", check_validation, {"error": "handle_error", "provider_discovery": "provider_discovery"})
    workflow.add_conditional_edges("provider_discovery", check_after_discovery, {"error": "handle_error", "no_match": "no_match", "match": "matching"})
    
    def check_matching(state):
        return "recommendation" if state.get("ranked_providers") else "no_match"
        
    workflow.add_conditional_edges("matching", check_matching, {"recommendation": "recommendation", "no_match": "no_match"})
    workflow.add_edge("recommendation", "set_completed")
    
    # From clarification agent to status node
    workflow.add_conditional_edges(
        "clarification_agent",
        check_clarification_error,
        {
            "set_clarification": "set_clarification",
            "error": "handle_error"
        }
    )
    
    # Connect status nodes to END
    workflow.add_edge("set_completed", END)
    workflow.add_edge("no_match", END)
    workflow.add_edge("set_clarification", END)
    workflow.add_edge("handle_error", END)
    workflow.add_edge("irrelevant_topic", END)
    
    # Compile the graph
    return workflow.compile()
