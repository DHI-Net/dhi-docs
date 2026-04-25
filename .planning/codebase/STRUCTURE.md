# Directory Structure

## Top-Level Layout

```
DHI_Net/
├── CLAUDE.md                        # Project specs and constraints
├── arch_diagram.png                 # Architecture diagram (image)
├── arch_diagram_preview.png         # Architecture diagram preview
├── draw_arch.py                     # Script to generate architecture diagram
├── src/                             # Standalone PDF conversion scripts (fixed)
├── backend/                         # FastAPI application
├── frontend/                        # Static HTML/JS frontend
└── data/                            # Historical DHI data files
```

## src/ — PDF Conversion Scripts (Fixed, Do Not Modify)

```
src/
├── milk_pdf_to_xlsx.py              # 牛乳品質 PDF → xlsx converter
├── performance_pdf_to_xlsx.py       # 性能檢定 PDF → xlsx converter
└── __pycache__/                     # Compiled bytecode cache
```

- These scripts are **standalone** — they use tkinter GUI dialogs for file selection
- `milk_pdf_to_xlsx.py` is frozen; do not modify its conversion logic
- `performance_pdf_to_xlsx.py` is the second converter (newer)

## backend/ — FastAPI Application

```
backend/
├── main.py                          # FastAPI app entry point, API routes, static file serving
├── extractor.py                     # Excel data extraction and normalization logic
└── requirements.txt                 # Python dependencies
```

- `main.py` — defines all API endpoints (`/api/data`, `/api/farms`, `/api/farms/{farm}/months`, `/api/farms/{farm}/{month}`)
- `extractor.py` — reads `DHI整理.xlsx` files and PDF-converted `.xlsx` files; outputs normalized JSON
- `FARM_FILES` dict in `extractor.py` hardcodes all known farm → month → file path mappings
- `CONVERTED_FILES` dict handles farms loaded from PDF-converted output (currently 吳炎珍)

## frontend/ — Static Frontend

```
frontend/
├── index.html                       # Main HTML page
└── data.js                          # JavaScript data/UI logic
```

- Served by FastAPI's `StaticFiles` mount at `/static`
- No build step required — plain HTML + JavaScript

## data/ — Historical DHI Data

```
data/
├── 06.林家和/
│   ├── 林家和_2026.02/
│   │   └── 林家和115.02月份_DHI整理.xlsx
│   ├── 林家和_2026.03/
│   │   └── 林家和115.03月份_DHI整理.xlsx
│   └── 林家和_2026.04/
│       └── 林家和115.04月份_DHI整理.xlsx
├── 94.吳龍廷/
│   ├── 吳龍廷_2026.1/
│   ├── 吳龍廷_2026.2/
│   └── 吳龍廷115.3月份_DHI整理.xlsx   # ← note: inconsistent placement
├── 顏御哲_2026.1/
├── 顏御哲_2026.2/
├── 顏御哲_2026.3/
├── 顏御哲115.3月份_DHI整理.xlsx        # ← orphaned at top level
├── 20260108145639QF_DHI.xlsx           # PDF-converted output (merged)
├── 20260108145639QF_性能檢定月報表.pdf
└── 20260108145639QF_牛乳品質檢驗報告.pdf (+ .xlsx)
```

## Naming Conventions

### PDF Files
Format: `YYYYMMDDHHMMSS{案件編號}_{report_type}.pdf`
- Example: `20260108145639QF_牛乳品質檢驗報告.pdf`
- First 8 digits = date (YYYYMMDD)
- Suffix codes: `_牛乳品質檢驗報告`, `_性能檢定月報表`

### DHI整理.xlsx Files
Format: `{農場名稱}{民國年}.{月}月份_DHI整理.xlsx`
- Example: `吳龍廷115.3月份_DHI整理.xlsx`
- 民國年 115 = 2026

### Farm Directories
Format: `{案件編號}.{農場名稱}/` or `{農場名稱}_{year}/{農場名稱}_{year.month}/`
- Farm directories under `94.吳龍廷/` use subdirectories by month
- 顏御哲 farm uses top-level subdirectories without a farm prefix directory

## Key File Locations

| Purpose | Path |
|---------|------|
| API entry point | `backend/main.py` |
| Data extraction | `backend/extractor.py` |
| Milk quality converter | `src/milk_pdf_to_xlsx.py` |
| Performance converter | `src/performance_pdf_to_xlsx.py` |
| Frontend UI | `frontend/index.html` |
| Farm file registry | `backend/extractor.py` → `FARM_FILES` dict |
| Dependencies | `backend/requirements.txt` |