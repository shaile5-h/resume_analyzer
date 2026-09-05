from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Analysis
from app.schemas.schemas import AnalysisResponse

router = APIRouter()

@router.get("/history", response_model=List[AnalysisResponse], summary="List evaluation history")
def list_analyses(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Retrieve historical resume evaluations."""
    analyses = db.query(Analysis).order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    return analyses

@router.get("/{analysis_id}", response_model=AnalysisResponse, summary="Get analysis by ID")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific analysis by its ID."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found")
    return analysis
