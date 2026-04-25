# Pitfalls Research: DHI Web System

**Domain:** FastAPI + Vue 3 brownfield upgrade with PDF conversion pipeline
**Researched:** 2026-04-23
**Confidence:** HIGH — Based on codebase analysis + common patterns in this stack

---

## Data Pipeline Pitfalls

### Pitfall 1: PDF Pair Validation Happens Too Late
- **Issue:** User uploads two PDFs; system only discovers they're mismatched (different farm, different month) after running the conversion script, which takes 5–10 seconds and may produce garbled output.
- **Warning sign:** Conversion "succeeds" but imported data is nonsense — wrong farm name, wrong date in records.
- **Prevention:** Validate pair before calling conversion scripts. Extract farm code and date from filename (first 8 chars = date, suffix = case number per CLAUDE.md). Check match before any file I/O beyond filename parsing. Return 422 with specific error: "性能檢定 (94, 2026.01) 和 牛乳品質 (06, 2026.01) 案件編號不符".
- **Phase:** Phase 2 (Data Import Pipeline)

### Pitfall 2: Fixed Converters Run in the Web Process
- **Issue:** `src/milk_pdf_to_xlsx.py` uses `tkinter` GUI pickers when invoked via `main()`. If called directly from a FastAPI background task, it may attempt to open a GUI window, fail silently, or block the process.
- **Warning sign:** Upload endpoint hangs indefinitely; no error returned.
- **Prevention:** Always call converter functions directly (not `main()`), bypassing the GUI entry point. Review `performance_pdf_to_xlsx.py` to ensure there's a callable function that accepts file paths without spawning GUI. Wrap in a try/except and capture stdout/stderr.
- **Phase:** Phase 2 (Data Import Pipeline)

### Pitfall 3: Partial Import on Conversion Failure
- **Issue:** Conversion succeeds for milk quality PDF but fails for performance PDF (or vice versa). Importer writes partial data to the database. Subsequent months' comparisons are now wrong.
- **Warning sign:** Monthly report exists in DB but `avg_dim`, `open_days`, `services` are all NULL or 0.
- **Prevention:** Run conversion as a transaction: if either script fails, delete any partial output and mark the upload job as failed. Do not write to the database until both xlsx files are successfully produced and parseable.
- **Phase:** Phase 2 (Data Import Pipeline)

### Pitfall 4: LABEL_KEY Mapping Brittleness
- **Issue:** `backend/extractor.py` has a `LABEL_KEY` dict that maps Chinese column names from xlsx to Python keys. If a PDF layout change causes a column header to shift slightly (e.g., "體細胞數(萬/ml)" → "體細胞數(萬/mL)"), the mapping silently returns None for that field.
- **Warning sign:** SCC column shows as 0 or None for all cows in a specific month only.
- **Prevention:** Add explicit validation after parsing: assert that critical columns (乳量, 體細胞數, 胎次) are present and not all-null before committing to the database. Log which columns were not found. Alert admin on import.
- **Phase:** Phase 2 (Data Import Pipeline)

---

## Authentication / Authorization Pitfalls

### Pitfall 5: UI-Only Role Enforcement
- **Issue:** Farmer role is blocked from seeing other farms in the frontend, but the API endpoint `/api/farms/06/...` is not actually protected. A curious user inspecting network traffic can fetch any farm's data.
- **Warning sign:** Works fine in demo; security audit or pen test reveals unrestricted API.
- **Prevention:** Enforce role checks in FastAPI dependencies, not just in Vue Router guards. Every `/api/farms/{farm_code}/...` endpoint must check that the authenticated user either has `consultant`/`admin` role OR has `farm_id` matching the requested farm.
- **Phase:** Phase 1 (Auth)

### Pitfall 6: Admin Lockout
- **Issue:** Admin changes or forgets their password. No recovery mechanism. System is unusable without DB direct access.
- **Warning sign:** Admin says "I can't log in" and there's no fallback.
- **Prevention:** During initial setup, generate a one-time recovery code. Hash and store it in DB. Display it once with instructions to save it. Recovery code flow: POST /auth/recover with code + new password. Optionally, a CLI script `python manage.py reset-admin-password` that works with direct DB access.
- **Phase:** Phase 1 (Auth)

