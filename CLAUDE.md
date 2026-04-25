# DHI_Net 專案

## 角色定位
前後端網頁設計工程師。唯一任務是根據使用者分析好的資料架構，開發完整互動式網頁系統。

## 專案概述
DHI (Dairy Herd Improvement) 月報表網頁系統。資料來源為酪農每月測乳紀錄（DHI），原始資料為兩份 PDF（性能檢定、牛乳品質），需轉檔為 xlsx 後彙整至資料庫，提供互動式儀表板呈現。

## 已知農場資料
目前資料集包含三個農場：
- 吳龍廷（案件編號 94）
- 林家和（案件編號 06）
- 顏御哲

## 技術棧（待使用者確認後定案）
- **後端**: Python FastAPI（與轉檔腳本同語言）
- **資料庫**: SQLite（開發）→ PostgreSQL（正式，便於搬遷）
- **前端**: Vue 3 + Vite（或 React，待定）
- **圖表**: Chart.js 或 ECharts
- **部署**: WSL → 搬遷到新主機時使用 Docker

## 絕對限制（不可更動）
1. **轉檔程式固定調用**：
   - 牛乳品質：`src/milk_pdf_to_xlsx.py`（已存在，不得修改轉檔邏輯）
   - 性能檢定：待設計新程式（參考 `原始資料彙整(全)` 的使用方式）
2. **不允許調用 LLM** 做轉檔或額外分析
3. **重要管理功能須設密碼保護**，且需防呆機制（避免忘記管理者密碼）

## PDF 檔案命名規則
- 前 8 碼 = 日期（YYYYMMDD 或民國年格式）
- 後面 = 案件編號
- 需成對：性能檢定 + 牛乳品質，才能合法轉檔
- 配對失敗：僅取消該月份轉檔，其他月份正常處理

## 資料結構（已分析）

### 月DHI.xlsx（轉檔後中間產物）
- `合併1`：乳品質 + 性能檢定合併（場內編號、統一編號、乳量、乳脂肪、乳蛋白、乳糖、乳固形物、乳無脂固形物、體細胞數、尿素氮、檸檬酸、P/F、酪蛋白、游離脂肪酸、飽和脂肪酸、不飽和脂肪酸、丙酮、β-羥基丁酸、注意事項、胎次、分娩日期、泌乳天數、空胎天數、配種次數）
- `性能檢定`：場內編號、胎次、分娩日期、泌乳天數、空胎天數、配種次數
- `明細`：乳品質完整欄位

### DHI整理.xlsx（最終整理檔，定義資料庫架構的參考）
Sheets:
- `1-總表`：牧場摘要（測乳日期、按分群/胎次統計）
- `2-乳品質`：乳品質分布圖
- `3-月比較`：本月 vs 上月對比（平均、頭產、經產）
- `4-牛群資料表`：每頭牛詳細資料（排序後）
- `性能檢定轉換`：前 9 個月歷史乳量 + 體細胞數趨勢
- `原始資料彙整(全)`：當月完整原始資料
- `上月資料`：上月原始資料（用於月比較）
- `2-牛群資料`：依分群（頭產/經產）的牛隻清單
- `總表-檢查`：統計驗算表
- `BCS`：體況評分
- `泌乳早期`：DIM<60 早期泌乳牛列表
- `調區`：需調整分群的牛隻

### 核心欄位與重要性
| 欄位 | 說明 | 正常範圍 | 重要度 |
|------|------|---------|--------|
| 乳量 (kg) | **最重要參數** | 依牛而定 | ★★★ |
| 體細胞數 (萬/mL) | 乳房健康指標 | <20 正常 | ★★★ |
| 尿素氮 (mg/dL) | 能量/蛋白平衡 | 11~17 | ★★ |
| 檸檬酸 (mg/dL) | | 119~190 | ★★ |
| P/F | 蛋白/脂肪比 | 0.85~0.88 | ★★ |
| 游離脂肪酸 (mmol) | 能量負平衡 | <1.5 | ★★ |
| 空胎日數 | 繁殖效率 | <120 佳 | ★★ |
| 泌乳天數 | 泌乳週期位置 | | ★ |

### 注意事項代碼
- (A) = 高乳脂
- (B) = 高體細胞數（乳房炎風險）
- (C) = 低乳量
- (D) = 低泌乳天數（剛分娩）
- (E) = 高游離脂肪酸（能量負平衡）

## 使用者角色
- **酪農戶**：只能閱覽自己牧場資料
- **顧問**：可預覽複數牧場資料
- **管理者**：可閱覽、修改任何資料；重要功能有唯一密碼保護 + 防呆機制

