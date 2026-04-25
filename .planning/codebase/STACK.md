# Technology Stack

**Analysis Date:** 2026-04-22

## Languages

**Primary:**
- Python 3.13 - Backend API server, PDF conversion scripts, data extraction

**Secondary:**
- JavaScript (ES2022, no transpile) - Frontend Vue 3 application (CDN-loaded, no build step currently)
- HTML/CSS - Single-page frontend (`frontend/index.html`)

## Runtime

**Environment:**
- CPython 3.13.9 on WSL2 (Linux 5.15, Microsoft)

**Package Manager:**
- pip (no lockfile present; `backend/requirements.txt` pins minimum versions with `>=`)
- Lockfile: missing (pip freeze not captured)

## Frameworks

**Core:**
- FastAPI 0.136.0 - REST API server (`backend/main.py`)
- Uvicorn 0.44.0 (standard extras) - ASGI server; run with `uvicorn main:app`

**Frontend (current, CDN-loaded):**
- Vue 3.4.21 - Reactive UI framework, loaded via `cdn.jsdelivr.net`
- ECharts 5.4.3 - Chart library for data visualizations, loaded via `cdn.jsdelivr.net`
- Tailwind CSS (latest) - Utility-first CSS, loaded via `cdn.tailwindcss.com`

**Frontend (planned, not yet implemented):**
- Vue 3 + Vite - Proper build pipeline (see `draw_arch.py` architecture diagram)
- Vue Router + Pinia/Vuex - Routing and state management

**PDF Conversion:**
- pdfplumber 0.11.9 - Extracts tabular text from milk-quality PDFs (`src/milk_pdf_to_xlsx.py`)
- tkinter (stdlib) - GUI file picker for standalone PDF converter script

**Data Processing:**
- pandas 2.3.4 - DataFrame operations in extractor and converter
- numpy 1.26.x - Numerical helpers (NaN checks)
- openpyxl 3.1.5 - Read/write `.xlsx` files

**Testing:**
- Not detected (no test files, no pytest/unittest config)

**Build/Dev:**
- matplotlib - Architecture diagram generator only (`draw_arch.py`); not a runtime dependency

## Key Dependencies

**Critical:**
- `fastapi>=0.111.0` - API layer; all endpoints defined in `backend/main.py`
- `uvicorn[standard]>=0.29.0` - Required to serve FastAPI
- `pdfplumber>=0.11.9` - Core of the milk-quality PDF-to-xlsx pipeline (`src/milk_pdf_to_xlsx.py`); this file must not be modified
- `pandas>=2.2.0` - All data extraction logic in `backend/extractor.py`
- `openpyxl>=3.1.0` - Reading `DHI整理.xlsx` and `月DHI.xlsx` files

**Infrastructure:**
- `python-multipart>=0.0.9` - Needed for FastAPI form/file uploads (future upload pipeline)
- `numpy>=1.26.0` - Used for NaN detection in `backend/extractor.py`

## Configuration

**Environment:**
- No `.env` file detected; no environment-variable-based configuration in current code
- All file paths are hardcoded in `backend/extractor.py` (`FARM_FILES` and `CONVERTED_FILES` dicts)
- CORS is fully open (`allow_origins=["*"]`) — development only setting

**Build:**
- No build config files (no `pyproject.toml`, `setup.cfg`, `Dockerfile`, or `docker-compose.yml` yet)
- Frontend has no bundler config (plain HTML file served as static asset via FastAPI `StaticFiles`)

## Platform Requirements

**Development:**
- WSL2 (Linux) with Python 3.13
- NotoSansCJK font at `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` (required by `draw_arch.py` only)
- No Node.js required currently (all frontend via CDN)

**Production (planned):**
- Docker Compose: backend (FastAPI/uvicorn) + frontend (nginx) + PostgreSQL containers
- Target: new Linux host; WSL2 is development-only

---

*Stack analysis: 2026-04-22*
