"""FastAPI application entry point for FixFind AI."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import services, providers

app = FastAPI(
    title="FixFind AI API",
    description="Backend API for FixFind AI service discovery",
    version="0.1.0",
)

# CORS setup
origins_str = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')
import json
try:
    origins = json.loads(origins_str)
except Exception:
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router)
app.include_router(providers.router)

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "fixfind-backend"}
