import os

def test_list_resumes_endpoint(client):
    response = client.get("/api/v1/resumes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_invalid_file_extension(client):
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("malicious.exe", b"binary content", "application/x-msdownload")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_upload_all_sample_resumes(client, sample_resumes_dir):
    """
    End-to-end integration test verifying that all 6 industry-standard
    sample resumes (.pdf and .docx) upload, parse, and evaluate properly.
    """
    assert os.path.exists(sample_resumes_dir), f"Directory {sample_resumes_dir} must exist"
    sample_files = sorted(os.listdir(sample_resumes_dir))
    assert len(sample_files) == 6, f"Expected 6 sample resumes, found {len(sample_files)}"

    for filename in sample_files:
        filepath = os.path.join(sample_resumes_dir, filename)
        mime = "application/pdf" if filename.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        with open(filepath, "rb") as f:
            content = f.read()

        # 1. Initial Upload
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": (filename, content, mime)}
        )
        assert response.status_code == 201, f"Failed uploading {filename}: {response.text}"
        data = response.json()

        assert data["filename"] == filename
        assert data["word_count"] > 30
        assert data["audit"]["formatting_score"] > 0
        resume_id = data["resume_id"]

        # 2. Duplicate Upload (Testing SHA-256 Deduplication Caching)
        dup_response = client.post(
            "/api/v1/resumes/upload",
            files={"file": (filename, content, mime)}
        )
        assert dup_response.status_code == 201
        dup_data = dup_response.json()
        assert dup_data["resume_id"] == resume_id
        assert dup_data["is_cached"] is True

        # 3. Retrieve Individual Resume Record
        get_res = client.get(f"/api/v1/resumes/{resume_id}")
        assert get_res.status_code == 200
        assert get_res.json()["id"] == resume_id

        # 4. Retrieve Resume Audit Record
        audit_res = client.get(f"/api/v1/resumes/{resume_id}/audit")
        assert audit_res.status_code == 200
        assert audit_res.json()["formatting_score"] > 0

        # 5. Role-Specific Profile Verification
        if "1_Senior_FullStack" in filename:
            assert data["audit"]["formatting_score"] >= 80
            assert data["audit"]["contact_info"]["email"] is not None
            assert "Experience" in data["audit"]["sections"]["detected"]
        elif "3_DevOps" in filename:
            assert data["file_type"] == "docx"
            assert data["audit"]["formatting_score"] >= 75
        elif "6_Needs_Improvement" in filename:
            # Low score for edge case missing contact details and non-standard sections
            assert data["audit"]["formatting_score"] < 65
            assert data["audit"]["contact_info"]["email"] is None
            assert len(data["audit"]["recommendations"]) >= 2
