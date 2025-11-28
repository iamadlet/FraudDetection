"""
Routes for transaction validation and model retraining
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.schemas import Transaction, APIResponse
from app.database.repositories import ValidatedTransactionRepository, PatternRepository
from app.ml.predictor import predictor
import os
import sys
import subprocess

router = APIRouter(prefix="/api", tags=["validation"])


@router.post("/validate-transaction", response_model=APIResponse)
def validate_transaction(transaction: Transaction):
    """
    Validate a transaction against patterns and predict fraud using ML model.
    
    Args:
        transaction: Transaction object to validate
        
    Returns:
        Validation result with fraud prediction (0 = legitimate, 1 = fraud)
    """
    try:
        # Convert transaction to dictionary
        transaction_data = transaction.dict()
        
        # Make fraud prediction using the ML model
        prediction = predictor.predict(transaction_data)
        
        # Get prediction probabilities if available
        probabilities = predictor.predict_proba(transaction_data)
        
        # Build validation result
        validation_result = {
            "prediction": prediction,  # 0 = legitimate, 1 = fraud
            "is_fraud": prediction == 1,
            "transaction": transaction_data,
            "probabilities": probabilities,
            "timestamp": datetime.now().isoformat()
        }
        
        return APIResponse(
            status="success",
            message=f"Transaction {'flagged as FRAUD' if prediction == 1 else 'validated as legitimate'}",
            data=validation_result
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation failed: {str(e)}"
        )


@router.get("/trigger-retraining", response_model=APIResponse)
def trigger_retraining():
    """
    Trigger model retraining with current data from database.
    
    Returns:
        Status of the retraining process with data statistics
    """
    try:
        # Run app/Script.py synchronously and capture log
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Script.py'))
        script_dir = os.path.dirname(script_path)
        if not os.path.exists(script_path):
            raise HTTPException(status_code=500, detail=f"Retraining script not found at: {script_path}")

        logs_dir = os.path.join(script_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = os.path.join(logs_dir, f'retraining_{ts}.log')

        start_ts = datetime.now().timestamp()
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        with open(log_path, 'wb') as lf:
            proc = subprocess.run([sys.executable, script_path], cwd=script_dir, stdout=lf, stderr=subprocess.STDOUT, env=env)

        retraining_result = {
            "timestamp": datetime.now().isoformat(),
            "log_path": log_path,
            "exit_code": proc.returncode
        }

        if proc.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Retraining script failed with code {proc.returncode}. See log: {log_path}")

        # Detect model file created in script directory
        model_path = os.path.join(script_dir, 'best_xgb_model.pkl')
        if os.path.exists(model_path):
            mtime = os.path.getmtime(model_path)
            if mtime >= start_ts:
                retraining_result['new_model_path'] = model_path
                return APIResponse(status='success', message='New model created successfully', data=retraining_result)
            else:
                retraining_result['model_path'] = model_path
                return APIResponse(status='success', message='No new model created (existing model present)', data=retraining_result)
        else:
            raise HTTPException(status_code=500, detail=f"No model file created. See log: {log_path}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Retraining failed: {str(e)}"
        )
