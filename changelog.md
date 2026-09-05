# Changelog

All notable changes to the **AI-Powered Resume Analyzer** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned for Stage 3: AI Intelligence Engine & Semantic Scoring
- [ ] Structured LLM service (Gemini / OpenAI API) with Pydantic JSON schema constraints.
- [ ] Weighted ATS scoring formula (35% Skills, 30% Experience, 20% Semantic Relevance, 15% Formatting).
- [ ] Keyword matching and skill gap identification.

### Planned for Stage 4: Backend REST APIs & Persistence
- [ ] SQLite database models (`Resume`, `JobDescription`, `Analysis`, `Recommendation`).
- [ ] Job evaluation endpoint (`POST /api/v1/analyses/evaluate`).
- [ ] Historical records endpoint (`GET /api/v1/analyses/history`).
- [ ] Career Copilot endpoints: STAR-method bullet rewriter (`POST /api/v1/copilot/rewrite-bullet`) and interview prep questions (`POST /api/v1/copilot/interview-prep`).

### Planned for Stage 5: High-End React Frontend Dashboard
- [ ] Drag-and-drop resume upload zone with client validation.
- [ ] Job description input with sample presets.
- [ ] Animated circular SVG ATS score gauge with status coloring.
- [ ] Interactive skills matrix (matched vs missing skill chips).
- [ ] Interactive STAR bullet rewriter copilot drawer with one-click copy.

### Planned for Stage 6: Testing & Quality Assurance
- [ ] Pytest suite for parser edge cases, scoring calculations, and API routes.
- [ ] End-to-end integration and user verification.

---

## [0.3.0] - 2026-09-05

### Added (Stage 2: Resume Ingestion & Deterministic ATS Audit Completed)
- **Document Ingestion Service (`backend/app/services/parser.py`)**:
  - `PyMuPDF` (`fitz`) multi-page text and coordinate extraction engine.
  - `python-docx` Word extraction engine extracting paragraphs, tables, and lists.
  - SHA-256 hash generation for instant file deduplication and response caching.
  - Robust file validation handling file sizes up to 10MB and rejecting unsearchable/scanned PDFs or invalid MIME types.
- **Deterministic ATS Parsability Auditor (`backend/app/services/ats_audit.py`)**:
  - Regex-based contact extraction (Email, reachable Phone, LinkedIn URL, GitHub URL).
  - Standard ATS section header detection (Experience, Education, Skills, Summary, Projects, Certifications).
  - Quantified achievements and metric counter (`%`, `$`, multiplier patterns).
  - Action verb density analyzer matching against 75+ industry action verbs.
  - Quantitative 0-100 ATS Formatting Score calculation with prioritized recommendations.
- **Backend API Endpoints (`backend/app/api/routes/resumes.py`)**:
  - `POST /api/v1/resumes/upload`: Multipart upload with SHA-256 caching and immediate audit return.
  - `GET /api/v1/resumes/{id}/audit`: Endpoint to fetch granular ATS breakdown for any stored resume.
- **Frontend File Upload Component (`frontend/src/components/FileUpload.tsx`)**:
  - High-UX drag-and-drop resume upload zone with live validation and loading state.
  - Instant ATS Parsability Score badge, contact status pills, detected sections chips, action verbs, and prioritized formatting fixes.
- **Automated Pytest Coverage & Integration Tests (`backend/tests/test_api.py`)**:
  - Added unit and integration tests for parsers, deterministic ATS scoring, extension rejection, and SHA-256 caching.
  - Added full test suite verifying all 6 industry-standard sample resumes (`.pdf` and `.docx`).
- **Sample Test Resumes (`sample_resumes/` & `backend/tests/sample_resumes/`)**:
  - `1_Senior_FullStack_Engineer.pdf` (High-score ATS optimized PDF)
  - `2_Data_Scientist_ML_Engineer.pdf` (High-score ML/AI specialist PDF)
  - `3_DevOps_Cloud_Architect.docx` (High-score Cloud/Kubernetes Word document)
  - `4_Junior_Frontend_Developer.docx` (Mid-level React/TypeScript Word document)
  - `5_Product_Manager_Tech.pdf` (Metrics-driven Product Management PDF)
  - `6_Needs_Improvement_EdgeCase.pdf` (Low-score edge case with missing headers & contact fields)

## [0.2.0] - 2026-09-05

### Added (Stage 1: Foundation & Scaffolding Completed)
- **Root Configuration**: Standardized `.gitignore`, `.env.example`, and local `.env` with configurable parameters for AI providers and SQLite database path.
- **Backend Architecture (`backend/`)**:
  - `backend/server.py`: Dedicated entrypoint running Uvicorn at `http://127.0.0.1:8000` with Swagger UI at `/docs`.
  - `backend/app/main.py`: Configured FastAPI application with CORS middleware, health check endpoint (`/health`), and `/api/v1` router.
  - `backend/app/core/config.py`: Pydantic settings loading environment configurations and auto-creating upload directories.
  - `backend/app/db/session.py`: SQLite engine configured with **WAL mode** (`PRAGMA journal_mode=WAL;`), synchronous=NORMAL, foreign keys enabled, and sessionmaker.
  - `backend/app/models/models.py`: SQLAlchemy database models (`Resume`, `JobDescription`, `Analysis`) with foreign key constraints, timestamps, and cascade deletions.
  - `backend/app/schemas/schemas.py`: Pydantic v2 schemas for health status, resumes, job descriptions, analyses, and career copilot requests/responses.
  - `backend/app/api/router.py` & routes (`resumes.py`, `analyses.py`, `copilot.py`): Clean modular routing for resume listing, evaluation history, and interactive STAR/XYZ bullet point rewriting.
  - `backend/tests/test_api.py`: Automated Pytest suite covering root endpoints, health status, and copilot endpoints.
  - `backend/requirements.txt`: Clean, non-redundant dependency manifest.
- **Frontend Architecture (`frontend/`)**:
  - Initialized modern React 18 + Vite + TypeScript application.
  - Configured Tailwind CSS with custom brand palette and typography.
  - Setup typed API service layer in `frontend/src/services/api.ts` connecting to FastAPI backend.
  - Built sticky header component `frontend/src/components/Navbar.tsx` featuring real-time backend health ping indicator and Swagger docs shortcut.
  - Built interactive welcome dashboard `frontend/src/App.tsx` featuring an interactive Career Copilot sandbox to test bullet enhancement immediately against the live backend API.

## [0.1.0] - 2026-09-05

### Added
- **Project Architectural Plan (`plan.md`)**: Comprehensive senior engineering specification covering UX-first design, system architecture, database schema, and staged roadmap.
- **End-to-End Implementation Guide (`implementation_guide.md`)**: Detailed step-by-step developer guide with exact code snippets, execution commands (`python server.py` for FastAPI Swagger, `npm run dev` for React), zero-redundancy directory layout, and verification checkpoints.
- **Project Documentation (`README.md`)**: Project overview, architectural stack, quick start guide, API documentation links, and stage tracker.
- **Project Changelog (`changelog.md`)**: Initialized changelog to record all past, present, and future implementation milestones.
