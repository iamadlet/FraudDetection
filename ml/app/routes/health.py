"""
Routes for health checks and API information
"""

from fastapi import APIRouter
from app.config.settings import API_TITLE, API_VERSION

router = APIRouter(tags=["health"])


@router.get("/")
def read_root():
    """API root endpoint with information"""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "endpoints": {
            "POST /api/create-validated-transaction": "Create a new validated transaction",
            "POST /api/create-pattern": "Create a new pattern",
            "POST /api/validate-transaction": "Validate a transaction",
            "GET /api/TriggerRetraining": "Trigger model retraining",
            "GET /health": "Health check"
        }
    }


@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": API_TITLE
    }
