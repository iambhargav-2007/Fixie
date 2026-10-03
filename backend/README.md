# Backend

This is the backend for FixFind AI, built with FastAPI and Python.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints
- **Health Endpoint:** `GET /health`
- **Swagger Documentation:** `GET /docs`
