"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel
from typing import Optional


class ValidatedTransaction(BaseModel):
    """Schema for validated transaction"""
    transdate: str  # DateTime in C# - ISO 8601 string format
    transdatetime: str  # DateTime in C# - ISO 8601 string format
    amount: float  # decimal in C#
    docno: int  # int in C#
    direction: str  # string in C#
    cst_dim_id: int  # long in C#
    target: int
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "transdate": "2025-11-27",
                "transdatetime": "2025-11-27T14:30:00",
                "amount": 150.50,
                "docno": 12345,
                "direction": "credit",
                "cst_dim_id": 1,
                "target": 0
            }
        }
    }


class Pattern(BaseModel):
    """Schema for pattern"""
    transdate: str
    cst_dim_id: str
    monthly_os_changes: int
    monthly_phone_model_changes: int
    last_phone_model_categorical: str
    last_os_categorical: str
    logins_last_7_days: int
    logins_last_30_days: int
    login_frequency_7d: float
    login_frequency_30d: float
    freq_change_7d_vs_mean: float
    logins_7d_over_30d_ratio: float
    avg_login_interval_30d: float
    std_login_interval_30d: float
    var_login_interval_30d: float
    ewm_login_interval_7d: float
    burstiness_login_interval: float
    fano_factor_login_interval: float
    zscore_avg_login_interval_7d: float
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "transdate": "2025-11-27",
                "cst_dim_id": "CUST001",
                "monthly_os_changes": 2,
                "monthly_phone_model_changes": 1,
                "last_phone_model_categorical": "iPhone",
                "last_os_categorical": "iOS",
                "logins_last_7_days": 5,
                "logins_last_30_days": 18,
                "login_frequency_7d": 0.71,
                "login_frequency_30d": 0.60,
                "freq_change_7d_vs_mean": 0.18,
                "logins_7d_over_30d_ratio": 0.28,
                "avg_login_interval_30d": 1.67,
                "std_login_interval_30d": 0.49,
                "var_login_interval_30d": 0.24,
                "ewm_login_interval_7d": 1.71,
                "burstiness_login_interval": 0.12,
                "fano_factor_login_interval": 0.14,
                "zscore_avg_login_interval_7d": 0.35
            }
        }
    }


class Transaction(BaseModel):
    """Schema for transaction validation"""
    transdate: str  # DateTime in C# - ISO 8601 string format
    transdatetime: str  # DateTime in C# - ISO 8601 string format
    amount: float  # decimal in C#
    docno: int  # int in C#
    direction: str  # string in C#
    cst_dim_id: int  # long in C#
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "transdate": "2025-11-27",
                "transdatetime": "2025-11-27T14:30:00",
                "amount": 150.50,
                "docno": 12345,
                "direction": "credit",
                "cst_dim_id": 1
            }
        }
    }


class APIResponse(BaseModel):
    """Standard API response schema"""
    status: str
    message: str
    data: Optional[dict] = None
