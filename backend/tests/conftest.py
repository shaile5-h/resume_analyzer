import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """Shared FastAPI test client instance across the test session."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session")
def sample_resumes_dir():
    """Path to the 6 industry-standard sample resumes for testing."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    resumes_dir = os.path.join(tests_dir, "sample_resumes")
    if not os.path.exists(resumes_dir):
        # Fallback to root sample_resumes
        resumes_dir = os.path.join(os.path.dirname(os.path.dirname(tests_dir)), "sample_resumes")
    return resumes_dir

@pytest.fixture
def valid_resume_text():
    return """
    Alexander Wright
    Email: alex.wright@techmail.com
    Phone: (555) 234-5678
    LinkedIn: linkedin.com/in/alexanderwright
    GitHub: github.com/awright-dev

    Professional Summary
    Senior Full-Stack Engineer with 7+ years of experience architecting resilient microservices and web applications.

    Technical Skills
    Python, FastAPI, TypeScript, React.js, Docker, Kubernetes, AWS, PostgreSQL, Redis

    Work Experience
    Senior Full-Stack Engineer | CloudScale Technologies (2021 - Present)
    - Architected and engineered distributed microservices handling 2.5M daily requests with 99.99% uptime.
    - Optimized database queries and introduced Redis caching, reducing API latency by 45%.
    - Spearheaded frontend migration to React, boosting web performance by 35%.
    - Mentored a team of 6 engineers and automated CI/CD pipelines.

    Education
    Bachelor of Science in Computer Science | UC Berkeley (2014 - 2018)
    """

@pytest.fixture
def edge_case_resume_text():
    return """
    John Doe
    Location: Dallas, Texas

    Things I Have Worked On
    I have done coding for many years in various small tasks.

    My Past Roles
    Developer at Small Tech Firm
    - Worked on computer bugs and assisted senior teammates.
    - Did some website modifications.

    What I Know
    Computers, internet, programming languages.

    Schooling
    College degree in general technology studies.
    """
