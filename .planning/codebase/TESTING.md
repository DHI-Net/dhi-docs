# Testing

## Current State
**No formal test suite.** Zero test files, no test framework configured, no CI pipeline.

## Manual Verification
`backend/extractor.py` has an `if __name__ == "__main__":` block that prints per-farm/month summaries:
```python
# Run manually: cd backend && python extractor.py
for farm, fd in data.items():
    for month, md in fd["months"].items():
        print(f"{farm} {month}: 測乳日={md['measurement_date']}  頭數=...  平均乳量=...")
```

`src/milk_pdf_to_xlsx.py` uses tkinter GUI for file selection; reports `[OK]` / `[EMPTY]` per PDF.

## Infrastructure Gaps
- No pytest / unittest setup
- No test fixtures or sample data mocks
- No API integration tests
- No data validation / schema checks
- No CI/CD (no `.github/`, `Makefile`, `tox.ini`, etc.)

## Pure Functions Suitable for Unit Tests (When Added)
| Function | Module | What to test |
|----------|--------|-------------|
| `to_float()` | `backend/extractor.py` | None, NaN, `"─"`, numeric strings, Chinese dashes |
| `to_str()` | `backend/extractor.py` | None, NaN, sentinel values, normal strings |
| `parse_date()` | `backend/extractor.py` | datetime, Timestamp, Excel serial int, ISO string |
| `roc_to_iso()` | `src/performance_pdf_to_xlsx.py` | `"25/5/17"` → `"2025-05-17"` |
| `normalize_farm_id()` | `src/milk_pdf_to_xlsx.py` | `"11M2459"`, `"2N1"`, `"312-2"` |
| `safe_float()` | `src/performance_pdf_to_xlsx.py` | invalid strings, None |

## Integration Test Opportunities
- `extract_cows()` against real `.xlsx` files in `data/` — verify row counts match expected
- `extract_summary()` — verify month comparison values are in expected numeric ranges
- API endpoints — verify `/api/farms` returns correct farm list, `/api/farms/{farm}/{month}` returns non-empty cows list

## Recommended Approach
**pytest** — consistent with existing Python stack. Real Excel files in `data/` can serve as integration fixtures (no mock needed for initial coverage).