## 開發階段
目前尚未開始。需使用者確認架構後才開始實作。
Server 先架設在 WSL，需設計便於搬遷到新主機（用 Docker Compose）。

## 目錄結構（規劃）
```
DHI_Net/
├── CLAUDE.md
├── src/
│   └── milk_pdf_to_xlsx.py        # 牛乳品質轉檔（固定，不修改）
├── data/                          # 現有歷史資料
├── backend/
│   ├── main.py                    # FastAPI 入口
│   ├── routers/
│   ├── models/                    # SQLAlchemy models
│   ├── services/
│   │   ├── converter/             # 轉檔服務（調用固定腳本）
│   │   └── importer/              # 資料庫匯入
│   └── database.py
├── frontend/
│   └── src/
└── docker-compose.yml
```

<!-- GSD:project-start source:PROJECT.md -->
## Project

**DHI_Net**

DHI_Net 是一個供酪農業顧問使用的 DHI 月報表網頁系統。顧問（飼養管理顧問、獸醫、乳品廠指導員、飼料廠業務）可同時管理多個牧場的每月 DHI 資料，用於現場與酪農討論牛群現況，並產製客製化報告。酪農戶為次要使用者，僅能查閱自身牧場資料。

**Core Value:** 顧問能在現場即時篩選、比較多個牧場的牛群指標，並一鍵匯出報告，取代手動整理 Excel 的流程。

### Constraints

