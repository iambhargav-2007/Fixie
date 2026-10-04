"""Tests for the Problem Analyst Agent."""

import pytest
from unittest.mock import patch, MagicMock

from backend.app.agents.problem_analyst import problem_analyst_agent, ProblemAnalysis
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


def test_ac_leakage():
    """Test 1: AC Leakage produces expected service and specialization."""
    mock_response = ProblemAnalysis(
        problem_summary="AC is leaking water.",
        service_category="Appliance Repair",
        service="ac_repair",
        specialization="water_leakage",
        urgency="medium",
        preferred_time=None,
        requirements={"object": "air_conditioner", "issue": "water_leakage"},
        missing_information=[],
        requirements_complete=True,
        confidence=0.9
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "text_input": "My AC is leaking water.",
            "location": {"lat": 17.385, "lng": 78.486},
            "vision_result": {
                "object_type": "air_conditioner",
                "visible_issue": "water_leakage"
            }
        }
        
        result = problem_analyst_agent(state)
        
        assert "problem" in result
        assert result["problem"]["service"] == "ac_repair"
        assert result["problem"]["specialization"] == "water_leakage"
        assert result["requirements"].get("location_available") is True


def test_refrigerator():
    """Test 2: Refrigerator issue maps to refrigerator_repair."""
    mock_response = ProblemAnalysis(
        problem_summary="Refrigerator is not cooling.",
        service_category="Appliance Repair",
        service="refrigerator_repair",
        specialization="cooling_issue",
        urgency="medium",
        preferred_time=None,
        requirements={"object": "refrigerator", "issue": "not_cooling"},
        missing_information=[],
        requirements_complete=True,
        confidence=0.9
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "text_input": "My refrigerator is not cooling.",
            "location": {"lat": 17.0, "lng": 78.0}
        }
        result = problem_analyst_agent(state)
        assert result["problem"]["service"] == "refrigerator_repair"


def test_ambiguous_problem():
    """Test 3: Ambiguous problem missing information."""
    mock_response = ProblemAnalysis(
        problem_summary="User reports a noisy machine.",
        service_category=None,
        service=None,
        specialization=None,
        urgency=None,
        preferred_time=None,
        requirements={},
        missing_information=["type_of_machine"],
        requirements_complete=False,
        confidence=0.4
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "text_input": "My machine is making noise.",
            "location": {"lat": 17.0, "lng": 78.0}
        }
        result = problem_analyst_agent(state)
        assert result["problem"]["requirements_complete"] is False
        assert "type_of_machine" in result["missing_information"]


def test_preferred_time():
    """Test 4: Preferred time extracted correctly."""
    mock_response = ProblemAnalysis(
        problem_summary="AC leaking, needs fix today.",
        service_category="Appliance Repair",
        service="ac_repair",
        specialization="water_leakage",
        urgency="high",
        preferred_time="today",
        requirements={"object": "air_conditioner"},
        missing_information=[],
        requirements_complete=True,
        confidence=0.9
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "text_input": "My AC is leaking and I need someone today.",
            "location": {"lat": 17.0, "lng": 78.0}
        }
        result = problem_analyst_agent(state)
        assert result["problem"]["preferred_time"] == "today"


def test_location():
    """Test 5: Location provided updates requirements."""
    def get_mock_response():
        return ProblemAnalysis(
            problem_summary="Fan repair",
            service_category="Electrical",
            service="fan_repair",
            specialization="noise",
            urgency="low",
            preferred_time=None,
            requirements={},
            missing_information=[],
            requirements_complete=True,
            confidence=0.9
        )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(get_mock_response())):
        # Without location, should append missing info
        state_no_loc: ServiceState = {"text_input": "Fix fan."}
        res_no_loc = problem_analyst_agent(state_no_loc)
        assert "location" in res_no_loc["missing_information"]
        assert res_no_loc["problem"]["requirements_complete"] is False

    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(get_mock_response())):
        # With location, requirements_complete is maintained
        state_loc: ServiceState = {"text_input": "Fix fan.", "location": {"lat": 1, "lng": 1}}
        res_loc = problem_analyst_agent(state_loc)
        assert res_loc["requirements"].get("location_available") is True
        assert res_loc["problem"]["requirements_complete"] is True


def test_unsupported_service():
    """Test 6: Unsupported service name is rejected."""
    # LLM hallucinates an unsupported service 'rocket_repair'
    mock_response = ProblemAnalysis(
        problem_summary="Rocket needs fixing.",
        service_category="Aerospace",
        service="rocket_repair",
        specialization="thruster",
        urgency="high",
        preferred_time=None,
        requirements={},
        missing_information=[],
        requirements_complete=True,
        confidence=0.9
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "text_input": "My rocket is broken.",
            "location": {"lat": 17.0, "lng": 78.0}
        }
        result = problem_analyst_agent(state)
        
        # Post-processing should strip 'rocket_repair' because it's not in valid services
        assert result["problem"]["service"] is None
        assert "unsupported_service" in result["missing_information"]
        assert result["problem"]["requirements_complete"] is False


def test_llm_failure():
    """Test 7: LLM failure handles gracefully."""
    class CrashingLLM:
        def with_structured_output(self, schema):
            raise ValueError("API Offline")

    with patch("backend.app.config.settings.Settings.get_llm", return_value=CrashingLLM()):
        state: ServiceState = {"text_input": "Broken AC"}
        result = problem_analyst_agent(state)
        assert "error" in result
        assert result["error"] == "Problem analysis failed."


def test_empty_input():
    """Test empty input returns error before LLM call."""
    state: ServiceState = {}
    result = problem_analyst_agent(state)
    assert "error" in result
    assert result["error"] == "Insufficient input for problem analysis."
