# AI-Powered Resume Analyzer: End-to-End Implementation Guide

This guide provides an exhaustive, step-by-step technical blueprint for building the **AI-Powered Resume Analyzer** from scratch to production. It follows a clean architecture, zero redundant folders, deterministic and AI scoring, and a high-end user experience.

---

## 1. Quick Launch Summary

- **Backend Running Command**: 
  ```bash
  cd backend
  python server.py
  ```
  - **Swagger / OpenAPI Documentation**: `http://127.0.0.1:8000/docs`
  - **Health Check**: `http://127.0.0.1:8000/health`
- **Frontend Running Command**: 
  ```bash
  cd frontend
  npm run dev
  ```
  - **Application UI**: `http://localhost:5173`

---

## 2. Directory Structure (Clean & Zero-Redundancy)

```
resume_analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application instance & middleware
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py        # App settings & env loading via Pydantic
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── session.py       # SQLite engine with WAL mode & sessionmaker
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── models.py        # SQLAlchemy database models
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       # Pydantic v2 request/response schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── parser.py        # PDF (PyMuPDF) & DOCX extraction
│   │   │   ├── ats_audit.py     # Rule-based layout & parsability audit
│   │   │   ├── ai_service.py    # LLM service (Gemini/OpenAI) + structured JSON
│   │   │   └── scoring.py       # Composite ATS scoring & skill gap analysis
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── router.py        # Main API v1 router
│   │       └── routes/
│   │           ├── __init__.py
│   │           ├── resumes.py   # Upload, parse, text inspection
│   │           ├── analyses.py  # Resume vs JD analysis, history
│   │           └── copilot.py   # STAR bullet rewriter, interview prep
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py          # Pytest backend test suite
│   ├── uploads/                 # Storage for uploaded files (gitignored)
│   ├── server.py                # Entrypoint: runs uvicorn on python server.py
│   └── requirements.txt         # Pinned Python dependencies
├── frontend/
│   ├── public/                  # Static assets & favicons
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx       # Header with branding & theme toggle
│   │   │   ├── FileUpload.tsx   # Drag-and-drop resume uploader with validation
│   │   │   ├── JobInput.tsx     # Job description input with sample presets
│   │   │   ├── ScoreGauge.tsx   # Animated circular SVG score indicator
│   │   │   ├── SkillsMatrix.tsx # Interactive matched vs missing skills chips
│   │   │   ├── FeedbackList.tsx # Categorized actionable recommendations
│   │   │   ├── BulletRewriter.tsx # Interactive STAR formula bullet enhancer
│   │   │   └── HistoryView.tsx  # List of past analyses with score comparisons
│   │   ├── services/
│   │   │   └── api.ts           # Axios client for backend API communication
│   │   ├── types/
│   │   │   └── index.ts         # TypeScript interfaces matching backend schemas
│   │   ├── App.tsx              # Main dashboard view & layout state
│   │   ├── main.tsx             # React DOM root entry
│   │   └── index.css            # Tailwind directives & custom animations
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── .gitignore                   # Comprehensive gitignore (venv, node_modules, db)
├── .env.example                 # Example configuration environment variables
├── .env                         # Local environment variables (gitignored)
├── plan.md                      # High-level architecture specification
└── implementation_guide.md      # Detailed step-by-step implementation guide
```

---

## 3. Environment & Configuration Files

### 3.1 `.gitignore` (Root)
```gitignore
# Python & Virtual Environments
venv/
.venv/
env/
__pycache__/
*.py[cod]
*$py.class
*.so
.pytest_cache/

# SQLite Database
*.db
*.sqlite3
*.db-wal
*.db-shm

# File Uploads
backend/uploads/*
!backend/uploads/.gitkeep

# Environment variables & secrets
.env
.env.local

# Node & Frontend
frontend/node_modules/
frontend/dist/
frontend/.vite/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE & OS
.vscode/
.idea/
.DS_Store
Thumbs.db
```

### 3.2 `.env.example` (Root)
```env
# Application Settings
APP_NAME="AI-Powered Resume Analyzer"
ENVIRONMENT="development"
DEBUG=True
API_V1_STR="/api/v1"

# Server Settings
HOST="127.0.0.1"
PORT=8000

# Database Settings
DATABASE_URL="sqlite:///./resume_analyzer.db"

# AI Provider Configuration (Google Gemini or OpenAI)
AI_PROVIDER="gemini" # Options: 'gemini' or 'openai'
GEMINI_API_KEY="your_gemini_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"

# Upload Configuration
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=["pdf", "docx"]
```

---

## 4. Stage-by-Stage Implementation

### STAGE 1: Foundation, Environment & Scaffolding

