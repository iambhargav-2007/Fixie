"""Clarification Agent.

Analyzes missing information from the Problem Analyst and generates a single,
concise clarification question to ask the user.
"""

import logging
from typing import Optional, List
from pydantic import BaseModel, Field

from backend.app.models.state import ServiceState
from backend.app.config.settings import settings

logger = logging.getLogger(__name__)


class ClarificationResult(BaseModel):
    """Structured output for clarification generation."""
    clarification_question: Optional[str] = Field(None, description="The single question to ask the user.")
    target_information: Optional[str] = Field(None, description="The specific field/concept being asked about.")
    reasoning: Optional[str] = Field(None, description="A brief explanation of WHY you need this information to find the right provider.")


def get_priority_missing_field(missing_information: List[str]) -> Optional[str]:
    """
    Selects the most important missing field to ask about based on a fixed priority.
    """
    if not missing_information:
        return None

    priority_list = [
        "object",
        "equipment",
        "machine_type",
        "type_of_machine",
        "issue",
        "problem",
        "symptom",
        "service",
        "service_category",
        "location",
        "preferred_time",
        "urgency"
    ]

    for p in priority_list:
        # Match exactly or as a substring if reasonably close
        for missing in missing_information:
            if p in missing.lower():
                return missing

    # Fallback: just return the first one if none matched priority
    return missing_information[0]


def clarification_agent(state: ServiceState) -> dict:
    """
    Clarification Agent node function.
    Reads missing_information, problem, and messages from state.
    Generates a clarification_question.
    Updates the state.
    """
    try:
        missing_info = state.get("missing_information", [])
        requirements_complete = state.get("requirements_complete", False)
        
        # 1. Complete requirements check
        if requirements_complete or not missing_info:
            logger.info("Requirements complete. No clarification needed.")
            return {
                "clarification_question": None,
                "target_information": None
            }

        # 2. Prioritize ONE missing field
        target_info = get_priority_missing_field(missing_info)
        if not target_info:
            return {
                "clarification_question": None,
                "target_information": None
            }

        # 3. Prevent duplicate questions by checking existing context
        messages = state.get("messages", [])
        text_input = state.get("text_input", "")
        problem_summary = state.get("problem", {}).get("problem_summary", "")
        service_identified = state.get("problem", {}).get("service", "")
        
        # Combine context
        context_parts = []
        if problem_summary:
            context_parts.append(f"CURRENT PROBLEM SUMMARY: {problem_summary}")
        if service_identified:
            context_parts.append(f"SERVICE IDENTIFIED SO FAR: {service_identified}")
        
        # Add conversation history
        history_str = ""
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_str += f"{role.upper()}: {content}\n"
        
        if history_str:
            context_parts.append(f"CONVERSATION HISTORY:\n{history_str}")
        elif text_input:
            context_parts.append(f"USER TEXT: {text_input}")

        context_parts.append(f"TARGET MISSING INFORMATION TO ASK ABOUT: {target_info}")
        
        analysis_context = "\n\n".join(context_parts)

        system_prompt = (
            "You are the Clarification Agent for FixFind AI.\n"
            "Your job is to ask the user one concise question when required information is missing.\n\n"
            "EXPECTED INPUT:\n"
            "- The current problem analysis and the user's conversation history.\n"
            "- A 'TARGET MISSING INFORMATION' field specifying exactly what needs to be asked.\n\n"
            "EXPECTED OUTPUT (Strict JSON):\n"
            "- A ClarificationResult object containing a single, concise 'clarification_question', the 'target_information' it addresses, and 'reasoning' (a brief explanation of why this info is needed).\n\n"
            "You must ask about the 'TARGET MISSING INFORMATION' specified in the context and explain why it's necessary.\n"
            "Ask only ONE short, natural question. Avoid technical jargon.\n\n"
            "IMPORTANT: If the user has ALREADY provided the answer in the conversation history, "
            "do NOT ask the question again. Instead, return null for both fields.\n"
            "Do not solve the problem yourself or recommend providers.\n"
            "Return structured data only."
        )

        logger.info(f"Generating clarification for missing info: {target_info}")
        llm = settings.get_llm()

        if hasattr(llm, "with_structured_output"):
            try:
                structured_llm = llm.with_structured_output(ClarificationResult, method="function_calling")
            except Exception:
                structured_llm = llm.with_structured_output(ClarificationResult)
            llm_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_context}
            ]
            response = structured_llm.invoke(llm_messages)
            
            if isinstance(response, ClarificationResult):
                result = response
            else:
                result = ClarificationResult(**response)
            
            return {
                "clarification_question": result.clarification_question,
                "clarification_reasoning": result.reasoning,
                # Output the target info we asked about, or None if the LLM deemed it already answered
                "target_information": result.target_information if result.clarification_question else None
            }
        else:
            logger.warning("LLM does not support structured output. Skipping real execution.")
            return {"error": "LLM not properly configured for structured output."}

    except Exception as e:
        logger.error(f"Clarification generation failed: {str(e)}")
        return {"error": "Clarification generation failed."}
