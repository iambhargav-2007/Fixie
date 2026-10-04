"""FastAPI application entry point for FixFind AI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.chat import router as chat_router
from backend.app.api.providers import router as providers_router
from backend.app.api.requests import router as requests_router

app = FastAPI(
    title="FixFind AI API",
    description="Multimodal Agentic Service Discovery Assistant API",
    version="0.1.0",
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "fixfind-backend"}

app.include_router(chat_router, tags=["Chat"])
app.include_router(providers_router, tags=["Providers"])
app.include_router(requests_router, tags=["Requests"])
