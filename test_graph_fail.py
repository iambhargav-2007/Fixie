import json
import traceback
from backend.app.graph.workflow import build_graph
from backend.app.models.state import ServiceState

state = ServiceState(
    session_id="test_api_fail",
    text_input="my ac is leaking water",
    image_input="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAQAAAAAYLlVAAAAO0lEQVR42u3XQQ0AIAwAwe1/6ABz1w0k4B0dIDbZq6rO/1oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAODHAr8vAQG0O3h/AAAAAElFTkSuQmCC",
    location={"lat": 17.385, "lng": 78.486, "locality": "Hyderabad"},
    messages=[],
    missing_information=[]
)

graph = build_graph()
try:
    res = graph.invoke(state)
    print("SUCCESS")
except Exception as e:
    traceback.print_exc()
