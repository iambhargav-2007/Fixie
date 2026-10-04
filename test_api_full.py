import requests

b64 = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAQAAAAAYLlVAAAAO0lEQVR42u3XQQ0AIAwAwe1/6ABz1w0k4B0dIDbZq6rO/1oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAODHAr8vAQG0O3h/AAAAAElFTkSuQmCC"

res = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "session_id": "test_api_fail",
        "text": "my ac leaks water from the inner unit",
        "image_url": f"data:image/png;base64,{b64}",
        "location": {"lat": 17.385, "lng": 78.486, "locality": "Hyderabad"}
    }
)
print("STATUS CODE:", res.status_code)
print("RESPONSE:", res.text)
