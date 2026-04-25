# Research Summary: DHI Web System

**Synthesized:** 2026-04-23
**Sources:** STACK.md (HIGH), FEATURES.md (MEDIUM), ARCHITECTURE.md (HIGH), PITFALLS.md (HIGH)

---

## Recommended Stack

- **FastAPI + SQLAlchemy 2.x (async) + Alembic** — Keep existing FastAPI; SQLAlchemy handles SQLite↔PostgreSQL switch via `DATABASE_URL` env var; Alembic must be set up from day one even for SQLite dev, or the migration to PostgreSQL will require manual SQL reconstruction
- **Vue 3 + Vite + Pinia + Vue Router 4** — Upgrade from CDN prototype to Vite build; Pinia is mandatory (not optional) because filter state must be a single source of truth shared by charts, cow table, and export — without it, filters applied to one component will not propagate to others
- **ECharts 5.4+ via vue-echarts wrapper** — Already in use; vue-echarts handles chart disposal on unmount automatically, preventing the memory leak that raw `echarts.init()` causes when navigating between farms
- **JWT auth: access token in memory + refresh token in httpOnly cookie** — Stateless, Docker-compatible, with `Depends(get_current_user)` and `Depends(require_role(...))` as FastAPI dependencies; role enforcement must be in the backend, not just Vue Router guards
- **WeasyPrint for PDF export; openpyxl for Excel export** — WeasyPrint is Python-native (no headless Chrome); ECharts charts must be pre-rendered to PNG on the frontend via `chart.getDataURL()` and sent as base64 to the backend before PDF generation; openpyxl should use write_only mode for large datasets

---

## Table Stakes Features

Features that must exist before the first consultant demo. Missing any = tool is not credible.

- **Login + role enforcement at API level** — Every `/api/farms/{farm_code}/...` endpoint checks that the requesting user is admin/consultant OR owns that farm; UI-only gating is a security gap (Pitfall 5)
- **Admin lockout prevention** — On initial setup, generate a one-time recovery code, hash and store it in DB, display once; also provide `python manage.py reset-admin-password` CLI fallback (Pitfall 6)
- **Farm selector + month selector with auto-select to latest** — Core navigation; consultant must always see "which farm, which month" in a persistent header
- **KPI cards with month-over-month delta** — Milk yield, SCC, lactating count, with color-coded arrows; "is this better or worse than last month?" is the first question on every farm visit
- **Trend charts (12 months): milk yield, SCC, lactating count** — Already partially working in prototype; extend to 12 months with parity breakdown
- **Individual cow table: sortable, searchable, alert code badges** — A/B/C/D/E flag codes are already in the data; surface them as color-coded badges; client-side filtering preferred over API round-trips for herds of 30-150 cows
- **PDF pair upload with validation before conversion** — Validate farm code + date prefix match before calling any conversion script; return specific Chinese error messages; never call `main()` entry point of converter scripts (Pitfall 1, 2)
- **Excel export mirroring DHI整理.xlsx structure** — Sheet layout: 1-總表, 2-乳品質, 3-月比較, 4-牛群資料表; Traditional Chinese headers; conditional formatting (red for SCC > 20 萬); a flat data dump will fail at first consultant review (Pitfall 9)

---

## Key Differentiators

What makes this better than the current Excel + PDF workflow:

- **Multi-farm cross-comparison table** — Consultant sees all farms' key metrics for the same month in one table (rows = farms, columns = 乳量/SCC/lactating count/MoM deltas); impossible to do across 3 separate Excel files
- **Persistent filter bar with instant client-side response** — Parity/group filter applied simultaneously to all charts and cow table without API round-trip; on-site, when a farmer asks "show me just 經產" the answer appears in under a second, transforming presentation into dialogue
- **Alert feed: auto-surfaced problem cows** — Aggregate flagged cows (especially B = high SCC, E = high free fatty acid) at herd level before the consultant even opens the cow table; saves 15-20 minutes of manual row-scanning per farm visit
- **泌乳早期 list (DIM < 60) auto-generated** — Currently a manual sheet in Excel; filter is trivial to automate and surfaces freshening cows that need attention
- **One-click export respecting current filters** — Export reflects exactly what is on screen (farm, month, parity filter); consultant leaves a clean, formatted report with the farmer rather than a raw data dump

---

## Architecture in One Page

```
Frontend (Vue 3 + Vite)
  Pages: Dashboard | Upload | Reports | Admin
  State: Pinia store — activeFarm, activeMonth, parity, group, dateRange
  Charts: vue-echarts (dispose on unmount)
        |
        | HTTP/REST + JWT Bearer
        v
Backend (FastAPI)
  Routers: /auth  /farms  /upload  /reports  /admin
  Services: ConversionService (wraps fixed PDF scripts, never calls main())
            ImporterService (xlsx to DB, transactional)
  Auth: Depends(get_current_user) + Depends(require_role(...))
        |
        v
Database (SQLAlchemy 2.x + Alembic)
  Tables: farms | monthly_reports (cached aggregates) | cow_records | users | upload_jobs
  Dev: SQLite  |  Prod: PostgreSQL 15 (same code, different DATABASE_URL)
        |
        v
Deployment (Docker Compose)
  Dev: backend only (SQLite file volume-mounted)
  Prod: backend + frontend (nginx) + db (PostgreSQL)
```

