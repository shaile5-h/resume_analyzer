import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False) # 'pdf' or 'docx'
    file_path = Column(String(500), nullable=False)
    file_hash = Column(String(64), index=True, nullable=False) # SHA-256 for caching
    raw_text = Column(Text, nullable=False)
    page_count = Column(Integer, default=1)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Resume(id={self.id}, filename='{self.filename}', hash='{self.file_hash[:8]}...')>"


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="job_description", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobDescription(id={self.id}, role='{self.role_title}')>"


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="SET NULL"), nullable=True)
    
    # Quantitative Scores (0 - 100)
    overall_ats_score = Column(Float, nullable=False, default=0.0)
    skills_score = Column(Float, nullable=False, default=0.0)
    experience_score = Column(Float, nullable=False, default=0.0)
    formatting_score = Column(Float, nullable=False, default=0.0)
    
    # Parsed Candidate Profile Details
    candidate_name = Column(String(255), nullable=True)
    candidate_email = Column(String(255), nullable=True)
    candidate_phone = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    
    # Granular Feedback in JSON
    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    recommendations = Column(JSON, default=list) # List of {category, priority, issue, suggestion}
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis(id={self.id}, score={self.overall_ats_score}, candidate='{self.candidate_name}')>"
