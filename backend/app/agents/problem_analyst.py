"""Problem Analyst Agent.

Analyzes raw input and multimodal observations to infer service requirements, 
problem category, missing information, and readiness for provider discovery.
"""

import json
import logging
import os
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from backend.app.models.state import ServiceState
from backend.app.config.settings import settings

logger = logging.getLogger(__name__)

# Load valid services from seed
SEED_PATH = os.path.join(os.path.dirname(__file__), "../../../seed/services.json")
VALID_SERVICES = set()
VALID_CATEGORIES = set()
try:
    with open(SEED_PATH, "r") as f:
        services_data = json.load(f)
        for category in services_data:
            VALID_CATEGORIES.add(category["category"])
            for svc in category["services"]:
                VALID_SERVICES.add(svc["id"])
except Exception as e:
    logger.error(f"Failed to load service catalog: {e}")


class ProblemAnalysis(BaseModel):
    """Structured output for problem analysis."""
    problem_summary: str = Field(..., description="Summary of the user's problem")
    object: Optional[str] = Field(None, description="The physical object/appliance involved (e.g., 'AC', 'washing machine')")
    issue_summary: Optional[str] = Field(None, description="Short summary of the specific issue (e.g., 'water leakage from indoor unit')")
    urgency_level: Optional[str] = Field(None, description="Urgency: 'Low', 'Medium', or 'High'")
    service_category: Optional[str] = Field(None, description="The broad category of service needed (e.g., 'Appliance Repair', 'Home Maintenance')")
    service: Optional[str] = Field(None, description="The specific service required (e.g., 'ac_repair', 'plumbing', 'electrical', 'carpentry', 'home_cleaning'). Do not restrict to these examples; extract the most accurate service name based on the problem.")
    specialization: Optional[str] = Field(None, description="The specific problem specialization (e.g., 'water_leakage')")
    urgency: Optional[str] = Field(None, description="Urgency: 'low', 'medium', or 'high'")
    preferred_time: Optional[str] = Field(None, description="The user's requested timing (e.g., 'today')")
    requirements: Dict[str, Any] = Field(default_factory=dict, description="Key attributes required for provider search")
    missing_information: List[str] = Field(default_factory=list, description="List of missing information preventing search")
    requirements_complete: bool = Field(False, description="True if sufficient information exists to search providers")
    confidence: float = Field(0.0, description="Confidence in the analysis (0.0 to 1.0)")


def problem_analyst_agent(state: ServiceState) -> dict:
    """
    Problem Analyst Agent node function.
    Reads user input, multimodal vision_result, and location.
    Updates the state with problem, requirements, service_category, missing_information, etc.
    """
    try:
        text_input = state.get("text_input")
        transcription = state.get("transcription")
        vision_result = state.get("vision_result")
        location = state.get("location")

        if not text_input and not transcription and not vision_result:
            logger.warning("Insufficient input for problem analysis.")
            return {"error": "Insufficient input for problem analysis."}

        messages = state.get("messages", [])

        # Combine context
        context_parts = []
        
        # Add conversation history
        history_str = ""
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_str += f"{role.upper()}: {content}\n"
        if history_str:
            context_parts.append(f"CONVERSATION HISTORY:\n{history_str}")
            
        if text_input:
            context_parts.append(f"USER TEXT: {text_input}")
        if transcription:
            context_parts.append(f"TRANSCRIPTION: {transcription}")
        if vision_result:
            context_parts.append(f"MULTIMODAL OBSERVATION: {json.dumps(vision_result, indent=2)}")
        if location:
            locality = location.get("locality", "Unknown")
            context_parts.append(f"LOCATION: System has detected user location as '{locality}'. Do NOT ask the user for their location.")
        else:
            context_parts.append("LOCATION: Not provided.")

        analysis_context = "\n\n".join(context_parts)
        
        valid_services_str = ", ".join(VALID_SERVICES)

        system_prompt = (
            "You are the Problem Analyst Agent for FixFind AI.\n"
            "Your job is to transform user-described problems and multimodal observations into structured service requirements.\n"
            "EXPECTED INPUT:\n"
            "- A conversational history containing the user's problem description, plus optional multimodal observations.\n\n"
            "EXPECTED OUTPUT (Strict JSON):\n"
            "- A structured ProblemAnalysis object that extracts the problem, relevant service category/name, urgency, and identifies any 'missing_information' preventing a search.\n\n"
            "You must:\n"
            "- extract urgency ('low', 'medium', 'high')\n"
            "- extract preferred timing\n"
            "- identify missing information (ONLY ask for missing details about the PROBLEM or SERVICE. Do NOT ask for location/address unless explicitly stated as 'Not provided' in context)\n"
            "- determine whether requirements are complete\n\n"
            f"Examples of services include: {valid_services_str}\n"
            "However, you are NOT restricted to these. Infer the most accurate service category and service name.\n\n"
            "You must:\n"
            "- use evidence from the user and multimodal analysis\n"
            "- avoid unsupported assumptions\n"
            "- never invent provider information\n"
            "- never invent prices, ratings, availability, or distance\n"
            "- never claim an exact mechanical cause without evidence\n"
            "Return structured data only."
        )

        logger.info("Executing problem analysis.")
        llm = settings.get_llm()

        if hasattr(llm, "with_structured_output"):
            try:
                structured_llm = llm.with_structured_output(ProblemAnalysis, method="function_calling")
            except Exception:
                structured_llm = llm.with_structured_output(ProblemAnalysis)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_context}
            ]
            try:
                response = structured_llm.invoke(messages)
                if isinstance(response, ProblemAnalysis):
                    result = response
                else:
                    result = ProblemAnalysis(**response)
            except Exception as e:
                logger.warning(f"OpenRouter API failed in problem_analyst, falling back: {e}")
                # Provide a basic fallback so the frontend renders successfully
                return {
                    "problem": {
                        "problem_summary": str(text_input),
                        "object": "Unknown",
                        "issue_summary": "System error analyzing problem",
                        "urgency_level": "Medium"
                    },
                    "requirements": {},
                    "service_category": "appliances",
                    "service": "ac_repair",
                    "specialization": "general",
                    "missing_information": ["location"],
                    "requirements_complete": False
                }
            
            # Post-processing validation
            if result.service and result.service not in VALID_SERVICES:
                # Unsupported service hallucinated by LLM
                result.service = None
                result.requirements_complete = False
                result.missing_information.append("unsupported_service")

            # Add location availability requirement
            if location:
                result.requirements["location_available"] = True
            elif result.requirements_complete:
                # Typically we need location to find a provider
                result.requirements_complete = False
                if "location" not in result.missing_information:
                    result.missing_information.append("location")
                    
            # Ensure consistency between missing_information and requirements_complete
            if not result.service and "service" not in result.missing_information:
                result.missing_information.append("service")
            
            if not result.missing_information and result.service:
                result.requirements_complete = True

            # Return partial state updates
            return {
                "problem": result.model_dump(),
                "requirements": result.requirements,
                # Write service/specialization to top-level state for downstream nodes
                "service_category": result.service_category,
                "service": result.service,
                "specialization": result.specialization,
                "missing_information": result.missing_information
            }
        else:
            logger.warning("LLM does not support structured output. Skipping real execution.")
            return {"error": "LLM not properly configured for structured output."}

    except Exception as e:
        logger.error(f"Problem analysis failed: {str(e)}")
        return {"error": "Problem analysis failed."}
