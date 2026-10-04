"""Tests for the LangGraph Orchestration Workflow."""

import pytest
from unittest.mock import patch

from backend.app.graph.workflow import build_graph
from backend.app.models.state import ServiceState


def test_text_only_complete():
    """Test Case 1: Text-only flow resulting in ready."""
    with patch("backend.app.graph.workflow.multimodal_agent") as mock_multimodal, \
         patch("backend.app.graph.workflow.problem_analyst_agent") as mock_analyst:
        
        # Multimodal should not be called
        
        def mock_analyst_behavior(state):
            return {
                "problem": {
                    "service": "ac_repair",
                    "specialization": "water_leakage",
                    "preferred_time": "today",
                    "requirements_complete": True
                }
            }
        mock_analyst.side_effect = mock_analyst_behavior
        
        graph = build_graph()
        
        initial_state: ServiceState = {
            "text_input": "My AC is leaking water and I need someone today.",
            "image_input": None,
            "transcription": None
        }
        
        result = graph.invoke(initial_state)
        
        mock_multimodal.assert_not_called()
        mock_analyst.assert_called_once()
        assert result["ready_for_discovery"] is True
        assert result["workflow_status"] == "ready_for_discovery"


def test_image_and_text():
    """Test Case 2: Text + Image goes through Multimodal Agent."""
    with patch("backend.app.graph.workflow.multimodal_agent") as mock_multimodal, \
         patch("backend.app.graph.workflow.problem_analyst_agent") as mock_analyst:
        
        def mock_multi_behavior(state):
            return {"vision_result": {"object_type": "ac"}}
        mock_multimodal.side_effect = mock_multi_behavior
        
        def mock_analyst_behavior(state):
            return {"problem": {"requirements_complete": True}}
        mock_analyst.side_effect = mock_analyst_behavior
        
        graph = build_graph()
        
        initial_state: ServiceState = {
            "text_input": "My AC is leaking.",
            "image_input": "mock-image.jpg"
        }
        
        result = graph.invoke(initial_state)
        
        mock_multimodal.assert_called_once()
        mock_analyst.assert_called_once()
        assert result["ready_for_discovery"] is True


def test_ambiguous_input():
    """Test Case 3: Ambiguous input leads to Clarification Agent."""
    with patch("backend.app.graph.workflow.problem_analyst_agent") as mock_analyst, \
         patch("backend.app.graph.workflow.clarification_agent") as mock_clarification:
        
        def mock_analyst_behavior(state):
            return {
                "problem": {"requirements_complete": False},
                "missing_information": ["machine_type"]
            }
        mock_analyst.side_effect = mock_analyst_behavior
        
        def mock_clarification_behavior(state):
            return {"clarification_question": "What type of machine?"}
        mock_clarification.side_effect = mock_clarification_behavior
        
        graph = build_graph()
        
        initial_state: ServiceState = {
            "text_input": "My machine is making noise."
        }
        
        result = graph.invoke(initial_state)
        
        mock_analyst.assert_called_once()
        mock_clarification.assert_called_once()
        assert result["workflow_status"] == "clarification_required"
        assert result["clarification_question"] == "What type of machine?"


def test_resume_after_clarification():
    """Test Case 4: Resuming with user answer resolves requirements."""
    with patch("backend.app.graph.workflow.problem_analyst_agent") as mock_analyst:
        
        def mock_analyst_behavior(state):
            return {
                "problem": {
                    "service": "washing_machine_repair",
                    "requirements_complete": True
                }
            }
        mock_analyst.side_effect = mock_analyst_behavior
        
        graph = build_graph()
        
        # Existing state from prior paused graph run
        existing_state: ServiceState = {
            "text_input": "My machine is making noise.",
            "problem": {"requirements_complete": False},
            "missing_information": ["machine_type"],
            "clarification_question": "What type of machine is having the problem?",
            "workflow_status": "clarification_required",
            "messages": [
                {"role": "user", "content": "It's my LG washing machine."}
            ]
        }
        
        result = graph.invoke(existing_state)
        
        # Workflow goes supervisor -> problem_analyst -> ready (skips multimodal because no image)
        mock_analyst.assert_called_once()
        assert result["ready_for_discovery"] is True
        assert result["workflow_status"] == "ready_for_discovery"


def test_do_not_reprocess_image():
    """Test Case 5: Do not run Multimodal again if vision_result exists."""
    with patch("backend.app.graph.workflow.multimodal_agent") as mock_multimodal, \
         patch("backend.app.graph.workflow.problem_analyst_agent") as mock_analyst:
        
        def mock_analyst_behavior(state):
            return {"problem": {"requirements_complete": True}}
        mock_analyst.side_effect = mock_analyst_behavior
        
        graph = build_graph()
        
        existing_state: ServiceState = {
            "text_input": "Fix AC.",
            "image_input": "mock.jpg",
            "vision_result": {"object_type": "ac"}  # Processed in previous turn
        }
        
        result = graph.invoke(existing_state)
        
        mock_multimodal.assert_not_called()
        mock_analyst.assert_called_once()
        assert result["ready_for_discovery"] is True


def test_agent_error_routing():
    """Test Case 6: Graph handles agent errors cleanly."""
    with patch("backend.app.graph.workflow.problem_analyst_agent") as mock_analyst:
        
        def mock_error(state):
            return {"error": "API failed."}
        mock_analyst.side_effect = mock_error
        
        graph = build_graph()
        
        state: ServiceState = {"text_input": "Help"}
        result = graph.invoke(state)
        
        assert result["workflow_status"] == "error"
        assert result["ready_for_discovery"] is False


def test_no_input():
    """Test Case 7: Graph halts with error if no input provided."""
    # Actually the problem_analyst returns an error if no input is provided
    # Let's test standard flow
    graph = build_graph()
    state: ServiceState = {}
    result = graph.invoke(state)
    assert result["workflow_status"] == "error"
