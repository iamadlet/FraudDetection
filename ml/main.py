"""
FastAPI Fraud Detection Application - Main Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import API_TITLE, API_VERSION, API_DESCRIPTION
from app.database.connection import db
from app.routes import health, transactions, patterns, validation

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(transactions.router)
app.include_router(patterns.router)
app.include_router(validation.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    db.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    db.disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
