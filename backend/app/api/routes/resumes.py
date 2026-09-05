import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.db.session import get_db
from app.models.models import Resume
from app.schemas.schemas import ResumeResponse, ResumeUploadResponse, ATSAuditResponse
from app.services.parser import parse_resume_document
from app.services.ats_audit import audit_resume_parsability

router = APIRouter()

@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload, parse and run deterministic ATS audit on a resume (PDF/DOCX)"
)
async def upload_resume(
    file: UploadFile = File(..., description="Resume document in PDF or DOCX format"),
    db: Session = Depends(get_db)
):
    """
    Ingest a resume file:
    - Validates file size (<10MB) and format (.pdf, .docx).
    - Checks SHA-256 hash against existing database records for instant deduplication/caching.
    - Extracts raw text and page count with PyMuPDF or python-docx.
    - Executes zero-latency deterministic ATS formatting & parsability audit.
    - Saves parsed resume to SQLite database.
    """
    filename = file.filename or "uploaded_resume.pdf"
    file_bytes = await file.read()

    # Parse and extract text using multi-format pipeline
    parsed_data = parse_resume_document(file_bytes, filename)
    file_hash = parsed_data["file_hash"]

    # Check for existing resume in database with identical hash (SHA-256 caching)
    existing_resume = db.query(Resume).filter(Resume.file_hash == file_hash).first()
    if existing_resume:
        audit_result = audit_resume_parsability(
            raw_text=existing_resume.raw_text,
            page_count=existing_resume.page_count,
            file_type=existing_resume.file_type
        )
        return ResumeUploadResponse(
            resume_id=existing_resume.id,
            filename=existing_resume.filename,
            file_type=existing_resume.file_type,
            file_hash=existing_resume.file_hash,
            page_count=existing_resume.page_count,
            word_count=len(existing_resume.raw_text.split()),
            is_cached=True,
            audit=audit_result
        )

    # Save file to uploads directory
    safe_filename = f"{file_hash[:12]}_{filename}"
    saved_file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)
    try:
        with open(saved_file_path, "wb") as f:
            f.write(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to persist file to disk: {str(e)}"
        )

    # Run deterministic ATS audit
    audit_result = audit_resume_parsability(
        raw_text=parsed_data["raw_text"],
        page_count=parsed_data["page_count"],
        file_type=parsed_data["file_type"]
    )

    # Persist resume record to SQLite
    new_resume = Resume(
        filename=filename,
        file_type=parsed_data["file_type"],
        file_path=saved_file_path,
        file_hash=file_hash,
        raw_text=parsed_data["raw_text"],
        page_count=parsed_data["page_count"]
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return ResumeUploadResponse(
        resume_id=new_resume.id,
        filename=new_resume.filename,
        file_type=new_resume.file_type,
        file_hash=new_resume.file_hash,
        page_count=new_resume.page_count,
        word_count=parsed_data["word_count"],
        is_cached=False,
        audit=audit_result
    )

@router.get(
    "/{resume_id}/audit",
    response_model=ATSAuditResponse,
    summary="Get detailed deterministic ATS audit for a resume"
)
def get_resume_audit(resume_id: int, db: Session = Depends(get_db)):
    """Retrieve full deterministic ATS parsability analysis for a stored resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    return audit_resume_parsability(
        raw_text=resume.raw_text,
        page_count=resume.page_count,
        file_type=resume.file_type
    )

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
