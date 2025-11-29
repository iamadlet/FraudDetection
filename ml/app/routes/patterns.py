"""
Routes for pattern operations
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import Pattern, APIResponse
from app.database.repositories import PatternRepository

router = APIRouter(prefix="/api", tags=["patterns"])


@router.post("/create-pattern", response_model=APIResponse)
def create_pattern(pattern: Pattern):
    """
    Create and store a new pattern in the database.
    
    Args:
        pattern: Pattern object with all required features
        
    Returns:
        Success response with pattern data
    """
    try:
        PatternRepository.create(pattern)
        return APIResponse(
            status="success",
            message="Pattern created successfully",
            data=pattern.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create pattern: {str(e)}"
        )
