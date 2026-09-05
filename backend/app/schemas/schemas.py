import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

# ==========================================
# Health Schema
# ==========================================
class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str
    environment: str
    timestamp: datetime.datetime

# ==========================================
# Resume Schemas
# ==========================================
class ResumeBase(BaseModel):
    filename: str
    file_type: str
    page_count: int = 1

class ResumeResponse(ResumeBase):
    id: int
    file_hash: str
    raw_text: str
    uploaded_at: datetime.datetime

    class Config:
        from_attributes = True

# ==========================================
# ATS Audit Schemas
# ==========================================
class ContactInfoSchema(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class SectionAuditSchema(BaseModel):
    detected: List[str]
    missing: List[str]

class ScoreBreakdownSchema(BaseModel):
    contact_score: float
    section_score: float
    length_score: float
    content_score: float

class ATSAuditResponse(BaseModel):
    formatting_score: float
    breakdown: ScoreBreakdownSchema
    contact_info: ContactInfoSchema
    sections: SectionAuditSchema
    word_count: int
    page_count: int
    file_type: str
    quantifiable_metrics: List[str]
    action_verbs: List[str]
    recommendations: List[Dict[str, Any]]

class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    file_type: str
    file_hash: str
    page_count: int
    word_count: int
    is_cached: bool
    audit: ATSAuditResponse

# ==========================================
# Job Description Schemas
# ==========================================
class JobDescriptionCreate(BaseModel):
    role_title: Optional[str] = "Target Role"
    company_name: Optional[str] = None
    raw_text: str

class JobDescriptionResponse(JobDescriptionCreate):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# ==========================================
# Analysis Schemas
# ==========================================
class RecommendationItem(BaseModel):
    category: str = Field(..., description="e.g. Impact, Formatting, Skills, Structure")
    priority: str = Field("Medium", description="High, Medium, or Low")
    issue: str
    suggestion: str

class AnalyzeRequest(BaseModel):
    resume_id: int
    job_description_text: Optional[str] = None
    role_title: Optional[str] = "Target Role"
    company_name: Optional[str] = None

class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    job_description_id: Optional[int] = None
    overall_ats_score: float
    skills_score: float
    experience_score: float
    formatting_score: float
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    summary: Optional[str] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendations: List[RecommendationItem] = []
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# ==========================================
# Career Copilot Schemas
# ==========================================
class BulletRewriteRequest(BaseModel):
    bullet_text: str = Field(..., description="Original weak or unquantified resume bullet point")
    target_role: Optional[str] = Field("Software Engineer", description="Target role context")

class BulletRewriteResponse(BaseModel):
    original_bullet: str
    enhanced_variants: List[Dict[str, str]] = Field(
        ...,
        description="List of rewritten bullets using Google XYZ or STAR formulas with rationales"
    )

class InterviewPrepRequest(BaseModel):
    role_title: str
    skills: List[str] = []
    missing_skills: List[str] = []

class InterviewQuestion(BaseModel):
    category: str # 'Technical', 'Behavioral', 'System Design'
    question: str
    context: str
    suggested_talking_points: List[str]

class InterviewPrepResponse(BaseModel):
    role_title: str
    questions: List[InterviewQuestion]
