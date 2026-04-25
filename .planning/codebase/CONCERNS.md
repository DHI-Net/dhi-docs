# Concerns & Technical Debt

## Critical — Must Address Before Production

### No Authentication or Authorization
- **File:** `backend/main.py`
- All API endpoints are public — any client can read all farm data
- CORS is `allow_origins=["*"]` — no origin restriction
- No user roles (酪農戶 / 顧問 / 管理者) are enforced anywhere
- Admin password protection required by spec (`CLAUDE.md`) but not yet implemented

### Data in Version Control Risk
- `data/` directory contains ~85 PDFs and ~183 Excel files — likely to be accidentally committed
- No `.gitignore` exists yet — `git add .` would commit all farm data
- Some data may contain personally identifiable cow/farm information

### Demo Architecture Deployed as Spec
- `backend/extractor.py` hardcodes all farm → file path mappings in `FARM_FILES` dict (lines 22-38)
- No database — data is read directly from Excel files at request time
- Entire dataset loaded into memory on first request (`_DATA` global cache)
- No import pipeline in the web system — file paths must be edited in source code to add new data

## High — Technical Debt

### Hardcoded File Paths
- `FARM_FILES` and `CONVERTED_FILES` in `backend/extractor.py` must be manually updated for each new month/farm
- `FRONTEND = Path(__file__).parent.parent / "frontend"` assumes specific directory structure
- `BASE_DIR = Path(__file__).parent.parent` — fragile if entry point changes

### Positional Column Parsing
- `extract_cows()` uses `row.iloc[0]`, `row.iloc[1]`, ... `row.iloc[25]` — column index positions hardcoded
- Sheet structure changes in `DHI整理.xlsx` would silently produce wrong data with no error
- `extract_summary()` has hardcoded row range `range(4, min(25, len(df)))` — may miss rows if sheet grows

### Inconsistent Data Organization
- 顏御哲 farm data has no farm prefix directory (files at `data/顏御哲_2026.1/` not `data/xx.顏御哲/`)
- 吳龍廷 month 3 file is at `data/94.吳龍廷/吳龍廷115.3月份_DHI整理.xlsx` (not in a subdirectory)
- `顏御哲115.3月份_DHI整理.xlsx` exists at `data/` top level (orphaned)
- Month key formats inconsistent: `"2026.1"` vs `"2026.02"` (zero-padded for 林家和 only)

### Regex Mismatch for Farm IDs
- `ROW_START` in `milk_pdf_to_xlsx.py` matches IDs like `11M2459` or `2N1`
- `FARM_NORMALIZE` removes letter prefix but `normalize_farm_id()` may not match same patterns
- `ROW_B` in `performance_pdf_to_xlsx.py` expects `\d{3,6}` — may not match all farm ID formats

### Date Conversion Assumption
- `roc_to_iso()`: `2000 + YY` — breaks for ROC years ≥ 100 (i.e., year 2100+)
- Current ROC year 115 = 2026 is fine, but assumption is fragile for general use

## Medium — Missing Infrastructure

### No Docker Configuration
- `CLAUDE.md` specifies Docker Compose for deployment migration from WSL to new host
- No `Dockerfile`, no `docker-compose.yml` exist yet

### No Admin Interface
- No way to add new farms, new months, or manage data through the web UI
- Important management functions required to have password protection (per spec) — not started

### Single Massive API Endpoint
- `/api/data` returns all farms × all months in one response
- Will not scale as data grows — no pagination or filtering

### No Import/Upload Pipeline
- PDF upload + conversion workflow not connected to web system
- `src/milk_pdf_to_xlsx.py` and `src/performance_pdf_to_xlsx.py` are standalone desktop tools
- No web-based trigger for PDF → xlsx → database pipeline

## Low — Code Quality

### Warning Suppression
- `warnings.filterwarnings("ignore")` in `backend/extractor.py` — hides openpyxl warnings that may indicate real issues

### No Input Validation
- FastAPI endpoints accept any string for `farm` and `month` path parameters
- Only validation is dict key lookup + 404 response

### No Logging
- Only `print()` statements for status — no structured logging
- No request logging, no error tracking

### `吳炎珍` in CONVERTED_FILES
- `backend/extractor.py` line 250 has `"吳炎珍"` hardcoded in `CONVERTED_FILES` dict
- Not listed as one of the 3 known farms in `CLAUDE.md` — may be a test/temporary entry