import os
import json
from backend.app.agents.problem_analyst import problem_analyst_agent
from backend.app.models.state import ServiceState

state = ServiceState(
    session_id="test",
    text_input="my ac is leaking water from the indoor unit in my house",
    location={"lat": 17.385, "lng": 78.486, "locality": "Hyderabad"},
    vision_result=None
)

res = problem_analyst_agent(state)
print(json.dumps(res, indent=2))
