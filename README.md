# AI-Powered Resume Analyzer & Career Copilot

An enterprise-grade, end-to-end career intelligence and resume optimization platform designed to evaluate resumes against modern Applicant Tracking Systems (ATS) and job descriptions with deterministic parsability checks, semantic AI scoring, and an interactive career copilot.

---

## 🌟 Key Features

- **Multi-Format Ingestion**: High-fidelity parsing of PDF and DOCX documents extracting text, contact details, sections, and metadata.
- **Dual-Engine Evaluation**:
  - **Deterministic ATS Audit**: Evaluates formatting compliance (page count, font anomalies, tables, multi-column reading order, essential contact fields).
  - **Semantic AI Scoring**: Deep LLM-powered matching against job descriptions calculating skills match, experience alignment, and missing keyword identification.
- **Interactive Career Copilot**:
  - **STAR / Google XYZ Bullet Enhancer**: Transforms weak resume bullet points into high-impact, quantified achievement statements (*"Accomplished [X] as measured by [Y], by doing [Z]"*).
  - **Tailored Interview Prep**: Generates customized behavioral and technical interview questions addressing identified candidate gaps.
- **Modern User Experience**:
  - Drag-and-drop resume upload with client-side file validation.
  - Animated SVG circular score gauges with dynamic semantic coloring.
  - Matched vs. Missing skills chip matrix with 1-click recommendations.
- **Production-Grade Architecture**:
  - FastAPI asynchronous backend with Pydantic v2 schemas and automatic OpenAPI/Swagger documentation.
  - SQLite with **WAL (Write-Ahead Logging)** mode for concurrent, non-locking reads and writes.
  - SHA-256 file deduplication caching to avoid redundant LLM invocations.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | **Python 3.11+ / FastAPI** | High-performance asynchronous REST API framework |
| **Database** | **SQLite + SQLAlchemy 2.0 (WAL Mode)** | Embedded relational database with concurrent read/write optimization |
| **Frontend** | **React.js (Vite + TypeScript)** | Component-based UI with compile-time type safety |
| **Styling** | **Tailwind CSS + Lucide Icons** | Modern design tokens and accessible iconography |
| **Document Processing** | **PyMuPDF (`fitz`) + python-docx** | Robust PDF & DOCX text and layout coordinate extraction |
| **AI Orchestration** | **Google Gemini API / OpenAI API** | Structured JSON extraction, semantic matching & STAR bullet rewrites |

---

## 📁 Clean Directory Structure

```
resume_analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app instance & middleware
│   │   ├── core/config.py       # Pydantic v2 application settings
│   │   ├── db/session.py        # SQLite engine with WAL mode & sessionmaker
│   │   ├── models/models.py     # SQLAlchemy ORM models
│   │   ├── schemas/schemas.py   # Request and response schemas
│   │   ├── services/
│   │   │   ├── parser.py        # PDF & DOCX extraction engine
│   │   │   ├── ats_audit.py     # Rule-based formatting & layout audit
│   │   │   ├── ai_service.py    # LLM structured prompt engine
│   │   │   └── scoring.py       # Composite ATS scoring algorithm
│   │   └── api/
│   │       ├── router.py        # Main API v1 routing hub
│   │       └── routes/          # Modular endpoints (resumes, analyses, copilot)
│   ├── tests/                   # Pytest automated test suite
│   ├── uploads/                 # Local uploaded resume vault (gitignored)
│   ├── server.py                # Backend entrypoint: python server.py
│   └── requirements.txt         # Pinned Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components (Upload, Gauges, Copilot)
│   │   ├── services/api.ts      # Axios backend API client
│   │   ├── types/index.ts       # TypeScript interfaces matching backend models
│   │   ├── App.tsx              # Main dashboard view & layout state
│   │   └── main.tsx             # React entry point
│   ├── package.json             # Frontend dependencies & scripts
│   └── vite.config.ts           # Vite build configuration
├── .gitignore                   # Comprehensive ignores (venv, node_modules, db)
├── .env.example                 # Template environment variables
├── .env                         # Local environment secrets (gitignored)
├── plan.md                      # Detailed architectural blueprint
├── implementation_guide.md      # Step-by-step developer implementation guide
├── changelog.md                 # Semantic versioning & change history tracker
└── README.md                    # Project documentation & quickstart
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher & npm
- Git

### 1. Backend Setup & Launch
```powershell
# Navigate to the backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows (or 'source venv/bin/activate' on macOS/Linux)

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python server.py
```

- **API Server Running**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

### 2. Frontend Setup & Launch
Open a second terminal:
```powershell
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

- **Application Dashboard**: [`http://localhost:5173`](http://localhost:5173)

### 3. Sample Resumes for Testing
6 realistic industry-standard test resumes in `.pdf` and `.docx` formats are ready in [`sample_resumes/`](file:///C:/Users/HACKATHIN29/Desktop/Shailesh%20Yadav%20Hack/sample_resumes):
- `1_Senior_FullStack_Engineer.pdf` (High-score Full Stack Engineer)
- `2_Data_Scientist_ML_Engineer.pdf` (Machine Learning / AI Scientist)
- `3_DevOps_Cloud_Architect.docx` (Cloud & Kubernetes Architect in Word format)
- `4_Junior_Frontend_Developer.docx` (Frontend Developer in Word format)
- `5_Product_Manager_Tech.pdf` (Metrics-driven Product Manager)
- `6_Needs_Improvement_EdgeCase.pdf` (Edge case testing warnings for missing headers & contacts)

---

## 🧭 Project Roadmap & Stage Tracker

| Stage | Milestone | Status | Details |
| :--- | :--- | :---: | :--- |
| **Stage 1** | **Foundation & Scaffolding** | ✅ Completed | FastAPI, `server.py`, SQLite WAL mode, models, React Vite app, clean config |
| **Stage 2** | **Document Ingestion & ATS Audit** | ✅ Completed | `PyMuPDF` & `python-docx` parsing, SHA-256 caching, deterministic ATS audit |
| **Stage 3** | **AI Engine & Semantic Scoring** | 🔄 Next Up | LLM structured JSON integration, composite score calculations |
| **Stage 4** | **REST APIs & SQLite Persistence** | ⏳ Queued | Upload, evaluate, history, and copilot endpoints with caching |
| **Stage 5** | **Interactive React Frontend** | ⏳ Queued | File upload, animated score gauges, skills matrix, copilot drawer |
| **Stage 6** | **Testing & Production Polish** | ⏳ Queued | `pytest` test suite, verification checklist, end-to-end demo |

---

## 📚 Reference Documentation

- [Plan & Architectural Specification](file:///C:/Users/HACKATHIN29/Desktop/Shailesh%20Yadav%20Hack/plan.md): Architectural decisions, data models, and UX principles.
- [Implementation Guide](file:///C:/Users/HACKATHIN29/Desktop/Shailesh%20Yadav%20Hack/implementation_guide.md): Code examples, command references, and stage breakdowns.
- [Changelog](file:///C:/Users/HACKATHIN29/Desktop/Shailesh%20Yadav%20Hack/changelog.md): Release history and upcoming milestone tracking.
