"""Tests for the Recommendation Agent."""

import pytest
from unittest.mock import patch

from backend.app.agents.recommendation import recommendation_agent, RecommendationResult, AlternativeRecommendation
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


def test_top_match():
    """Test Case 1: Top match generates grounded recommendation."""
    mock_response = RecommendationResult(
        summary="Found a great match.",
        top_provider_id="P102",
        explanation="CoolCare is nearby (2.1 km) and available today.",
        alternatives=[]
    )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(mock_response)):
        state: ServiceState = {
            "problem": {"service": "ac_repair", "specialization": "water_leakage"},
            "ranked_providers": [
                {
                    "id": "P102",
                    "name": "CoolCare Services",
                    "distance_km": 2.1,
                    "rating": 4.7,
                    "price_min": 400,
                    "price_max": 700,
                    "availability": "today",
                    "fit_score": 95.4,
                    "services": ["ac_repair"],
                    "specializations": ["water_leakage"],
                    "verified": True
                }
            ]
        }
        
        result = recommendation_agent(state)
        
        assert "recommendation" in result
        rec = result["recommendation"]
        assert rec["top_provider_id"] == "P102"
        assert "CoolCare is nearby" in rec["explanation"]


def test_multiple_providers():
    """Test Case 2: Multiple providers ordered properly."""
    mock_response = RecommendationResult(
        summary="Found 3 matches.",
        top_provider_id="P1",
        explanation="P1 is the best.",
        alternatives=[
            AlternativeRecommendation(provider_id="P2", reason="Also good."),
            AlternativeRecommendation(provider_id="P3", reason="Farther but available.")
        ]
    )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(mock_response)):
        state: ServiceState = {
            "ranked_providers": [
                {"id": "P1"},
                {"id": "P2"},
                {"id": "P3"}
            ]
        }
        
        result = recommendation_agent(state)
        
        rec = result["recommendation"]
        assert rec["top_provider_id"] == "P1"
        assert len(rec["alternatives"]) == 2
        assert rec["alternatives"][0]["provider_id"] == "P2"


def test_no_providers():
    """Test Case 3: No providers handles cleanly."""
    state: ServiceState = {
        "ranked_providers": []
    }
    # No mock LLM since it shouldn't be called
    result = recommendation_agent(state)
    
    rec = result["recommendation"]
    assert rec["top_provider_id"] is None
    assert "No matching providers" in rec["summary"]
    assert len(rec["alternatives"]) == 0


def test_missing_rating():
    """Test Case 4: Missing rating is not hallucinated."""
    # Since we can't test LLM internals natively with a mocked structured return
    # we just verify the system prompt enforces this constraint via the context.
    mock_response = RecommendationResult(
        summary="Good match",
        top_provider_id="P1",
        explanation="They are a great choice.",
        alternatives=[]
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "ranked_providers": [{"id": "P1", "name": "CoolCare", "fit_score": 90}]
        }
        
        recommendation_agent(state)
        
        messages = mock_llm.structured_llm.last_messages
        system_prompt = messages[0]["content"]
        assert "If a field like 'rating' or 'availability' is missing, do not mention it" in system_prompt


def test_missing_availability():
    """Test Case 5: Missing availability constraint."""
    # Similar to test 4, testing via constraint injection in the prompt
    mock_response = RecommendationResult(
        summary="Match",
        top_provider_id="P1",
        explanation="Explained",
        alternatives=[]
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "ranked_providers": [{"id": "P1", "name": "CoolCare", "fit_score": 90}]
        }
        
        recommendation_agent(state)
        
        messages = mock_llm.structured_llm.last_messages
        system_prompt = messages[0]["content"]
        assert "availability" in system_prompt


def test_fact_preservation():
    """Test Case 6: Fact preservation enforced."""
    mock_response = RecommendationResult(
        summary="Match",
        top_provider_id="P1",
        explanation="Explained",
        alternatives=[]
    )
    mock_llm = MockLLM(mock_response)
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=mock_llm):
        state: ServiceState = {
            "ranked_providers": [
                {"id": "P1", "fit_score": 95.4, "distance_km": 2.1, "rating": 4.7, "price_min": 400}
            ]
        }
        
        recommendation_agent(state)
        
        messages = mock_llm.structured_llm.last_messages
        context = messages[1]["content"]
        assert "95.4" in context
        assert "2.1" in context
        assert "4.7" in context
        assert "400" in context


def test_llm_failure():
    """Test Case 7: LLM failure handles gracefully."""
    class CrashingLLM:
        def with_structured_output(self, schema):
            raise ValueError("Rate Limit")

    with patch("backend.app.config.settings.Settings.get_llm", return_value=CrashingLLM()):
        state: ServiceState = {
            "ranked_providers": [{"id": "P1"}]
        }
        result = recommendation_agent(state)
        
        assert "error" in result
        assert result["error"] == "Recommendation generation failed."


def test_no_llm_call_when_empty():
    """Test Case 8: No LLM call when empty."""
    # We use a dummy patch. If the code attempts to use LLM, it will crash.
    with patch("backend.app.config.settings.Settings.get_llm", side_effect=Exception("Should not be called")):
        state: ServiceState = {"ranked_providers": []}
        result = recommendation_agent(state)
        assert result["recommendation"]["top_provider_id"] is None


def test_provider_fact_grounding():
    """Test Case 9: Forcing top_provider_id correctly against LLM hallucinations."""
    # LLM hallucinates and decides P2 should be the top match, and invents an alternative P99
    mock_response = RecommendationResult(
        summary="I re-ranked them for you.",
        top_provider_id="P2",
        explanation="I like P2 better.",
        alternatives=[
            AlternativeRecommendation(provider_id="P99", reason="Made up alternative.")
        ]
    )
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=MockLLM(mock_response)):
        state: ServiceState = {
            "ranked_providers": [
                {"id": "P1"},
                {"id": "P2"}
            ]
        }
        
        result = recommendation_agent(state)
        rec = result["recommendation"]
        
        # Post processing should FORCE top provider to be P1 because it is ranked first in the array
        assert rec["top_provider_id"] == "P1"
        
        # Post processing should strip out P99 because it wasn't in the input array
        assert len(rec["alternatives"]) == 0
