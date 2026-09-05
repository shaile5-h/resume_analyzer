from fastapi import APIRouter
from app.api.routes import resumes, analyses, copilot

api_router = APIRouter()

api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["Analyses"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["Career Copilot"])
