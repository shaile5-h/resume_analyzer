import datetime
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import engine, Base
from app.api.router import api_router
from app.schemas.schemas import HealthResponse

# Create SQLite database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Enterprise-grade AI-Powered Resume Analyzer, ATS Parsability Auditor, and Career Copilot API.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure Cross-Origin Resource Sharing (CORS) for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", summary="Root Welcome Endpoint")
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "documentation": "/docs",
        "health": "/health",
        "status": "operational"
    }

@app.get("/health", response_model=HealthResponse, summary="API Health Check")
def health_check():
    """Health check endpoint to verify backend operational readiness."""
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.datetime.utcnow()
    )
