import datetime
import pytest
from app.schemas.schemas import (
    HealthResponse,
    ResumeUploadResponse,
    ATSAuditResponse,
    ScoreBreakdownSchema,
    ContactInfoSchema,
    SectionAuditSchema,
    BulletRewriteRequest,
    BulletRewriteResponse,
    InterviewPrepRequest,
    InterviewPrepResponse
)

def test_health_response_schema():
    data = HealthResponse(
        status="ok",
        app_name="Test App",
        environment="test",
        timestamp=datetime.datetime.utcnow()
    )
    assert data.status == "ok"
    assert data.app_name == "Test App"

def test_bullet_rewrite_schema():
    req = BulletRewriteRequest(bullet_text="fixed python bugs", target_role="Backend Engineer")
    assert req.bullet_text == "fixed python bugs"

    res = BulletRewriteResponse(
        original_bullet=req.bullet_text,
        enhanced_variants=[
            {"formula": "XYZ", "text": "Resolved 50+ bugs", "rationale": "Clear metrics"}
        ]
    )
    assert len(res.enhanced_variants) == 1
    assert res.enhanced_variants[0]["formula"] == "XYZ"

def test_ats_audit_schema():
    audit = ATSAuditResponse(
        formatting_score=85.5,
        breakdown=ScoreBreakdownSchema(
            contact_score=25.0,
            section_score=30.0,
            length_score=15.0,
            content_score=15.5
        ),
        contact_info=ContactInfoSchema(email="user@test.com", phone="1234567890"),
        sections=SectionAuditSchema(detected=["Experience", "Skills"], missing=["Certifications"]),
        word_count=500,
        page_count=1,
        file_type="pdf",
        quantifiable_metrics=["35%", "$100k"],
        action_verbs=["engineered", "automated"],
        recommendations=[]
    )
    assert audit.formatting_score == 85.5
    assert audit.breakdown.contact_score == 25.0
    assert audit.contact_info.email == "user@test.com"