**Recommended build order:**

- **Phase 1 — Database + Auth:** SQLAlchemy models, Alembic init, SQLite, JWT auth, user seed, recovery code mechanism. Everything else depends on this.
- **Phase 2 — Data Import Pipeline:** PDF upload endpoint, ConversionService (wrapping fixed scripts), xlsx importer, upload job status polling, bulk historical import script for existing data/.
- **Phase 3 — Farm Dashboard (Core UI):** Vue 3 + Vite project (replace CDN prototype), Pinia store, farm/month selectors, KPI cards, ECharts trend charts, parity distribution.
- **Phase 4 — Dynamic Filtering:** Filter store wired to all charts + cow table; cow table with sort, search, pagination; client-side filtering for instant on-site response.
- **Phase 5 — Report Export:** Excel export (openpyxl, mirroring DHI整理.xlsx), PDF export (WeasyPrint + chart PNG from frontend), export respects filter state.
- **Phase 6 — Admin + Deployment:** Admin panel (farm/user CRUD), password protection + anti-lockout, Docker Compose dev + prod configs, PostgreSQL migration test via Alembic.

---

## Top Pitfalls to Avoid

1. **PDF pair mismatch discovered after conversion (Pitfall 1)** — Validate farm code + date prefix from filename before calling any conversion script; return 422 with specific error message; never let mismatched PDFs reach the converter.

2. **Converter scripts called via `main()` entry point (Pitfall 2)** — The existing `milk_pdf_to_xlsx.py` uses tkinter GUI when invoked as `main()`; always call the underlying function with explicit file path arguments; wrap in try/except capturing stderr.

3. **Partial database write on conversion failure (Pitfall 3)** — Run the entire import as a transaction; if either PDF conversion fails, delete partial output and mark the upload job as failed; never write to the database until both xlsx files are produced and validated.

4. **Role enforcement only in the frontend (Pitfall 5)** — Every farm API endpoint must check user role or farm ownership in a FastAPI dependency; Vue Router guards are not security; a user can call the API directly.

5. **ECharts instance leak on component unmount (Pitfall 18)** — Use vue-echarts wrapper (handles disposal automatically) or always call `chart.dispose()` in `onUnmounted()`; raw chart instances accumulate when navigating between months/farms.

6. **Filter changes triggering API race conditions (Pitfall 19)** — Load all cow records for the month once (50-100 KB JSON for 30-150 cows) and filter client-side; avoids stale data from out-of-order API responses and enables instant on-site interaction without network dependency.

7. **Skipping Alembic for "just SQLite" dev (Pitfall 12)** — Set up Alembic in Phase 1 alongside the first models; without migration scripts from the start, the SQLite to PostgreSQL move requires manually reconstructing the schema, which will have errors.

---

## MVP Scope

### v1 — Build Now (Phases 1-6)

- JWT auth with role enforcement at API level + admin lockout prevention
- Database layer (SQLAlchemy + Alembic + SQLite dev)
- PDF upload + conversion pipeline (wrapping existing fixed scripts)
- Bulk historical import of existing data/ files (required before first demo)
- Farm dashboard: KPI cards, MoM delta, 12-month trend charts, parity distribution
- Parity/group filter bar (client-side filtering)
- Individual cow table: sortable, searchable, alert badges, DIM < 60 highlight
- Excel export mirroring DHI整理.xlsx structure with conditional formatting
- Admin panel: farm + user CRUD, password protection, recovery mechanism
- Docker Compose: dev (SQLite) + prod (PostgreSQL + nginx) configs

### v2 — Defer

- PDF export (complex; Excel covers consultant deliverable needs in v1)
- Cross-farm comparison view (single farm is the primary use case; comparison is a bonus)
- Per-cow 9-month lactation curve (requires cross-month cow ID stitching via 統一編號)
- 調區候選 auto-list (business logic requires consultant validation of criteria)
- LLM natural language query (explicitly out of scope; API is designed for compatibility)
- Herd average lactation curve benchmarking (requires external reference data)

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack choices | HIGH | Builds on existing working prototype; all libraries are established 2025 standards |
| Feature scope | MEDIUM | DHI domain knowledge from training data; validate with actual consultant before Phase 3 |
| Architecture | HIGH | Direct codebase analysis; standard FastAPI + Vue 3 patterns |
| Pitfalls | HIGH | Several (Pitfall 1, 2, 17) derived from actual code in the repo, not general patterns |

**Gaps to address during planning:**
- Confirm whether `performance_pdf_to_xlsx.py` has a callable function (not just `main()`); if not, a thin wrapper must be written in Phase 2 before the import pipeline can be built
- Confirm Excel export structure with the actual consultant before Phase 5 starts; the sheet layout assumption is based on DHI整理.xlsx analysis but consultant may have custom preferences
- Determine whether 顏御哲 farm has a numeric case code like the other two farms (94, 06); the upload validation logic depends on consistent filename suffix format