#### Step 1.1: Backend Virtual Environment & Dependencies
1. Create virtual environment inside `backend/`:
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Create `backend/requirements.txt`:
   ```txt
   fastapi>=0.110.0,<1.0.0
   uvicorn[standard]>=0.28.0,<1.0.0
   pydantic>=2.6.0,<3.0.0
   pydantic-settings>=2.2.0,<3.0.0
   sqlalchemy>=2.0.28,<3.0.0
   python-multipart>=0.0.9
   pymupdf>=1.23.26,<2.0.0
   python-docx>=1.1.0,<2.0.0
   google-genai>=0.1.1
   openai>=1.14.0
   pytest>=8.1.0
   httpx>=0.27.0
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

#### Step 1.2: Server Entrypoint (`backend/server.py`)
This file ensures that running `python server.py` boots the FastAPI app with Uvicorn and Swagger documentation:
```python
import uvicorn
import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting AI-Powered Resume Analyzer Backend")
    print("📖 Swagger UI Docs: http://127.0.0.1:8000/docs")
    print("📖 ReDoc:          http://127.0.0.1:8000/redoc")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
```

#### Step 1.3: SQLite Session with WAL Mode (`backend/app/db/session.py`)
```python
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_analyzer.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Enable SQLite Write-Ahead Logging (WAL) and Foreign Keys
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Step 1.4: Frontend Initialization
```powershell
cd ..
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install lucide-react axios clsx tailwind-merge
```

Verify backend and frontend run:
- Backend: `python server.py` -> Open `http://127.0.0.1:8000/docs`
- Frontend: `npm run dev` -> Open `http://localhost:5173`

---

### STAGE 2: Document Ingestion & Deterministic ATS Audit

#### Step 2.1: Multi-Format Parser (`backend/app/services/parser.py`)
- **PDF Extraction**: Use `fitz` (`PyMuPDF`) to extract text and font metadata.
- **DOCX Extraction**: Use `python-docx` to extract paragraphs, bullet points, and tables.
- **Text Sanitization**: Normalize Unicode, strip excessive whitespace, and preserve section headers.

```python
import fitz  # PyMuPDF
import docx
from typing import Dict, Any

def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    doc = fitz.open(file_path)
    full_text = []
    page_count = len(doc)
    has_images = False
    
    for page_num in range(page_count):
        page = doc[page_num]
        full_text.append(page.get_text())
        if len(page.get_images()) > 0:
            has_images = True
            
    doc.close()
    return {
        "text": "\n".join(full_text),
        "page_count": page_count,
        "has_images": has_images
    }

def extract_text_from_docx(file_path: str) -> Dict[str, Any]:
    doc = docx.Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return {
        "text": "\n".join(paragraphs),
        "page_count": 1,
        "has_images": False
    }
```

#### Step 2.2: Deterministic ATS Audit (`backend/app/services/ats_audit.py`)
Checks formatting compliance without needing an LLM:
- Length check (1-2 pages ideal; penalty for >3 pages).
- Essential contact presence (Email, Phone, LinkedIn, GitHub).
- Standard section headers detection (Experience, Education, Skills, Summary, Projects).
- Action verb and measurable metrics detection (percentages, dollar amounts, metrics).

---

### STAGE 3: AI Intelligence Engine & Semantic Scoring

#### Step 3.1: LLM Service Integration (`backend/app/services/ai_service.py`)
Implements structured JSON output for both Gemini and OpenAI:

```python
import json
from app.core.config import settings

def analyze_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    prompt = f"""
You are an expert ATS and Senior Technical Hiring Manager.
Analyze the following resume against the job description.

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Respond ONLY with a valid JSON object matching this schema:
{{
  "candidate_name": "string",
  "candidate_email": "string",
  "candidate_phone": "string",
  "summary": "string",
  "skills_score": 85,
  "experience_score": 80,
  "formatting_score": 90,
  "overall_ats_score": 83,
  "matched_skills": ["Python", "FastAPI", "React", "Docker"],
  "missing_skills": ["Kubernetes", "Redis", "GraphQL"],
  "strengths": ["Clear quantification of metrics", "Strong full-stack experience"],
  "weaknesses": ["Lacks container orchestration mentions", "Summary is slightly verbose"],
  "recommendations": [
    {{
      "category": "Impact",
      "priority": "High",
      "issue": "Bullet point lacks metrics",
      "suggestion": "Rewrite 'Worked on APIs' to 'Engineered 12+ FastAPI endpoints reducing response latency by 35%'"
    }}
  ]
}}
"""
    # Call Gemini or OpenAI based on settings.AI_PROVIDER
    # If API fails or key is missing, return a deterministic fallback analysis
```

#### Step 3.2: Composite Scoring Formula (`backend/app/services/scoring.py`)
Combines deterministic audit score with semantic AI score:
$$\text{Overall ATS Score} = (0.35 \times \text{Skills}) + (0.30 \times \text{Experience}) + (0.20 \times \text{Semantic Match}) + (0.15 \times \text{Formatting})$$