### Pitfall 7: JWT Secret Hardcoded in Source
- **Issue:** Developer puts `SECRET_KEY = "dev-secret"` in code. Ships to production. Tokens signed with dev secret are valid in prod.
- **Warning sign:** JWT secret is in version-controlled Python file, not environment variable.
- **Prevention:** Load from environment: `SECRET_KEY = os.environ.get("JWT_SECRET_KEY")`. Raise startup error if not set. Generate with `openssl rand -hex 32`. Never commit a real secret.
- **Phase:** Phase 1 (Auth)

---

## Report Generation Pitfalls

### Pitfall 8: ECharts Charts Don't Render in WeasyPrint
- **Issue:** PDF is generated server-side by WeasyPrint from HTML. ECharts charts are JavaScript — WeasyPrint cannot execute JavaScript. PDF has blank chart areas.
- **Warning sign:** PDF generates successfully but all chart sections are blank white rectangles.
- **Prevention:** Two approaches:
  1. **Frontend-first:** Frontend renders charts to canvas, exports PNG via `chart.getDataURL()`, sends base64 PNG to backend, backend embeds in PDF HTML template.
  2. **Server-side:** Use `pyecharts` to generate static chart images server-side (slower, requires separate library).
  Approach 1 is simpler. Design the export API to accept PNG payloads alongside filter params.
- **Phase:** Phase 5 (Report Export)

### Pitfall 9: Excel Export Looks Like Raw Data Dump
- **Issue:** Consultant expects Excel that looks like DHI整理.xlsx (formatted, color-coded, structured). System exports a flat CSV-style sheet with raw column names like `scc`, `pf_ratio`.
- **Warning sign:** First demo with a consultant: "This doesn't look like what I normally send to farmers."
- **Prevention:** Mirror DHI整理.xlsx sheet structure exactly (1-總表, 2-乳品質, 3-月比較, 4-牛群資料表). Use Traditional Chinese column headers. Apply openpyxl conditional formatting (red fill for SCC > 20, yellow for alert codes). Test export with an actual consultant before considering this feature done.
- **Phase:** Phase 5 (Report Export)

### Pitfall 10: Large Cow Table Causes Memory Spike During Export
- **Issue:** Farm with 150 cows × 12 months × many columns = large in-memory DataFrame during Excel generation. FastAPI process memory spikes; other requests slow down.
- **Warning sign:** Export works fine for 30-cow farm; crashes for 150-cow farm.
- **Prevention:** Generate Excel row-by-row using openpyxl's `write_only` mode. Stream the response using `StreamingResponse` in FastAPI. Do not load entire dataset into pandas DataFrame for export.
- **Phase:** Phase 5 (Report Export)

---

## Database Migration Pitfalls

### Pitfall 11: SQLite Works, PostgreSQL Breaks
- **Issue:** SQLite is permissive about types (stores anything in any column). PostgreSQL is strict. Code that works in SQLite fails in PostgreSQL due to type mismatches (e.g., storing `None` in a NOT NULL column, using `TEXT` for what should be `NUMERIC`).
- **Warning sign:** All tests pass in SQLite dev; first PostgreSQL deployment throws `sqlalchemy.exc.DataError`.
- **Prevention:** Use SQLAlchemy 2.x typed columns from the start. Run Alembic migrations against a local PostgreSQL container before production deploy. Add a CI step or a manual test checklist: "run migration on PostgreSQL before release."
- **Phase:** Phase 6 (Admin + Deployment)

### Pitfall 12: Skipping Alembic for "Just SQLite"
- **Issue:** Developer manually creates the SQLite database, skips Alembic setup. When PostgreSQL migration comes, there are no migration scripts. Someone has to manually write SQL to create the schema, possibly getting it wrong.
- **Warning sign:** Schema exists in `models.py` but no `alembic/` directory.
- **Prevention:** Set up Alembic in Phase 1 alongside the first models. Run `alembic init` and `alembic revision --autogenerate` from the first commit. Even for SQLite dev, treat migrations as the source of truth.
- **Phase:** Phase 1 (Database)

