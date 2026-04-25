# Stack Research: DHI Web System

**Domain:** FastAPI + Vue 3 agricultural data dashboard
**Researched:** 2026-04-23
**Confidence:** HIGH — Based on codebase analysis + established 2025 Python/Vue ecosystem

---

## Recommended Stack

### Backend

| Library | Version | Rationale |
|---------|---------|-----------|
| FastAPI | 0.136+ (already installed) | Already in use; async support; automatic OpenAPI docs useful for LLM integration later |
| Uvicorn | 0.44+ (already installed) | Paired with FastAPI; production-ready with `--workers` |
| SQLAlchemy | 2.x (async) | ORM that abstracts SQLite↔PostgreSQL switch; use `asyncpg` driver for PostgreSQL |
| Alembic | latest | Schema migrations; essential for SQLite→PostgreSQL migration path |
| Pydantic v2 | bundled with FastAPI | Request/response validation; already used implicitly |
| python-jose[cryptography] | 3.3+ | JWT token creation and validation; standard FastAPI auth pattern |
| passlib[bcrypt] | 1.7+ | Password hashing; bcrypt is the right choice for 2025 |
| python-multipart | latest | FastAPI file upload support (PDF uploads) |
| openpyxl | 3.1+ (already installed) | Excel export; already used for xlsx reading |
| WeasyPrint | 62+ | PDF generation from HTML/CSS; Python-native, no headless Chrome dependency |
| aiofiles | latest | Async file I/O for upload handling |

**What NOT to use:**
- `wkhtmltopdf` — requires system binary, Docker complexity, poor WSL support
- `reportlab` — low-level, requires writing PDF primitives; HTML→PDF via WeasyPrint is faster to implement
- `celery` — overkill for synchronous PDF conversion; use FastAPI BackgroundTasks instead
- `SQLModel` — attractive but adds a layer; SQLAlchemy 2.x direct is more flexible and better documented

### Frontend

| Library | Version | Rationale |
|---------|---------|-----------|
| Vue 3 | 3.4+ (already in use) | Keep existing choice; Composition API is correct for this complexity |
| Vite | 5.x | Build tooling upgrade from CDN prototype; HMR, tree-shaking, proper bundling |
| Pinia | 2.x | State management — filter state (parity, group, date range) must be single source of truth shared by charts + table + export; Pinia is the official Vue 3 store |
| Vue Router 4 | 4.x | Multi-page navigation (farm dashboard / upload / admin / reports) |
| ECharts | 5.4+ (already in use) | Keep existing choice; avoid re-writing working chart logic |
| vue-echarts | 7.x | Vue 3 wrapper for ECharts; cleaner component integration than manual `init()` |
| Tailwind CSS | 3.x (already in use) | Keep; utility-first works well for dashboard layouts |
| Axios | 1.x | HTTP client; cleaner than raw fetch for interceptor-based JWT refresh |

**What NOT to use:**
- Vuex — superseded by Pinia for Vue 3
- Chart.js — ECharts already in use and more capable for this domain; no reason to switch
- Element Plus / Vuetify — heavy UI kit; Tailwind + minimal custom components is sufficient
- Nuxt.js — SSR not needed; SPA is correct here

### Database & ORM

**Development:** SQLite (file-based, zero setup, works in WSL)
**Production:** PostgreSQL 15+

**Migration path:** SQLAlchemy 2.x with async support covers both. Use `aiosqlite` for SQLite dev, `asyncpg` for PostgreSQL prod. Switch via `DATABASE_URL` environment variable — no code changes needed.

**Alembic** for schema migrations: set up from day one, even for SQLite. This ensures migration scripts work when switching to PostgreSQL.

```
DATABASE_URL=sqlite+aiosqlite:///./dhi.db          # dev
DATABASE_URL=postgresql+asyncpg://user:pass@db/dhi  # prod
```

### Authentication

**Pattern:** JWT (access token + refresh token)

- Access token: short-lived (15–60 min), stored in memory (not localStorage)
- Refresh token: longer-lived (7 days), stored in httpOnly cookie
- FastAPI dependency injection for route protection: `Depends(get_current_user)`
- Role check as a separate dependency: `Depends(require_role("admin"))`

**Why not sessions?** Docker horizontal scaling and future LLM API access both benefit from stateless JWT.

**Admin anti-lockout mechanism:** Store a recovery code (hashed) in the database during initial setup. If admin password is forgotten, recovery code resets it. Recovery code itself is shown once and must be saved by the operator.

### Report Generation

**Excel:** `openpyxl` (already installed) — Write structured worksheets mirroring DHI整理.xlsx sheet layout. Use `openpyxl.styles` for conditional formatting (red for high SCC, yellow for flagged cows).

**PDF:** `WeasyPrint` — Generate HTML report template server-side, pass to WeasyPrint for PDF. ECharts charts must be pre-rendered to PNG (use `pyecharts` or capture via `snapshot-canvas` on frontend and send base64 to backend before PDF generation).

**Alternative PDF approach:** Frontend renders charts → canvas → sends PNG to backend → backend embeds in WeasyPrint HTML. This avoids server-side headless rendering entirely.

### Deployment

**Docker Compose structure:**

```yaml
services:
  backend:
    build: ./backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
    volumes:
      - ./data:/app/data        # PDF and xlsx files
      - ./backend:/app          # code (dev only)
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"                 # nginx serving dist/

  db:                           # only for PostgreSQL prod
    image: postgres:15
    environment:
      POSTGRES_DB: dhi
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Dev (SQLite): only `backend` service needed.
Prod (PostgreSQL): all three services.

### LLM Compatibility

Design the API so future natural language queries can be added without breaking existing clients:

1. **Structured query endpoints:** `/api/farms/{farm}/query` accepting filter objects (not SQL) — LLM can construct these filter objects from natural language
2. **Consistent field naming:** All API responses use the same English key names (defined in `extractor.py`'s `LABEL_KEY`) — LLM training data needs consistency
3. **OpenAPI spec auto-generated:** FastAPI does this by default; LLM tool-calling can use the spec directly
4. **Separate analytics endpoints:** `/api/farms/{farm}/summary`, `/api/farms/{farm}/cows`, `/api/farms/{farm}/trends` — clear semantic boundaries for LLM to reason about

---

## Confidence Levels

| Decision | Confidence | Notes |
|----------|-----------|-------|
| FastAPI + SQLAlchemy 2.x | HIGH | Established pattern, well-documented |
| Vue 3 + Vite + Pinia | HIGH | Official Vue 3 recommended stack |
| ECharts (keep) | HIGH | Already working in prototype |
| WeasyPrint for PDF | MEDIUM | Works well but chart pre-rendering adds complexity |
| JWT with httpOnly refresh | HIGH | Standard security practice |
| Alembic for migrations | HIGH | Required for SQLite→PostgreSQL path |
| openpyxl for Excel | HIGH | Already installed, well-suited |
