import io
import fitz  # PyMuPDF
from fastapi.testclient import TestClient
from app.main import app
from app.services.ats_audit import audit_resume_parsability
from app.services.parser import compute_sha256

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert data["status"] == "operational"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data

def test_bullet_rewriter_endpoint():
    payload = {
        "bullet_text": "worked on fixing bugs in python api",
        "target_role": "Backend Engineer"
    }
    response = client.post("/api/v1/copilot/rewrite-bullet", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["original_bullet"] == payload["bullet_text"]
    assert len(data["enhanced_variants"]) > 0

def test_ats_audit_logic():
    sample_resume_text = """
    Jane Doe
    Email: jane.doe@example.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/janedoe
    GitHub: github.com/janedoe

    Professional Summary
    Senior Full-Stack Engineer with 6+ years of experience building resilient cloud systems.

    Work Experience
    Senior Software Engineer | Tech Corp (2021 - Present)
    - Architected and engineered microservices handling 500k daily requests with 99.99% uptime.
    - Optimized PostgreSQL and Redis caching, reducing query latency by 45%.
    - Spearheaded team migration to Docker and Kubernetes, saving $120k annually in cloud spend.

    Technical Skills
    Python, FastAPI, TypeScript, React, Docker, Kubernetes, PostgreSQL, AWS

    Education
    Bachelor of Science in Computer Science | State University (2015 - 2019)
    """

    audit = audit_resume_parsability(sample_resume_text, page_count=1, file_type="pdf")
    
    assert audit["formatting_score"] > 80
    assert audit["contact_info"]["email"] == "jane.doe@example.com"
    assert audit["contact_info"]["phone"] == "(555) 123-4567"
    assert "Experience" in audit["sections"]["detected"]
    assert "Skills" in audit["sections"]["detected"]
    assert "Education" in audit["sections"]["detected"]
    assert len(audit["action_verbs"]) >= 3
    assert len(audit["quantifiable_metrics"]) >= 2

def test_upload_invalid_extension():
    file_content = b"This is a plain text file pretending to be code."
    files = {"file": ("resume.txt", file_content, "text/plain")}
    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_upload_valid_pdf_and_caching():
    # Programmatically create a valid PDF with PyMuPDF
    doc = fitz.open()
    page = doc.new_page()
    text = (
        "John Developer\n"
        "Email: john.dev@example.com\n"
        "Phone: 123-456-7890\n\n"
        "Professional Experience\n"
        "Software Engineer at Acme Corp.\n"
        "- Engineered automated testing pipelines reducing deployment failures by 35%.\n"
        "- Spearheaded backend API migration to FastAPI.\n\n"
        "Education\n"
        "B.S. in Software Engineering, Tech Institute\n\n"
        "Skills\n"
        "Python, Docker, SQL, Git"
    )
    page.insert_text((50, 72), text)
    pdf_bytes = doc.tobytes()
    doc.close()

    files = {"file": ("test_resume.pdf", pdf_bytes, "application/pdf")}
    
    # 1. First upload: Creates new record
    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test_resume.pdf"
    assert data["file_type"] == "pdf"
    assert data["page_count"] == 1
    assert data["is_cached"] is False
    assert data["audit"]["formatting_score"] > 60
    assert data["audit"]["contact_info"]["email"] == "john.dev@example.com"

    resume_id = data["resume_id"]

    # 2. Second upload of identical file: Should return cached record with is_cached=True
    files_cached = {"file": ("test_resume.pdf", pdf_bytes, "application/pdf")}
    response_cached = client.post("/api/v1/resumes/upload", files=files_cached)
    assert response_cached.status_code == 201
    data_cached = response_cached.json()
    assert data_cached["resume_id"] == resume_id
    assert data_cached["is_cached"] is True

    # 3. Retrieve audit endpoint
    audit_res = client.get(f"/api/v1/resumes/{resume_id}/audit")
    assert audit_res.status_code == 200
    assert audit_res.json()["formatting_score"] > 60

def test_integration_sample_resumes():
    """Integration test verifying all 6 realistic industry sample resumes (.pdf & .docx)."""
    import os
    samples_dir = os.path.join(os.path.dirname(__file__), "sample_resumes")
    assert os.path.exists(samples_dir), "Sample resumes directory must exist"
    
    files = sorted(os.listdir(samples_dir))
    assert len(files) == 6, f"Expected 6 sample resumes, found {len(files)}"

    for filename in files:
        filepath = os.path.join(samples_dir, filename)
        mime = "application/pdf" if filename.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        with open(filepath, "rb") as f:
            content = f.read()
        
        res = client.post("/api/v1/resumes/upload", files={"file": (filename, content, mime)})
        assert res.status_code == 201, f"Failed uploading {filename}: {res.text}"
        data = res.json()
        assert data["word_count"] > 30, f"Word count too low for {filename}"
        assert data["audit"]["formatting_score"] > 0
        
        # Test specific expectations
        if "1_Senior_FullStack" in filename:
            assert data["audit"]["formatting_score"] >= 80
            assert data["audit"]["contact_info"]["email"] is not None
            assert "Experience" in data["audit"]["sections"]["detected"]
        elif "3_DevOps" in filename:
            assert data["file_type"] == "docx"
            assert data["audit"]["formatting_score"] >= 75
        elif "6_Needs_Improvement" in filename:
            # Edge case has missing contact info and non-standard sections
            assert data["audit"]["formatting_score"] < 65
            assert data["audit"]["contact_info"]["email"] is None
            assert len(data["audit"]["recommendations"]) >= 2

