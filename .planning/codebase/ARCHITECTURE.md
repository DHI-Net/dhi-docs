# Architecture

**Analysis Date:** 2026-04-22

## Pattern Overview

**Overall:** Pipeline + Read-through Cache (Demo/Prototype Phase)

**Key Characteristics:**
- Two-stage data pipeline: PDF → xlsx (conversion scripts) → JSON (extractor)
- Backend loads all farm/month data into memory at startup via a single in-memory cache dict
- Frontend is a single-page application served as a static file, currently embedded with pre-computed data in `window.__DHI_DATA__`
- No database layer yet — all data read directly from xlsx files on disk
- Two parallel data paths: pre-arranged `DHI整理.xlsx` files vs. raw PDF-converted `_DHI.xlsx` files

## Layers

**Conversion Layer (offline tooling):**
- Purpose: Convert raw PDF reports to structured xlsx files
- Location: `src/`
- Contains: `milk_pdf_to_xlsx.py` (milk quality converter), `performance_pdf_to_xlsx.py` (performance converter + PDF-pair merger)
- Depends on: `pdfplumber`, `pandas`, `openpyxl`, optionally `tkinter` for GUI file picker
- Used by: Human operator (GUI) or future automated import service

**Data Extraction Layer:**
- Purpose: Read xlsx files from disk and normalize to Python dicts / JSON-serializable structures
- Location: `backend/extractor.py`
- Contains: Farm file registry (`FARM_FILES`, `CONVERTED_FILES`), sheet parsers (`extract_summary`, `extract_cows`, `extract_converted_cows`), label normalization map (`LABEL_KEY`), helper converters (`to_float`, `to_str`, `parse_date`)
- Depends on: `pandas`, `openpyxl`, `numpy`
- Used by: `backend/main.py` at startup via `load_all_data()`

**API Layer:**
- Purpose: Expose farm/month data as REST endpoints; serve frontend static files
- Location: `backend/main.py`
- Contains: FastAPI app, CORS middleware, 4 GET endpoints, startup cache loader, static file mount
- Depends on: `extractor.py`, `fastapi`, `uvicorn`
- Used by: Frontend (via fetch) or direct API consumers

**Frontend Layer:**
- Purpose: Interactive dashboard for viewing DHI data per farm and month
- Location: `frontend/`
- Contains: `index.html` (single-file Vue 3 + ECharts + Tailwind app), `data.js` (large embedded static dataset)
- Depends on: Vue 3 (CDN), ECharts (CDN), Tailwind CSS (CDN)
- Used by: End users (farmers, consultants, admin)

## Data Flow

**PDF-to-Web Pipeline:**

1. Operator selects paired PDFs (milk quality + performance) via GUI (`src/performance_pdf_to_xlsx.py main()`)
2. `convert_pair()` calls `milk_pdf_to_xlsx.convert_pdfs()` for milk quality → produces `*_牛乳品質檢驗報告.xlsx`
3. `parse_performance_pdf()` parses performance PDF → produces a DataFrame
4. `merge_milk_performance()` joins both on `farm_id` → combined DataFrame
5. `export_xlsx()` writes `*_DHI.xlsx` with sheets: `合併1`, `性能檢定`, `明細`
6. Consultant manually produces `*_DHI整理.xlsx` (the curated summary workbook)
7. On backend startup, `load_all_data()` reads both `DHI整理.xlsx` files and raw `_DHI.xlsx` converted files
8. Frontend fetches `/api/farms/{farm}/{month}` and renders charts and tables

**State Management:**
- Backend: module-level `_DATA: dict | None` — populated once on first request, never invalidated
- Frontend: Vue 3 reactive data, populated from `window.__DHI_DATA__` (embedded) or API fetch

## Key Abstractions

**Farm File Registry:**
- Purpose: Maps farm name → list of (month_key, Path) tuples pointing to xlsx files on disk
- Examples: `backend/extractor.py` (`FARM_FILES`, `CONVERTED_FILES` dicts)
- Pattern: Hard-coded dict; adding a new farm or month requires editing the source file

**Label Normalization Map (`LABEL_KEY`):**
- Purpose: Translates inconsistent Chinese column headers from xlsx sheets to fixed English keys
- Examples: `backend/extractor.py` lines 43-65
- Pattern: `dict[str, str]` lookup applied during sheet parsing

**Cow Record Schema:**
- Purpose: Canonical per-cow data structure output by both `extract_cows()` and `extract_converted_cows()`
- Fields: `farm_id`, `national_id`, `milk`, `fat`, `protein`, `lactose`, `snf`, `ts`, `scc`, `urea`, `citric`, `pf`, `casein`, `ffa`, `sat_fa`, `unsat_fa`, `acetone`, `bhb`, `notes`, `alerts`, `parity`, `calving_date`, `dim`, `open_days`, `services`, `group`
- Pattern: Plain Python dict; same structure regardless of whether data came from curated or converted xlsx

**Month Snapshot:**
- Purpose: Groups all data for one farm-month into a single JSON object
- Structure: `{ measurement_date, summary: { current, comparison }, cows: [...] }`
- Pattern: Returned by all `/api/farms/{farm}/{month}` endpoints

## Entry Points

**PDF Conversion (milk quality):**
- Location: `src/milk_pdf_to_xlsx.py` — `main()` / `convert_pdfs()`
- Triggers: GUI file picker (Windows tkinter) or direct `convert_pdfs([Path(...)])` call
- Responsibilities: Parse PDF text, extract tabular rows, write `明細` sheet xlsx, replace `#` chars, force numeric cell format

**PDF Conversion (performance + merge):**
- Location: `src/performance_pdf_to_xlsx.py` — `main()` / `convert_pair()`
- Triggers: GUI file picker (paired PDFs) or direct `convert_pair(milk_pdf, perf_pdf)` call
- Responsibilities: Parse both PDFs, merge on farm_id, classify heifer/multi-parity, output 3-sheet xlsx

**Backend API Server:**
- Location: `backend/main.py`
- Triggers: `uvicorn backend.main:app` from project root
- Responsibilities: Load all xlsx data into memory, expose REST API, serve `frontend/index.html` and static files

**Frontend SPA:**
- Location: `frontend/index.html`
- Triggers: Browser navigation to `/` or direct file open
- Responsibilities: Render farm selector, month selector, summary cards, ECharts trend charts, per-cow data table

## Error Handling

**Strategy:** Fail-soft with warnings to stdout; missing files are skipped, malformed rows are silently dropped

**Patterns:**
- `extractor.py` `_read_sheet()`: wraps `pd.read_excel` in `try/except`, returns `None` on failure
- `load_all_data()`: checks `path.exists()` before parsing, prints `[WARN]` and continues if missing
- `to_float()` / `to_str()` / `parse_date()`: return `None` for any unparseable value rather than raising
- `parse_milk_report_pdf()` / `parse_performance_pdf()`: skip non-matching lines silently

## Cross-Cutting Concerns

**Logging:** `print()` statements only — `[OK]`, `[WARN]`, `[EMPTY]` prefixes; no structured logging framework
**Validation:** Input validation is implicit — regex row detection in PDF parsers acts as a filter; no schema enforcement on output
**Authentication:** None currently implemented; CORS is fully open (`allow_origins=["*"]`)

---

*Architecture analysis: 2026-04-22*
