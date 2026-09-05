import pytest
from app.services.ats_audit import (
    extract_contact_info,
    detect_sections,
    count_quantifiable_metrics,
    count_action_verbs,
    audit_resume_parsability
)

def test_extract_contact_info():
    sample = (
        "Jane Doe | jane.doe@example.com | +1 (555) 345-6789 | "
        "https://linkedin.com/in/janedoe-dev | github.com/janedoe-coder"
    )
    contact = extract_contact_info(sample)
    assert contact["email"] == "jane.doe@example.com"
    assert contact["phone"] == "+1 (555) 345-6789"
    assert "linkedin.com/in/janedoe-dev" in contact["linkedin"]
    assert "github.com/janedoe-coder" in contact["github"]

def test_detect_sections_present():
    sample = """
    Professional Summary
    Experienced developer.
    Work Experience
    Software Engineer at Acme.
    Technical Skills
    Python, SQL.
    Education
    B.S. in CS.
    Projects
    Personal blog.
    Certifications
    AWS Certified.
    """
    sections = detect_sections(sample)
    assert "Summary" in sections["detected"]
    assert "Experience" in sections["detected"]
    assert "Skills" in sections["detected"]
    assert "Education" in sections["detected"]
    assert "Projects" in sections["detected"]
    assert "Certifications" in sections["detected"]
    assert len(sections["missing"]) == 0

def test_detect_sections_missing():
    sample = "Random notes about work with no standard headers."
    sections = detect_sections(sample)
    assert len(sections["detected"]) == 0
    assert "Experience" in sections["missing"]
    assert "Skills" in sections["missing"]

def test_count_quantifiable_metrics():
    sample = (
        "Increased revenue by 35% and cut costs by $150k annually. "
        "Processed 2.5M daily requests for 80k active users."
    )
    metrics = count_quantifiable_metrics(sample)
    assert any("35%" in m for m in metrics)
    assert any("$150k" in m or "150k" in m for m in metrics)
    assert len(metrics) >= 2

def test_count_action_verbs():
    sample = (
        "Architected scalable backend, engineered APIs, spearheaded CI/CD migration, "
        "automated test pipelines, and optimized databases."
    )
    verbs = count_action_verbs(sample)
    assert "architected" in verbs
    assert "engineered" in verbs
    assert "spearheaded" in verbs
    assert "automated" in verbs
    assert "optimized" in verbs

def test_audit_resume_parsability_optimal(valid_resume_text):
    audit = audit_resume_parsability(valid_resume_text, page_count=1, file_type="pdf")
    assert audit["formatting_score"] >= 80
    assert audit["contact_info"]["email"] == "alex.wright@techmail.com"
    assert audit["contact_info"]["phone"] == "(555) 234-5678"
    assert "Experience" in audit["sections"]["detected"]
    assert "Skills" in audit["sections"]["detected"]
    assert "Education" in audit["sections"]["detected"]
    assert audit["breakdown"]["contact_score"] >= 20
    assert audit["breakdown"]["section_score"] >= 30

def test_audit_resume_parsability_edge_case(edge_case_resume_text):
    audit = audit_resume_parsability(edge_case_resume_text, page_count=1, file_type="pdf")
    # Low score due to missing email, phone, and non-standard headers
    assert audit["formatting_score"] < 65
    assert audit["contact_info"]["email"] is None
    assert audit["contact_info"]["phone"] is None
    assert "Experience" in audit["sections"]["missing"]
    
    # Recommendations should highlight critical issues
    issues = [r["issue"] for r in audit["recommendations"]]
    assert any("email" in i.lower() for i in issues)
    assert any("phone" in i.lower() for i in issues)
    assert any("experience" in i.lower() for i in issues)
