"""Tests for the Clarification Agent."""

import pytest
from unittest.mock import patch

from backend.app.agents.clarification import clarification_agent, ClarificationResult
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


def test_machine_type():
    """Test 1: Asks for machine type."""
    mock_response = ClarificationResult(
        clarification_question="What type of machine is having the problem?",
        target_information="machine_type"
    )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(mock_response)):
        state: ServiceState = {
            "missing_information": ["machine_type"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        assert result.get("clarification_question") is not None
        assert result.get("target_information") == "machine_type"


def test_preferred_time():
    """Test 2: Asks for preferred time."""
    mock_response = ClarificationResult(
        clarification_question="When would you like the technician to come?",
        target_information="preferred_time"
    )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(mock_response)):
        state: ServiceState = {
            "problem": {"service": "ac_repair"},
            "missing_information": ["preferred_time"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        assert result.get("target_information") == "preferred_time"


def test_location():
    """Test 3: Asks for location."""
    mock_response = ClarificationResult(
        clarification_question="Where should we look for a provider?",
        target_information="location"
    )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(mock_response)):
        state: ServiceState = {
            "missing_information": ["location"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        assert result.get("target_information") == "location"


def test_multiple_missing_fields():
    """Test 4: Prioritizes and asks ONE question."""
    mock_response = ClarificationResult(
        clarification_question="What type of machine is it?",
        target_information="machine_type"
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "missing_information": ["location", "preferred_time", "machine_type"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        assert result.get("target_information") == "machine_type"
        
        # Verify the context sent to LLM focused on machine_type
        last_messages = mock_llm.structured_llm.last_messages
        context_content = last_messages[1]["content"]
        assert "TARGET MISSING INFORMATION TO ASK ABOUT: machine_type" in context_content


def test_already_answered():
    """Test 5: Does not ask if already answered."""
    # LLM infers it's already answered, returns nulls
    mock_response = ClarificationResult(
        clarification_question=None,
        target_information=None
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "messages": [
                {"role": "user", "content": "I have an LG washing machine."}
            ],
            "missing_information": ["machine_type"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        assert result.get("clarification_question") is None
        assert result.get("target_information") is None


def test_complete_requirements():
    """Test 6: No LLM call if requirements complete."""
    # We don't mock LLM return. If it tries to invoke, it will crash.
    state: ServiceState = {
        "missing_information": [],
        "requirements_complete": True
    }
    result = clarification_agent(state)
    
    assert result.get("clarification_question") is None
    assert result.get("target_information") is None


def test_llm_failure():
    """Test 7: Handles LLM failure gracefully."""
    class CrashingLLM:
        def with_structured_output(self, schema):
            raise ValueError("Network Error")

    with patch("backend.app.config.settings.Settings.get_llm", return_value=CrashingLLM()):
        state: ServiceState = {
            "missing_information": ["location"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        assert "error" in result
        assert result["error"] == "Clarification generation failed."


def test_context_preservation():
    """Test 8: Uses previous problem context to make question specific."""
    mock_response = ClarificationResult(
        clarification_question="When would you like the AC technician to come?",
        target_information="preferred_time"
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "messages": [
                {"role": "user", "content": "My AC is leaking."}
            ],
            "problem": {
                "service": "ac_repair"
            },
            "missing_information": ["preferred_time"],
            "requirements_complete": False
        }
        result = clarification_agent(state)
        
        last_messages = mock_llm.structured_llm.last_messages
        context_content = last_messages[1]["content"]
        
        assert "CURRENT PROBLEM SUMMARY" not in context_content # Since it wasn't provided in state, but service was
        assert "SERVICE IDENTIFIED SO FAR: ac_repair" in context_content
        assert "USER: My AC is leaking." in context_content
        assert "TARGET MISSING INFORMATION TO ASK ABOUT: preferred_time" in context_content
        
        assert result.get("clarification_question") == "When would you like the AC technician to come?"
