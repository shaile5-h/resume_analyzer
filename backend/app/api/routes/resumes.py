from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Resume
from app.schemas.schemas import ResumeResponse

router = APIRouter()

@router.get("/", response_model=List[ResumeResponse], summary="List all uploaded resumes")
def list_resumes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Retrieve list of uploaded resumes with pagination."""
    resumes = db.query(Resume).order_by(Resume.uploaded_at.desc()).offset(skip).limit(limit).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeResponse, summary="Get resume details by ID")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Retrieve details and extracted raw text of a specific resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return resume
