"""Tests for the agentic foundation and initial LangGraph workflow."""

import pytest
from backend.app.graph.workflow import build_graph
from backend.app.config.settings import settings


def test_graph_construction():
    """Test 1: The graph can be constructed."""
    graph = build_graph()
    assert graph is not None
    # We should be able to get the compiled graph.
    assert hasattr(graph, "invoke")


def test_graph_invocation_and_state():
    """Test 2, 3, 4: Invoke graph, check state fields, and ensure it reaches END."""
    from unittest.mock import patch, MagicMock
    from backend.app.agents.problem_analyst import ProblemAnalysis

    graph = build_graph()
    
    # Test 2 payload
    initial_state = {
        "session_id": "TEST001",
        "messages": [],
        "text_input": "My AC is leaking",
        "image_input": None,
        "audio_input": None,
        "transcription": None,
        "location": {
            "lat": 17.385,
            "lng": 78.486
        }
    }
    
    class MockLLM:
        def with_structured_output(self, schema):
            mock = MagicMock()
            if schema == ProblemAnalysis:
                mock.invoke.return_value = ProblemAnalysis(
                    problem_summary="AC leak",
                    requirements_complete=True,
                    confidence=0.9
                )
            return mock

    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM()):
        result = graph.invoke(initial_state)
    
    # Test 3: The resulting state contains the expected fields.
    assert "session_id" in result
    assert result["session_id"] == "TEST001"
    assert "messages" in result
    assert result["messages"] == []
    assert "text_input" in result
    assert result["text_input"] == "My AC is leaking"
    assert "location" in result
    assert result["location"]["lat"] == 17.385
    
    # Check that error is not set or is None
    assert result.get("error") is None

    # Test 4: The graph reaches the END state successfully.
    # By successfully returning from invoke without exceptions and having the expected outputs,
    # it indicates it processed the START -> initialize_state -> END flow.


def test_llm_abstraction():
    """Test that the LLM abstraction exists and doesn't crash."""
    llm = settings.get_llm()
    assert llm is not None
