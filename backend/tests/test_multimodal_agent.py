"""Tests for the Multimodal Understanding Agent."""

import pytest
from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from backend.app.agents.multimodal import multimodal_agent, VisionObservation
from backend.app.models.state import ServiceState


class MockStructuredLLM:
    def __init__(self, expected_response):
        self.expected_response = expected_response
        self.last_messages = None

    def invoke(self, messages):
        self.last_messages = messages
        return self.expected_response


class MockLLM:
    def __init__(self, expected_response):
        self.structured_llm = MockStructuredLLM(expected_response)

    def with_structured_output(self, schema):
        return self.structured_llm


@pytest.fixture
def mock_llm_setup():
    mock_response = VisionObservation(
        object_type="air_conditioner",
        visible_issue="water_leakage",
        observations=["water visible near indoor unit"],
        user_description="AC is leaking",
        confidence=0.9
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        yield mock_llm


def test_text_only(mock_llm_setup):
    """Test 1: Text only input produces structured output."""
    state: ServiceState = {
        "text_input": "My AC is leaking water."
    }
    
    result = multimodal_agent(state)
    
    assert "vision_result" in result
    assert result["vision_result"]["object_type"] == "air_conditioner"
    assert result["vision_result"]["confidence"] == 0.9

    # Verify context sent to LLM
    last_messages = mock_llm_setup.structured_llm.last_messages
    context_content = last_messages[1]["content"]
    assert "USER TEXT:" in context_content
    assert "My AC is leaking water." in context_content
    assert "IMAGE:" not in context_content


def test_text_and_image(mock_llm_setup):
    """Test 2: Text + image are passed correctly into the agent context."""
    state: ServiceState = {
        "text_input": "My AC is leaking water.",
        "image_input": "http://example.com/ac_leak.jpg"
    }
    
    result = multimodal_agent(state)
    
    assert "vision_result" in result
    
    last_messages = mock_llm_setup.structured_llm.last_messages
    context_content = last_messages[1]["content"]
    
    assert "USER TEXT:" in context_content
    assert "IMAGE:" in context_content
    assert "http://example.com/ac_leak.jpg" in context_content


def test_voice_transcription(mock_llm_setup):
    """Test 3: Voice transcription is included in model context."""
    state: ServiceState = {
        "transcription": "The refrigerator is not cooling."
    }
    
    result = multimodal_agent(state)
    
    assert "vision_result" in result
    
    last_messages = mock_llm_setup.structured_llm.last_messages
    context_content = last_messages[1]["content"]
    
    assert "VOICE TRANSCRIPTION:" in context_content
    assert "The refrigerator is not cooling." in context_content


def test_empty_input(mock_llm_setup):
    """Test 4: Empty input returns controlled error and skips LLM call."""
    state: ServiceState = {
        "text_input": None,
        "image_input": None,
        "transcription": None
    }
    
    result = multimodal_agent(state)
    
    assert "error" in result
    assert result["error"] == "No user input available for multimodal analysis."
    assert "vision_result" not in result
    
    # LLM should not have been invoked
    assert mock_llm_setup.structured_llm.last_messages is None


def test_invalid_confidence():
    """Test 5: Verify invalid confidence values are rejected by the schema."""
    with pytest.raises(ValidationError):
        VisionObservation(
            object_type="air_conditioner",
            visible_issue="water_leakage",
            observations=["water visible near indoor unit"],
            user_description="AC is leaking",
            confidence=1.5  # Invalid, must be <= 1.0
        )
        
    with pytest.raises(ValidationError):
        VisionObservation(
            object_type="air_conditioner",
            visible_issue="water_leakage",
            observations=["water visible near indoor unit"],
            user_description="AC is leaking",
            confidence=-0.1  # Invalid, must be >= 0.0
        )


def test_llm_failure_handling():
    """Verify that exceptions during LLM execution are caught and state is returned gracefully."""
    class CrashingLLM:
        def with_structured_output(self, schema):
            raise ValueError("API Timeout")

    with patch("backend.app.config.settings.Settings.get_llm", return_value=CrashingLLM()):
        state: ServiceState = {"text_input": "My AC is broken."}
        result = multimodal_agent(state)
        
        assert "error" in result
        assert result["error"] == "Multimodal analysis failed."
