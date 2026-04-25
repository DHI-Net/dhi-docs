# Code Conventions

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