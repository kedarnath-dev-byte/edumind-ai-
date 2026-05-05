"""
health_controller.py
Health check endpoint for EduMind AI backend.
Used by Render to verify the service is running correctly.
Returns system status, version, and environment info.
"""

from fastapi import APIRouter
from datetime import datetime
import platform

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns 200 OK with system info when backend is running.
    """
    return {
        "status": "healthy",
        "service": "EduMind AI Backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "python_version": platform.python_version(),
        "environment": "production"
    }
