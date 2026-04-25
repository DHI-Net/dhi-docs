# External Integrations

**Analysis Date:** 2026-04-22

## APIs & External Services

**CDN-delivered Frontend Libraries:**
- ECharts 5.4.3 - Chart rendering
  - Source: `https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js`
  - Auth: None (public CDN)
- Vue 3.4.21 - UI framework
  - Source: `https://cdn.jsdelivr.net/npm/vue@3.4.21/dist/vue.global.prod.js`
  - Auth: None (public CDN)
- Tailwind CSS - Styling
  - Source: `https://cdn.tailwindcss.com`
  - Auth: None (public CDN)

**Note:** All three CDN dependencies are loaded in `frontend/index.html` lines 9-13. In the planned Vite build these would become npm packages installed locally, eliminating the CDN dependency.

## Data Storage

**Databases:**
- None currently. All data is read directly from `.xlsx` files on disk and cached in memory at startup by `backend/extractor.py` → `load_all_data()`.

**Planned:**
- SQLite (development) → PostgreSQL (production)
  - Connection: environment variable not yet defined
  - ORM: SQLAlchemy (planned, not yet implemented)
  - Tables planned: farms, months, cows (per `draw_arch.py` architecture diagram)

**File Storage (current data source):**
- Local filesystem under `data/` directory
  - `data/94.吳龍廷/` — farm 吳龍廷 monthly folders with `DHI整理.xlsx` files
  - `data/06.林家和/` — farm 林家和 monthly folders
  - `data/顏御哲_*/` — farm 顏御哲 monthly folders
  - `data/20260108145639QF_DHI.xlsx` — converted milk-quality xlsx (direct PDF output)
- File paths are hardcoded in `backend/extractor.py` in `FARM_FILES` and `CONVERTED_FILES` dicts

**Caching:**
- In-process Python dict (`_DATA` global in `backend/main.py`) — populated once at first request, lives for server lifetime. No Redis or external cache.

## Authentication & Identity

**Auth Provider:**
- None currently. All API endpoints are fully public with no authentication.
- CORS is open (`allow_origins=["*"]` in `backend/main.py` line 20).

**Planned:**
- JWT or session-based auth (per architecture diagram `draw_arch.py`)
- Three roles: 酪農戶 (farmer), 顧問 (consultant), 管理者 (admin)
- Admin functions require password protection with anti-forget mechanism

## Monitoring & Observability

**Error Tracking:**
- None. Errors print to stdout via `print(f"[WARN] 找不到檔案: {path}")` in `backend/extractor.py`.

**Logs:**
- Python `print()` statements only; no structured logging framework.

## CI/CD & Deployment

**Hosting:**
- Development: WSL2 local server (uvicorn)
- Production (planned): Docker Compose on a new Linux host
  - Planned containers: backend (FastAPI), frontend (nginx), PostgreSQL

**CI Pipeline:**
- None detected. No `.github/`, `.gitlab-ci.yml`, or similar config.

## Webhooks & Callbacks

**Incoming:**
- None currently.

**Outgoing:**
- None currently.

## PDF Conversion Pipeline

**Internal integration (not external, but a fixed boundary):**
- `src/milk_pdf_to_xlsx.py` — converts 牛乳品質檢驗報告 PDFs to `.xlsx`
  - Invoked manually via tkinter GUI or CLI (`python milk_pdf_to_xlsx.py`)
  - Input: PDF files selected interactively
  - Output: same-named `.xlsx` alongside each PDF
  - This file must NOT be modified (project constraint per `CLAUDE.md`)
- A second converter for 性能檢定月報表 PDFs is planned but not yet implemented

**PDF naming convention (per `CLAUDE.md`):**
- First 8 chars = date (YYYYMMDD or ROC calendar format)
- Remainder = case ID (案件編號)
- PDFs must appear in pairs (性能檢定 + 牛乳品質) per farm per month to be valid for conversion

## Environment Configuration

**Required env vars:**
- None currently defined or consumed by the application.

**Secrets location:**
- No secrets management in place. No `.env` file detected.

---

*Integration audit: 2026-04-22*