- **Tech — 轉檔程式**：`src/milk_pdf_to_xlsx.py` 固定，不得修改；性能檢定轉檔參考 `原始資料彙整(全)` 使用方式
- **Tech — 禁止 LLM**：轉檔或資料分析不得使用 LLM
- **Tech — 後端語言**：Python FastAPI（與轉檔腳本同語言，方便整合）
- **Tech — 資料庫**：SQLite（開發）→ PostgreSQL（正式），需無痛搬遷
- **Tech — 前端**：Vue 3 + Vite + ECharts（升級自現有雛型）
- **Security — 管理功能**：重要操作需唯一密碼保護 + 防呆機制（避免忘記密碼導致鎖死）
- **Deployment**：WSL 開發，Docker Compose 供正式搬遷使用
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.13 - Backend API server, PDF conversion scripts, data extraction
- JavaScript (ES2022, no transpile) - Frontend Vue 3 application (CDN-loaded, no build step currently)
- HTML/CSS - Single-page frontend (`frontend/index.html`)
## Runtime
- CPython 3.13.9 on WSL2 (Linux 5.15, Microsoft)
- pip (no lockfile present; `backend/requirements.txt` pins minimum versions with `>=`)
- Lockfile: missing (pip freeze not captured)
## Frameworks
- FastAPI 0.136.0 - REST API server (`backend/main.py`)
- Uvicorn 0.44.0 (standard extras) - ASGI server; run with `uvicorn main:app`
- Vue 3.4.21 - Reactive UI framework, loaded via `cdn.jsdelivr.net`
- ECharts 5.4.3 - Chart library for data visualizations, loaded via `cdn.jsdelivr.net`
- Tailwind CSS (latest) - Utility-first CSS, loaded via `cdn.tailwindcss.com`
- Vue 3 + Vite - Proper build pipeline (see `draw_arch.py` architecture diagram)
- Vue Router + Pinia/Vuex - Routing and state management
- pdfplumber 0.11.9 - Extracts tabular text from milk-quality PDFs (`src/milk_pdf_to_xlsx.py`)
- tkinter (stdlib) - GUI file picker for standalone PDF converter script
- pandas 2.3.4 - DataFrame operations in extractor and converter
- numpy 1.26.x - Numerical helpers (NaN checks)
- openpyxl 3.1.5 - Read/write `.xlsx` files
- Not detected (no test files, no pytest/unittest config)
- matplotlib - Architecture diagram generator only (`draw_arch.py`); not a runtime dependency
## Key Dependencies
- `fastapi>=0.111.0` - API layer; all endpoints defined in `backend/main.py`
- `uvicorn[standard]>=0.29.0` - Required to serve FastAPI
- `pdfplumber>=0.11.9` - Core of the milk-quality PDF-to-xlsx pipeline (`src/milk_pdf_to_xlsx.py`); this file must not be modified
- `pandas>=2.2.0` - All data extraction logic in `backend/extractor.py`
- `openpyxl>=3.1.0` - Reading `DHI整理.xlsx` and `月DHI.xlsx` files
- `python-multipart>=0.0.9` - Needed for FastAPI form/file uploads (future upload pipeline)
- `numpy>=1.26.0` - Used for NaN detection in `backend/extractor.py`
## Configuration
- No `.env` file detected; no environment-variable-based configuration in current code
- All file paths are hardcoded in `backend/extractor.py` (`FARM_FILES` and `CONVERTED_FILES` dicts)
- CORS is fully open (`allow_origins=["*"]`) — development only setting
- No build config files (no `pyproject.toml`, `setup.cfg`, `Dockerfile`, or `docker-compose.yml` yet)
- Frontend has no bundler config (plain HTML file served as static asset via FastAPI `StaticFiles`)
## Platform Requirements
- WSL2 (Linux) with Python 3.13
- NotoSansCJK font at `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` (required by `draw_arch.py` only)
- No Node.js required currently (all frontend via CDN)
- Docker Compose: backend (FastAPI/uvicorn) + frontend (nginx) + PostgreSQL containers
- Target: new Linux host; WSL2 is development-only
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Language
- **Python 3.13** — all backend and conversion scripts
- Traditional Chinese used for domain-specific identifiers (sheet names, column labels, farm names)
- English used for internal code keys and API fields (e.g., `"scc"`, `"milk"`, `"farm_id"`)
## Code Style (Python)
### Imports & Type Hints
- `from __future__ import annotations` at top of every module
- `Optional[T]` from `typing` for nullable return values
- Type hints on public functions: `def to_float(v) -> Optional[float]:`
### Constants & Regex
- Module-level constants in `UPPER_SNAKE_CASE`: `HEADER_COLS`, `ROW_START`, `HASH_REPLACEMENT`
- Compiled regex stored as module-level constants for reuse (not compiled inline)
- `MISSING` set defines sentinel values: `{"─", "-", ".", "", "nan"}`
### Path Handling
- `pathlib.Path` used throughout — never `os.path` string concatenation
- `BASE_DIR = Path(__file__).parent.parent` pattern for repo-relative paths
### Function Design
- Small, focused conversion helpers: `to_float()`, `to_str()`, `parse_date()`, `roc_to_iso()`
- Guard clauses: check None/NaN first, return early
- `try/except` for type coercion only — not used for flow control
- `if __name__ == "__main__":` blocks for manual integration testing
### Naming
- `snake_case` for all Python identifiers
- Domain mappings via dicts: `LABEL_KEY` (Chinese label → English key), `_COL_MAP` (DataFrame column rename)
- Month keys: `"YYYY.M"` format (e.g., `"2026.1"`, `"2026.12"`)
- Dates normalized to ISO 8601: `"YYYY-MM-DD"` strings
## Error Handling
- Conversion failures return `None` silently (data pipeline pattern) — no exceptions raised
- Missing files: `print(f"[WARN] 找不到檔案: {path}")` + skip entry
- Conversion status: `[OK]` / `[EMPTY]` prefixed print statements
- `warnings.filterwarnings("ignore")` in extractor to suppress openpyxl pandas warnings
## Data Pipeline Patterns
- Excel sheets parsed with `pd.read_excel(..., header=None)` then positional column access (`df.iloc[i, j]`)
- Alert codes extracted via regex: `re.findall(r"\([A-Z]\)", notes_raw)` → `["(A)", "(B)"]`
- `nan` string artifacts cleaned: `if notes_raw == "nan": notes_raw = ""`
- Numeric coercion: `try: return float(s2); except: return x`
## Frontend (Current Demo)
- Vanilla HTML + JavaScript — no framework, no build step
- Static files served by FastAPI's `StaticFiles` at `/static`
- CORS middleware set to `allow_origins=["*"]` (demo-only)
## API Design (Current)
- REST endpoints under `/api/` prefix
- Responses are raw Python dicts serialized to JSON by FastAPI
- `HTTPException(404, ...)` for missing farm/month
- Single global cache `_DATA` loaded at first request, held in memory for the process lifetime
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- Two-stage data pipeline: PDF → xlsx (conversion scripts) → JSON (extractor)
- Backend loads all farm/month data into memory at startup via a single in-memory cache dict
- Frontend is a single-page application served as a static file, currently embedded with pre-computed data in `window.__DHI_DATA__`
- No database layer yet — all data read directly from xlsx files on disk
- Two parallel data paths: pre-arranged `DHI整理.xlsx` files vs. raw PDF-converted `_DHI.xlsx` files
## Layers
- Purpose: Convert raw PDF reports to structured xlsx files
- Location: `src/`
- Contains: `milk_pdf_to_xlsx.py` (milk quality converter), `performance_pdf_to_xlsx.py` (performance converter + PDF-pair merger)
- Depends on: `pdfplumber`, `pandas`, `openpyxl`, optionally `tkinter` for GUI file picker
- Used by: Human operator (GUI) or future automated import service
- Purpose: Read xlsx files from disk and normalize to Python dicts / JSON-serializable structures
- Location: `backend/extractor.py`
- Contains: Farm file registry (`FARM_FILES`, `CONVERTED_FILES`), sheet parsers (`extract_summary`, `extract_cows`, `extract_converted_cows`), label normalization map (`LABEL_KEY`), helper converters (`to_float`, `to_str`, `parse_date`)
- Depends on: `pandas`, `openpyxl`, `numpy`
- Used by: `backend/main.py` at startup via `load_all_data()`
- Purpose: Expose farm/month data as REST endpoints; serve frontend static files
- Location: `backend/main.py`
- Contains: FastAPI app, CORS middleware, 4 GET endpoints, startup cache loader, static file mount
- Depends on: `extractor.py`, `fastapi`, `uvicorn`
- Used by: Frontend (via fetch) or direct API consumers
- Purpose: Interactive dashboard for viewing DHI data per farm and month
- Location: `frontend/`
- Contains: `index.html` (single-file Vue 3 + ECharts + Tailwind app), `data.js` (large embedded static dataset)
- Depends on: Vue 3 (CDN), ECharts (CDN), Tailwind CSS (CDN)
- Used by: End users (farmers, consultants, admin)
## Data Flow
- Backend: module-level `_DATA: dict | None` — populated once on first request, never invalidated
- Frontend: Vue 3 reactive data, populated from `window.__DHI_DATA__` (embedded) or API fetch
## Key Abstractions
- Purpose: Maps farm name → list of (month_key, Path) tuples pointing to xlsx files on disk
- Examples: `backend/extractor.py` (`FARM_FILES`, `CONVERTED_FILES` dicts)
- Pattern: Hard-coded dict; adding a new farm or month requires editing the source file
- Purpose: Translates inconsistent Chinese column headers from xlsx sheets to fixed English keys
- Examples: `backend/extractor.py` lines 43-65
- Pattern: `dict[str, str]` lookup applied during sheet parsing
- Purpose: Canonical per-cow data structure output by both `extract_cows()` and `extract_converted_cows()`
- Fields: `farm_id`, `national_id`, `milk`, `fat`, `protein`, `lactose`, `snf`, `ts`, `scc`, `urea`, `citric`, `pf`, `casein`, `ffa`, `sat_fa`, `unsat_fa`, `acetone`, `bhb`, `notes`, `alerts`, `parity`, `calving_date`, `dim`, `open_days`, `services`, `group`
- Pattern: Plain Python dict; same structure regardless of whether data came from curated or converted xlsx
- Purpose: Groups all data for one farm-month into a single JSON object
- Structure: `{ measurement_date, summary: { current, comparison }, cows: [...] }`
- Pattern: Returned by all `/api/farms/{farm}/{month}` endpoints
## Entry Points
- Location: `src/milk_pdf_to_xlsx.py` — `main()` / `convert_pdfs()`
- Triggers: GUI file picker (Windows tkinter) or direct `convert_pdfs([Path(...)])` call
- Responsibilities: Parse PDF text, extract tabular rows, write `明細` sheet xlsx, replace `#` chars, force numeric cell format
- Location: `src/performance_pdf_to_xlsx.py` — `main()` / `convert_pair()`
- Triggers: GUI file picker (paired PDFs) or direct `convert_pair(milk_pdf, perf_pdf)` call
- Responsibilities: Parse both PDFs, merge on farm_id, classify heifer/multi-parity, output 3-sheet xlsx
- Location: `backend/main.py`
- Triggers: `uvicorn backend.main:app` from project root
- Responsibilities: Load all xlsx data into memory, expose REST API, serve `frontend/index.html` and static files
- Location: `frontend/index.html`
- Triggers: Browser navigation to `/` or direct file open
- Responsibilities: Render farm selector, month selector, summary cards, ECharts trend charts, per-cow data table
## Error Handling
- `extractor.py` `_read_sheet()`: wraps `pd.read_excel` in `try/except`, returns `None` on failure
- `load_all_data()`: checks `path.exists()` before parsing, prints `[WARN]` and continues if missing
- `to_float()` / `to_str()` / `parse_date()`: return `None` for any unparseable value rather than raising
- `parse_milk_report_pdf()` / `parse_performance_pdf()`: skip non-matching lines silently
## Cross-Cutting Concerns
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
