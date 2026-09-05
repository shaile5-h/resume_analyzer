# Changelog

All notable changes to the **AI-Powered Resume Analyzer** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned for Stage 1: Foundation & Scaffolding
- [ ] Initialize root configuration (`.gitignore`, `.env.example`, `.env`).
- [ ] Initialize `backend/` modular structure (`app/core/`, `app/db/`, `app/models/`, `app/schemas/`, `app/services/`, `app/api/`).
- [ ] Setup `backend/requirements.txt` and virtual environment (`venv`).
- [ ] Create `backend/server.py` entrypoint configured to run FastAPI with Uvicorn on `http://127.0.0.1:8000`.
- [ ] Setup SQLite engine with WAL (Write-Ahead Logging) mode and foreign key constraints in `backend/app/db/session.py`.
- [ ] Initialize `frontend/` (React + TypeScript + Vite + Tailwind CSS + Lucide Icons).

### Planned for Stage 2: Resume Ingestion & Deterministic ATS Audit
- [ ] Multi-format text extraction pipeline (`PyMuPDF` for PDF, `python-docx` for Word).
- [ ] Deterministic ATS parsability audit (table traps, multi-column reading orders, contact info checks).
- [ ] File upload API endpoint (`POST /api/v1/resumes/upload`) with SHA-256 hash deduplication.

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

## [0.1.0] - 2026-09-05

### Added
- **Project Architectural Plan (`plan.md`)**: Comprehensive senior engineering specification covering UX-first design, system architecture, database schema, and staged roadmap.
- **End-to-End Implementation Guide (`implementation_guide.md`)**: Detailed step-by-step developer guide with exact code snippets, execution commands (`python server.py` for FastAPI Swagger, `npm run dev` for React), zero-redundancy directory layout, and verification checkpoints.
- **Project Documentation (`README.md`)**: Project overview, architectural stack, quick start guide, API documentation links, and stage tracker.
- **Project Changelog (`changelog.md`)**: Initialized changelog to record all past, present, and future implementation milestones.
