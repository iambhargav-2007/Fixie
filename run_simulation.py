import json
from unittest.mock import patch, MagicMock
from backend.app.graph.workflow import build_graph
from backend.app.models.state import ServiceState
from backend.app.agents.problem_analyst import ProblemAnalysis
from backend.app.agents.clarification import ClarificationResult
from backend.app.agents.recommendation import RecommendationResult

# We will create a smarter Mock LLM that returns different things based on the schema requested.
class SmartMockLLM:
    def with_structured_output(self, schema):
        mock = MagicMock()
        
        def invoke_behavior(messages):
            # Extract the user input context
            context = messages[1]["content"] if len(messages) > 1 else ""
            
            if schema == ProblemAnalysis:
                if "My machine is making noise" in context and "LG washing machine" not in context:
                    # Ambiguous case
                    return ProblemAnalysis(
                        problem_summary="User reports noisy machine.",
                        requirements_complete=False,
                        missing_information=["machine_type"]
                    )
                else:
                    # Clear case (either AC or resolved washing machine)
                    return ProblemAnalysis(
                        problem_summary="Resolved machine issue.",
                        service="washing_machine_repair",
                        specialization="noise",
                        requirements_complete=True,
                        requirements={"location_available": True},
                        confidence=0.95
                    )
                    
            elif schema == ClarificationResult:
                if "machine_type" in context:
                    return ClarificationResult(
                        clarification_question="What type of machine is having the problem?",
                        target_information="machine_type"
                    )
                if "location" in context:
                    return ClarificationResult(
                        clarification_question="Where are you located?",
                        target_information="location"
                    )
                return ClarificationResult(clarification_question=None, target_information=None)
                
            elif schema == RecommendationResult:
                return RecommendationResult(
                    summary="Top provider found.",
                    top_provider_id="P1",
                    explanation="This provider is a great match based on the provided facts.",
                    alternatives=[]
                )
                
            raise ValueError(f"Unknown schema: {schema}")

        mock.invoke.side_effect = invoke_behavior
        return mock


def print_state(step_name, state):
    print(f"\n--- State after {step_name} ---")
    
    # Filter out empty fields for cleaner output
    clean_state = {k: v for k, v in state.items() if v not in [None, [], {}]}
    
    # Remove messages for brevity if they exist
    if "messages" in clean_state and not clean_state["messages"]:
         del clean_state["messages"]
         
    print(json.dumps(clean_state, indent=2))


def run_edge_cases():
    graph = build_graph()
    
    with patch("backend.app.config.settings.Settings.get_llm", return_value=SmartMockLLM()):
        print("="*60)
        print("EDGE CASE 1: Clear Problem -> Ready for Discovery")
        print("="*60)
        state1: ServiceState = {
            "text_input": "My AC is leaking water.",
            "location": {"lat": 17.0, "lng": 78.0}
        }
        res1 = graph.invoke(state1)
        print_state("Edge Case 1 Result", res1)


        print("\n\n" + "="*60)
        print("EDGE CASE 2: Ambiguous Problem -> Clarification Required")
        print("="*60)
        state2: ServiceState = {
            "text_input": "My machine is making noise."
        }
        res2 = graph.invoke(state2)
        print_state("Edge Case 2 (Paused) Result", res2)


        print("\n\n" + "="*60)
        print("EDGE CASE 3: Resuming after Clarification")
        print("="*60)
        # We append the user's answer to the messages and re-invoke
        state2["messages"] = [{"role": "user", "content": "It's an LG washing machine."}]
        res3 = graph.invoke(state2)
        print_state("Edge Case 3 (Resumed) Result", res3)

        print("\n\n" + "="*60)
        print("EDGE CASE 4: Second Clarification Answered (Location)")
        print("="*60)
        state2["messages"].append({"role": "user", "content": "I am in Gachibowli, Hyderabad."})
        state2["location"] = {"lat": 17.44, "lng": 78.34}
        res4 = graph.invoke(state2)
        print_state("Edge Case 4 (Final Ready) Result", res4)

if __name__ == "__main__":
    run_edge_cases()