### Pitfall 13: Existing xlsx Data Not Migrated
- **Issue:** System launches with a new database, but 3 years of historical xlsx data for 3 farms is still sitting in `data/`. Consultant opens the system and sees no data.
- **Warning sign:** Import pipeline works for new uploads but historical data is inaccessible.
- **Prevention:** Build a one-time bulk import script as part of Phase 2: scans `data/` for all existing `*_DHI.xlsx` and `*_DHI整理.xlsx` files, imports them into the database in chronological order. Run before any first demo.
- **Phase:** Phase 2 (Data Import Pipeline)

---

## Deployment Pitfalls

### Pitfall 14: WSL Volume Mount Path Issues
- **Issue:** Docker on WSL2 uses Linux paths. `./data` works in WSL terminal but may not resolve correctly if Docker Desktop is configured to use Windows paths, causing the backend to see an empty `/app/data/` directory.
- **Warning sign:** Backend starts successfully; `GET /api/farms` returns empty list despite data existing on disk.
- **Prevention:** Use explicit absolute paths in `docker-compose.yml` or ensure WSL2 Docker context is used (not Windows Docker Desktop). Test with `docker exec -it backend ls /app/data` to verify mounts.
- **Phase:** Phase 6 (Deployment)

### Pitfall 15: `localhost` vs Container Networking
- **Issue:** Backend connects to database using `localhost`. In Docker, `localhost` is the container itself, not the host or the `db` service. PostgreSQL connection fails.
- **Warning sign:** Backend container starts, immediately crashes with `Connection refused` to database.
- **Prevention:** Use Docker service name as hostname: `DATABASE_URL=postgresql+asyncpg://user:pass@db/dhi` (where `db` is the service name). For SQLite dev without Docker, use relative path `sqlite+aiosqlite:///./dhi.db`.
- **Phase:** Phase 6 (Deployment)

### Pitfall 16: PDF/xlsx Files Not Persisted in Production
- **Issue:** Docker container is stateless. PDFs uploaded to the container are lost when it restarts. Database has upload records pointing to files that no longer exist.
- **Warning sign:** After container restart, re-import fails with "source file not found."
- **Prevention:** Mount `data/` as a named Docker volume or host-path volume. Ensure the volume is included in backup strategy. Never write uploaded files to container filesystem only.
- **Phase:** Phase 6 (Deployment)

---

## Frontend Pitfalls

### Pitfall 17: CDN Prototype State Management Ported Directly
- **Issue:** Existing `index.html` uses `window.__DHI_DATA__` (global variable) and Vue 3 reactive state per component. This doesn't scale to a multi-page Vite app with shared filter state.
- **Warning sign:** Parity filter applied to chart doesn't update the cow table; or selecting a farm on the dashboard doesn't persist when navigating to the upload page.
- **Prevention:** Migrate to Pinia store from day one of the Vite rebuild. Define a single `useFilterStore()` with: `activeFarm`, `activeMonth`, `parity`, `group`, `dateRange`. All components read from and write to this store. No component-local filter state.
- **Phase:** Phase 3 (Farm Dashboard)

### Pitfall 18: ECharts Instance Leak in Vue Components
- **Issue:** ECharts chart is initialized in `onMounted()` but not disposed in `onUnmounted()`. When navigating between farms/months, old chart instances accumulate, causing memory growth and visual glitches (old data briefly visible before new data loads).
- **Warning sign:** Chart shows old data for a frame when switching months; browser memory grows during navigation.
- **Prevention:** Always call `chart.dispose()` in `onUnmounted()`. Use `vue-echarts` component wrapper (handles this automatically). If using raw ECharts, pattern:
  ```js
  onUnmounted(() => { chartInstance?.dispose() })
  ```
- **Phase:** Phase 3 (Farm Dashboard)

### Pitfall 19: Filter Round-Trip on Every Keypress
- **Issue:** Filter changes (parity, group) trigger API calls on every change. On slow connections, rapid filter changes result in race conditions: older response arrives after newer one, displaying stale data.
- **Warning sign:** Filter flickering; chart briefly shows wrong data when clicking filters quickly.
- **Prevention:** Debounce filter-triggered API calls (300ms). Alternatively, load all cow records for the month once and filter client-side — this is feasible for herds of 30–150 cows (JSON payload ~50–100 KB). Client-side filtering also enables instant on-site response without network dependency.
- **Phase:** Phase 4 (Dynamic Filtering)