---

### STAGE 4: Backend REST APIs & Persistence

#### Step 4.1: Database Models (`backend/app/models/models.py`)
- `Resume`: stores file metadata, hash (SHA-256), and raw extracted text.
- `JobDescription`: stores target role title and description text.
- `Analysis`: stores scores (overall, skills, experience, formatting), JSON summary, matched/missing skills, and recommendations.

#### Step 4.2: Endpoints Implemented
1. `POST /api/v1/resumes/upload`:
   - Validates file extension (`.pdf`, `.docx`) and file size limit (<10MB).
   - Computes SHA-256 hash to prevent duplicate parsing.
   - Extracts raw text and stores metadata in SQLite.
2. `POST /api/v1/analyses/evaluate`:
   - Takes `resume_id` and `job_description_text`.
   - Runs AI and deterministic scoring.
   - Saves results into SQLite database and returns the full analysis response.
3. `GET /api/v1/analyses/{analysis_id}`:
   - Fetches cached analysis.
4. `GET /api/v1/analyses/history`:
   - Returns chronological list of all previous evaluations.
5. `POST /api/v1/copilot/rewrite-bullet`:
   - Input: raw bullet point.
   - Output: 3 high-impact variants structured with the Google XYZ formula.
6. `POST /api/v1/copilot/interview-prep`:
   - Generates 5 technical and behavioral questions tailored to candidate's missing skills.

---

### STAGE 5: Interactive React Frontend Dashboard

#### Step 5.1: API Service Layer (`frontend/src/services/api.ts`)
Configured with Axios, base URL `http://127.0.0.1:8000/api/v1`, and error handling.

#### Step 5.2: Core UI Components
1. **`Navbar.tsx`**: Header with logo, status badge ("FastAPI Connected"), and links to Analyzer and History.
2. **`FileUpload.tsx`**: Drag-and-drop zone using standard HTML5 drag events with instant size checking, upload animation, and file details preview.
3. **`JobInput.tsx`**: Target job description input area with quick-fill sample presets (e.g. "Full Stack Developer", "Data Scientist", "DevOps Engineer").
4. **`ScoreGauge.tsx`**: Dynamic SVG radial progress ring with animated stroke offset and color gradient:
   - 🟢 Green (>80%): ATS Optimized
   - 🟡 Yellow (60-79%): Good, Needs Minor Tweaks
   - 🔴 Red (<60%): Needs Significant Optimization
5. **`SkillsMatrix.tsx`**: Visual chips with tab filtering (`All`, `Matched`, `Missing`). Green badges for matched skills, amber/red badges for missing skills with "+ Add to Resume" suggestions.
6. **`FeedbackList.tsx`**: Prioritized recommendations (High, Medium, Low) with clear rationale and concrete action steps.
7. **`BulletRewriter.tsx`**: Interactive career copilot drawer where users paste weak resume bullets and receive 3 rewritten, high-impact STAR variants with a 1-click copy button.

---

### STAGE 6: End-to-End Verification & Testing

#### Step 6.1: Backend Pytest Suite (`backend/tests/test_api.py`)
Run automated tests:
```powershell
cd backend
pytest tests/
```
Tests verify:
- Health check returns `200 OK`.
- Document parser rejects invalid file extensions.
- ATS scoring algorithm accurately calculates composite weights.
- Bullet rewriter generates structured XYZ outputs.

#### Step 6.2: Complete Run Verification
1. Open Terminal 1:
   ```powershell
   cd backend
   python server.py
   ```
2. Open Terminal 2:
   ```powershell
   cd frontend
   npm run dev
   ```
3. Open `http://localhost:5173` in browser:
   - Upload sample PDF/DOCX resume.
   - Select or paste a Job Description.
   - Click **"Analyze Resume"**.
   - Verify animated ATS score, matched/missing skill chips, and recommendations.
   - Use the **Bullet Rewriter** tool to polish an experience bullet.

---

## 5. Verification Checklist

| Milestone | Expected Result | Verified |
| :--- | :--- | :---: |
| **Backend Boot** | `python server.py` starts server on `http://127.0.0.1:8000` | [ ] |
| **Swagger Access** | `http://127.0.0.1:8000/docs` loads interactive OpenAPI UI | [ ] |
| **Frontend Boot** | `npm run dev` starts React Vite on `http://localhost:5173` | [ ] |
| **Resume Upload** | PDF/DOCX uploaded without crashes; text accurately extracted | [ ] |
| **Database Persistence** | Data saved in `resume_analyzer.db` with WAL mode | [ ] |
| **ATS Scoring** | Overall score (0-100) computed with category breakdown | [ ] |
| **Skills Extraction** | Matched and missing skills clearly separated and tagged | [ ] |
| **AI Copilot** | Bullet rewriter produces STAR/XYZ metrics-driven alternatives | [ ] |
