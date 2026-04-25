# Architecture Research: DHI Web System

**Domain:** FastAPI + Vue 3 agricultural data dashboard (brownfield upgrade)
**Researched:** 2026-04-23
**Confidence:** HIGH — Based on direct codebase analysis + established patterns

---

## Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Vue 3 + Vite)                 │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐   │
│  │ Dashboard│  │ Upload   │  │ Admin     │  │ Reports  │   │
│  │ (charts) │  │ (PDF)    │  │ (users)   │  │ (export) │   │
│  └──────────┘  └──────────┘  └───────────┘  └──────────┘   │
│                    Pinia store (filter state)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST (JWT Bearer)
┌──────────────────────────▼──────────────────────────────────┐
│                     BACKEND (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routers                                             │   │
│  │  /auth  /farms  /upload  /reports  /admin            │   │
│  └──────────────┬─────────────────┬────────────────────┘   │
│                 │                 │                          │
│  ┌──────────────▼──┐  ┌───────────▼────────────────────┐   │
│  │  Services       │  │  Conversion Service             │   │
│  │  (business      │  │  (calls fixed PDF scripts)      │   │
│  │   logic)        │  │  src/milk_pdf_to_xlsx.py        │   │
│  └──────────────┬──┘  │  src/performance_pdf_to_xlsx.py │   │
│                 │     └───────────────────────────────── ┘   │
│  ┌──────────────▼──────────────────────────────────────┐   │
│  │  SQLAlchemy Models + Alembic migrations             │   │
│  └──────────────┬────────────────────────────────────── ┘   │
└─────────────────┼───────────────────────────────────────────┘
                  │
      ┌───────────▼───────────┐
      │  Database             │
      │  SQLite (dev)         │
      │  PostgreSQL (prod)    │
      └───────────────────────┘
```

## Data Flow

### PDF → Dashboard Pipeline

```
1. Consultant uploads PDF pair via browser
   └─→ POST /api/upload  (multipart, 2 files)

2. Backend validates pair
   ├─→ Check: same farm prefix + same date prefix
   ├─→ Check: one 性能檢定 + one 牛乳品質
   └─→ Return 422 with specific error if invalid

3. Save PDFs to disk (data/{farm}/{date}/)
   └─→ Trigger conversion (FastAPI BackgroundTasks)

4. Conversion Service calls fixed scripts
   ├─→ src/milk_pdf_to_xlsx.py → *_牛乳品質.xlsx
   ├─→ src/performance_pdf_to_xlsx.py → *_DHI.xlsx
   └─→ Merge result: combined DataFrame

5. Importer reads combined xlsx
   └─→ Normalizes column names (reuse LABEL_KEY from extractor.py)
   └─→ Writes to database:
       ├─→ farms table (upsert farm record)
       ├─→ monthly_reports table (insert month snapshot)
       └─→ cow_records table (insert per-cow rows)

6. Frontend polls /api/upload/{job_id}/status
   └─→ On completion: redirect to farm/month dashboard
```

### API → Frontend Data Flow

```
Frontend (Pinia store)
  └─→ GET /api/farms                           # farm list
  └─→ GET /api/farms/{farm}/months             # available months
  └─→ GET /api/farms/{farm}/{month}/summary    # KPI cards data
  └─→ GET /api/farms/{farm}/{month}/trends     # 12-month trend data
  └─→ GET /api/farms/{farm}/{month}/cows       # cow table (filterable)
  └─→ GET /api/farms/comparison?month={m}      # cross-farm summary
  └─→ POST /api/reports/excel                  # trigger Excel export
  └─→ POST /api/reports/pdf                    # trigger PDF export
```

## Database Schema Approach

DHI data is **monthly snapshots** — not a continuous time series. Schema reflects this.

```sql
-- Farms registry
farms (
  id           INTEGER PK,
  code         TEXT UNIQUE,   -- "94", "06", "顏御哲"
  name         TEXT,
  created_at   TIMESTAMP
)

-- Each uploaded month's summary-level data
monthly_reports (
  id           INTEGER PK,
  farm_id      FK → farms.id,
  report_date  DATE,          -- 測乳日期 (measurement date)
  import_date  TIMESTAMP,     -- when it was uploaded
  source_file  TEXT,          -- path to source xlsx

  -- Herd-level aggregates (cached for fast KPI display)
  total_cows        INTEGER,
  lactating_count   INTEGER,
  avg_milk_kg       FLOAT,
  avg_scc           FLOAT,
  avg_dim           FLOAT,
  avg_open_days     FLOAT,
  avg_services      FLOAT,

  UNIQUE (farm_id, report_date)
)

-- Per-cow records for each month
cow_records (
  id              INTEGER PK,
  monthly_report_id  FK → monthly_reports.id,
  farm_id         FK → farms.id,
  farm_cow_id     TEXT,        -- 場內編號 (local farm ID)
  national_id     TEXT,        -- 統一編號

  -- Core metrics
  milk_kg         FLOAT,
  fat_pct         FLOAT,
  protein_pct     FLOAT,
  scc             FLOAT,       -- 體細胞數 (萬/mL)
  urea_nitrogen   FLOAT,
  citric_acid     FLOAT,
  pf_ratio        FLOAT,
  free_fatty_acid FLOAT,
  bhba            FLOAT,       -- β-羥基丁酸

  -- Reproductive
  parity          INTEGER,     -- 胎次
  calving_date    DATE,
  dim             INTEGER,     -- 泌乳天數
  open_days       INTEGER,     -- 空胎天數
  services        INTEGER,     -- 配種次數

  -- Alert flags
  alert_codes     TEXT,        -- "(A)(B)" etc, stored as string

  INDEX (farm_id, monthly_report_id),
  INDEX (national_id)
)

-- Users and roles
users (
  id           INTEGER PK,
  username     TEXT UNIQUE,
  password_hash TEXT,
  role         TEXT,           -- "admin" | "consultant" | "farmer"
  farm_id      FK → farms.id NULL,  -- NULL = all farms (admin/consultant)
  recovery_hash TEXT,          -- admin lockout prevention
  created_at   TIMESTAMP
)

-- Upload job tracking
upload_jobs (
  id           TEXT PK,        -- UUID
  user_id      FK → users.id,
  status       TEXT,           -- "pending" | "converting" | "done" | "failed"
  error_msg    TEXT NULL,
  farm_id      FK → farms.id NULL,
  report_date  DATE NULL,
  created_at   TIMESTAMP,
  completed_at TIMESTAMP NULL
)
```

**Key design decisions:**
- `monthly_reports` caches herd-level aggregates for fast KPI card rendering (avoids re-aggregating cow_records on every request)
- `cow_records` stores raw per-cow data for filtering and individual lookup
- `national_id` (統一編號) enables cross-month cow tracking without complex linking tables
- `alert_codes` stored as string — simple and matches source data format

## API Design for LLM Compatibility

The API must be structured so a future LLM can call it via tool-calling without breaking changes.

**Principles:**
1. **Filter as structured params, not query strings** — Use consistent JSON body for filter state:
   ```json
   { "parity": "all|primiparous|multiparous", "group": "string|null", "months": 6 }
   ```
   LLM can construct this from "show me first-calvers for the past 6 months"

2. **Semantic endpoint names** — `/summary`, `/trends`, `/cows` are meaningful to an LLM reasoning about data

3. **Consistent field names** — All responses use the same field names from a central schema (Pydantic models). No endpoint returns `乳量` in one place and `milk_kg` in another.

4. **OpenAPI spec** — FastAPI generates this automatically. LLM tool-calling can use `/openapi.json` directly.

5. **Future `/api/query` endpoint** — Reserve this path for LLM-generated structured queries. Implement as a no-op that returns 501 for now; add implementation when LLM feature is built.

## Docker / Deployment Architecture

**WSL development:**
```
docker-compose.dev.yml
  backend: uvicorn with --reload, volume-mounted code
  (no db container — uses SQLite file at ./data/dhi.db)
```

**Production (new host):**
```
docker-compose.yml
  backend: uvicorn with multiple workers
  frontend: nginx serving dist/ + proxy /api → backend
  db: PostgreSQL 15 container with named volume
```

**Environment switch:** `DATABASE_URL` env var controls SQLite vs PostgreSQL — no code changes required (SQLAlchemy handles dialect).

**Volume strategy:**
- `./data/` mounted into backend — PDF files and xlsx files persist here
- Named Docker volume for PostgreSQL data
- Never bake data into the image

**WSL → Linux migration checklist:**
- File paths: use forward slashes only (already correct in Python)
- Line endings: ensure `.gitattributes` normalizes to LF
- Port binding: `0.0.0.0` not `localhost` in Docker
- `host.docker.internal` not available on Linux — use service names

## Recommended Build Order

Dependencies determine phase order:

```
Phase 1: Database + Auth
  └─→ SQLAlchemy models + Alembic + SQLite
  └─→ JWT auth (login, role middleware)
  └─→ User seed data (admin account)
  REASON: Everything else depends on the database existing and routes being protected

Phase 2: Data Import Pipeline
  └─→ PDF upload endpoint
  └─→ Conversion service (wraps existing scripts)
  └─→ Importer (xlsx → database)
  └─→ Upload job status polling
  REASON: Without data in the database, the dashboard has nothing to show

Phase 3: Farm Dashboard (Core UI)
  └─→ Vue 3 + Vite project setup (replacing CDN prototype)
  └─→ Farm selector, month selector
  └─→ KPI cards + MoM deltas
  └─→ ECharts trend charts (milk, SCC, lactating count)
  └─→ Parity distribution chart
  REASON: This is the primary use case; must exist before filters or export

Phase 4: Dynamic Filtering
  └─→ Pinia filter store (parity, group, date range)
  └─→ API filter params on /cows and /summary endpoints
  └─→ Cow table (sortable, searchable, paginated)
  REASON: Transforms static display into on-site interactive tool

Phase 5: Report Export
  └─→ Excel export (openpyxl, mirrors DHI整理.xlsx structure)
  └─→ PDF export (WeasyPrint + chart PNG pre-rendering)
  └─→ Export respects current filter state
  REASON: Secondary use case; requires dashboard + filters to be complete

Phase 6: Admin + Deployment
  └─→ Admin panel (farm management, user management)
  └─→ Password protection + anti-lockout mechanism
  └─→ Docker Compose (dev + prod configs)
  └─→ PostgreSQL migration + Alembic migration test
  REASON: Deploy-readiness comes last; app must work before hardening
```
