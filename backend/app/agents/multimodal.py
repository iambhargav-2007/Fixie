"""Multimodal Understanding Agent.

This agent processes raw user inputs (text, image, voice transcription)
and returns a structured observation without diagnosing or making final decisions.
"""

import logging
from typing import Optional, List
from pydantic import BaseModel, Field

from backend.app.models.state import ServiceState
from backend.app.config.settings import settings

logger = logging.getLogger(__name__)


class VisionObservation(BaseModel):
    """Structured observation extracted from multimodal inputs."""
    object_type: Optional[str] = Field(None, description="The identified physical object (e.g., 'air_conditioner')")
    visible_issue: Optional[str] = Field(None, description="The visible or reported issue (e.g., 'water_leakage')")
    observations: List[str] = Field(default_factory=list, description="List of observed facts from image or text")
    user_description: Optional[str] = Field(None, description="Summary of the user's reported problem")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the observation extraction (0.0 to 1.0)")


def multimodal_agent(state: ServiceState) -> dict:
    """
    Multimodal Agent node function for LangGraph.
    
    Reads text, transcription, and image inputs from the state.
    Generates a structured VisionObservation.
    Updates the state with 'vision_result'.
    """
    try:
        text_input = state.get("text_input")
        image_input = state.get("image_input")
        transcription = state.get("transcription")

        # 1. Handle empty input
        if not text_input and not image_input and not transcription:
            logger.warning("No user input provided for multimodal analysis.")
            return {"error": "No user input available for multimodal analysis."}

        # 2. Build multimodal context
        context_parts = []
        if text_input:
            context_parts.append(f"USER TEXT:\n{text_input}")
        if transcription:
            context_parts.append(f"VOICE TRANSCRIPTION:\n{transcription}")
        
        multimodal_context = "\n\n".join(context_parts)
        
        logger.info("Executing multimodal analysis.")
        
        # 3. Retrieve LLM (Centralized configuration)
        llm = settings.get_llm()
        
        # 4. In a real scenario, we would format a prompt and invoke the LLM with structured output:
        # prompt = ChatPromptTemplate.from_messages([...])
        # chain = prompt | llm.with_structured_output(VisionObservation)
        # response = chain.invoke({"context": multimodal_context})
        
        # For the purpose of the foundational task, if the LLM is a mock object 
        # that has an `invoke` method returning a VisionObservation (or a dict), we call it.
        # Otherwise, if it's the default string from settings, we simulate a failure or mock it safely.
        
        if hasattr(llm, "with_structured_output"):
            # Real/LangChain Mock LLM execution path
            structured_llm = llm.with_structured_output(VisionObservation)
            system_prompt = (
                "You are the Multimodal Understanding Agent for FixFind AI.\n"
                "Your job is to analyze user-provided text, image evidence, and voice transcription.\n"
                "Identify observable objects, visible issues, and user-described symptoms.\n"
                "Do not diagnose beyond the available evidence.\n"
                "Do not invent facts.\n"
                "Do not recommend providers.\n"
                "Do not choose the final service.\n"
                "Do not assign prices.\n"
                "Do not claim certainty when evidence is weak.\n"
                "Return structured output only."
            )
            
            # Simple invocation logic (adjust based on standard LangChain patterns)
            # using structured_llm.invoke for simplicity.
            user_content = []
            if multimodal_context:
                user_content.append({"type": "text", "text": multimodal_context})
            if image_input:
                user_content.append({"type": "image_url", "image_url": {"url": image_input}})
                
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            try:
                response = structured_llm.invoke(messages)
                if isinstance(response, VisionObservation):
                    result_dict = response.model_dump()
                else:
                    # Fallback if it returns dict
                    result_dict = response
                return {"vision_result": result_dict}
            except Exception as e:
                logger.warning(f"OpenRouter API failed (likely rate limit or model format issue), falling back: {e}")
                return {"vision_result": None}
            
        else:
            # Fallback for when the settings LLM is just a placeholder string during early development
            logger.warning("LLM does not support structured output. Skipping real execution.")
            return {"error": "LLM not properly configured for structured output."}

    except Exception as e:
        logger.error(f"Multimodal analysis failed: {str(e)}")
        return {"error": "Multimodal analysis failed."}
