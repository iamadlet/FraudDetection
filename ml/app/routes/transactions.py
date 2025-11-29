"""
Routes for validated transaction operations
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ValidatedTransaction, APIResponse
from app.database.repositories import ValidatedTransactionRepository

router = APIRouter(prefix="/api", tags=["transactions"])


@router.post("/create-validated-transaction", response_model=APIResponse)
def create_validated_transaction(transaction: ValidatedTransaction):
    """
    Create and store a new validated transaction in the database.
    
    Args:
        transaction: Validated transaction object
        
    Returns:
        Success response with transaction data
    """
    try:
        ValidatedTransactionRepository.create(transaction)
        return APIResponse(
            status="success",
            message="Validated transaction created successfully",
            data=transaction.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create validated transaction: {str(e)}"
        )
