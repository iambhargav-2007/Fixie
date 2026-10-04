"""Recommendation Agent.

Explains already-ranked service providers to the user.
Does not perform ranking or querying, but generates grounded explanations based on provided facts.
"""

import json
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from backend.app.models.state import ServiceState
from backend.app.config.settings import settings

logger = logging.getLogger(__name__)


class AlternativeRecommendation(BaseModel):
    provider_id: str = Field(..., description="ID of the alternative provider")
    reason: str = Field(..., description="Why this provider is a good alternative")


class RecommendationResult(BaseModel):
    """Structured output for recommendation explanation."""
    summary: str = Field(..., description="High level summary of matches")
    top_provider_id: Optional[str] = Field(None, description="The ID of the top matched provider")
    explanation: str = Field(..., description="Fact-grounded explanation of why the top provider is a match")
    alternatives: List[AlternativeRecommendation] = Field(default_factory=list, description="List of alternative providers")


def recommendation_agent(state: ServiceState) -> dict:
    """
    Recommendation Agent node function.
    Reads problem, requirements, and ranked_providers.
    Returns a grounded recommendation explanation.
    """
    try:
        ranked_providers = state.get("ranked_providers", [])
        problem = state.get("problem", {})
        
        # 1. Empty Providers Check (No LLM Call)
        if not ranked_providers:
            logger.info("No ranked providers found. Skipping LLM call.")
            return {
                "recommendation": {
                    "summary": "No matching providers were found.",
                    "top_provider_id": None,
                    "explanation": "No providers in the current catalogue matched the requested service and location.",
                    "alternatives": []
                }
            }

        # 2. Extract top provider statically to prevent hallucinated re-ranking
        top_provider = ranked_providers[0]
        actual_top_id = top_provider.get("id")

        # 3. Build Context
        context_parts = []
        if problem:
            context_parts.append(f"USER PROBLEM:\n{json.dumps(problem, indent=2)}")
        
        context_parts.append(f"RANKED PROVIDERS DATA (Do NOT change this ranking):\n{json.dumps(ranked_providers, indent=2)}")
        
        analysis_context = "\n\n".join(context_parts)

        system_prompt = (
            "You are the Recommendation Agent for FixFind AI.\n"
            "Your job is to explain already-ranked service providers to the user.\n"
            "EXPECTED INPUT:\n"
            "- The user's parsed problem and a deterministic ranking of service providers.\n\n"
            "EXPECTED OUTPUT (Strict JSON):\n"
            "- A RecommendationResult explaining why the top provider is a match, along with potential alternatives from the list.\n\n"
            "You MUST NOT:\n"
            "- change ranking\n"
            "- calculate a new score\n"
            "- invent provider information\n"
            "- invent prices, ratings, availability, or distance\n"
            "- invent services or specializations\n\n"
            "Use ONLY the supplied provider data. If a field like 'rating' or 'availability' is missing, do not mention it.\n"
            f"The TOP provider is strictly '{actual_top_id}'. Explain why this provider matches the user's problem.\n"
            "Mention alternatives only from the remaining supplied ranked provider list, using their exact provider IDs.\n"
            "Keep the explanation concise and useful. Return structured data only."
        )

        logger.info(f"Generating recommendation explanation for {len(ranked_providers)} providers.")
        llm = settings.get_llm()

        if hasattr(llm, "with_structured_output"):
            structured_llm = llm.with_structured_output(RecommendationResult)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_context}
            ]
            response = structured_llm.invoke(messages)
            
            if isinstance(response, RecommendationResult):
                result = response
            else:
                result = RecommendationResult(**response)
            
            # Post-processing to enforce deterministic ranking and facts
            # Force the top_provider_id to match the deterministic ranking
            if result.top_provider_id != actual_top_id:
                logger.warning(f"LLM tried to change top provider to {result.top_provider_id}. Overriding to {actual_top_id}.")
                result.top_provider_id = actual_top_id
                
            # Ensure alternatives only contain IDs that were actually provided, and are not the top provider
            valid_ids = {p.get("id") for p in ranked_providers}
            filtered_alternatives = []
            for alt in result.alternatives:
                if alt.provider_id in valid_ids and alt.provider_id != actual_top_id:
                    filtered_alternatives.append(alt)
            result.alternatives = filtered_alternatives
            
            return {
                "recommendation": result.model_dump()
            }
        else:
            logger.warning("LLM does not support structured output. Skipping real execution.")
            return {"error": "LLM not properly configured for structured output."}

    except Exception as e:
        logger.error(f"Recommendation generation failed: {str(e)}")
        return {"error": "Recommendation generation failed."}
