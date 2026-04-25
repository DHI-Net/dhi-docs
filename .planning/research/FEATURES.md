# Features Research: DHI Web System

**Domain:** Agricultural data dashboard for dairy herd management consultants
**Researched:** 2026-04-22
**Confidence:** MEDIUM — Domain established; findings from training knowledge of DHI systems (DRMS, DairyComp, CDCB tools), agricultural SaaS patterns, and existing codebase analysis. No live web search available.

---

## Table Stakes

Features consultants expect to exist. Missing any = tool is not credible.

### Authentication & Access Control

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Login (username + password) | Any multi-user tool has login | Low | JWT-based; FastAPI-python-jose |
| Role enforcement at API level | Farmers must not see other farms; not just UI gating | Medium | Middleware on every `/api/farms/{farm}/*` route |
| Session persistence (remember login) | Consultant visits same farm repeatedly; re-auth kills flow | Low | JWT refresh token or long-lived token |
| Admin panel — user CRUD | Need to add/remove farms and accounts | Medium | Password-protected, not role-gated alone |
| Password reset mechanism | Consultant forgets password; cannot lock self out | Medium | Secret question or backup email; prevent admin lockout |

### Farm & Data Navigation

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Farm list / switcher | Consultant manages 3+ farms; needs fast switching | Low | Sidebar or top-level selector |
| Month selector | DHI is monthly; browsing history is core workflow | Low | Dropdown or timeline strip |
| Current month auto-selected | Consultant opens tool on visit day; wants latest | Low | Default to most recent available month |
| Breadcrumb / current context display | "Which farm, which month am I viewing?" always visible | Low | Static header row |

### Core Metrics Display (Summary View)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Herd summary KPI cards | Milk yield, SCC, lactating count — top-line at a glance | Low | 4–6 stat cards at page top |
| Month-over-month delta indicators | "Is this better or worse than last month?" is the first question asked on every farm visit | Low | Arrow + %, color-coded |
| Parity breakdown (頭產/經產) | Standard DHI segmentation; farmers always think in these groups | Medium | Sub-totals within summary cards |

### Charts (Herd Level)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Milk yield trend line (12 months) | Core productivity view; ECharts line chart | Low | Already partially in prototype |
| SCC trend line (12 months) | Udder health is the second most-watched metric | Low | Same chart type; log scale optional |
| Lactating cow count trend | Context for yield changes | Low | Bar or line overlay |
| Parity distribution bar chart | Standard DHI summary graphic | Low | Stacked bar: 頭產 / 2胎 / 3胎以上 |
| Monthly comparison table (本月 vs 上月) | Matches 3-月比較 sheet the consultant already uses | Medium | Table with conditional formatting cells |

### Filtering

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Parity filter (all / 頭產 / 經產) | Consultant segments by parity constantly on-site | Medium | Applied to charts + cow table simultaneously |
| Group filter (分群) | Farms separate dry/fresh/high/low groups | Medium | Depends on farm-specific group names in data |
| Date range / month range | Multi-month trend selection | Medium | 3 / 6 / 12 month presets + custom |

### Individual Cow Table

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Sortable cow list | Find problem cows by SCC, milk drop | Low | Client-side sort on all columns |
| Search by cow ID | Consultant needs to find specific animal fast | Low | Simple string filter |
| Alert flag display (A/B/C/D/E codes) | Already in data; critical for cow-level discussion | Low | Color-coded badge per row |
| Pagination or virtual scroll | Herd of 50–150 cows; table must be usable | Low | 50 rows/page is sufficient |

### Report Export

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Export to Excel (.xlsx) | Consultant's deliverable to farmer is an Excel file | High | Openpyxl; must replicate DHI整理.xlsx structure |
| Export to PDF (printable report) | Signed/stamped reports; leave-behind for farmer | High | WeasyPrint or wkhtmltopdf via FastAPI |
| Export respects current filters | If parity filter = 頭產, export only 頭產 data | Medium | Export API must accept same filter params |

### Data Upload

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| PDF pair upload (性能檢定 + 牛乳品質) | Primary data ingestion path | High | File pair validation before conversion trigger |
| Upload status / progress feedback | Conversion can take seconds; silent wait is confusing | Medium | Simple polling or SSE status endpoint |
| Upload error messaging | Mismatched pair, corrupt PDF; consultant needs to know why | Medium | Validation before and after conversion |

---

## Differentiators

Features that make this tool demonstrably better than Excel + PDFs.

### Multi-Farm Comparison View

| Feature | Value Proposition | Complexity | Notes |
|---------|------------------|------------|-------|
| Cross-farm KPI table | Consultant sees all 3 farms on one screen; impossible in Excel | Medium | Rows = farms, columns = key metrics for same month |
| Cross-farm trend overlay | Compare milk yield trend between two farms | High | Multi-series ECharts line; axis normalization tricky |
| Farm ranking on any metric | "Which farm has worst SCC this month?" in one click | Low | Sort the cross-farm table |

**Rationale:** The consultant's core advantage is managing multiple farms simultaneously. Giving them a single view across farms that would require opening 3 different Excel files is the biggest single UX win.

### Early Warning Flags (Alert Feed)

| Feature | Value Proposition | Complexity | Notes |
|---------|------------------|------------|-------|
| Dashboard-level alert summary | "Farm 林家和: 8 cows flagged (B), up from 3 last month" — consultant enters prepared | Medium | Aggregate note-type codes from cow table |
| 泌乳早期 list (DIM < 60) | Freshening cows need attention; currently a manual sheet | Low | Filter: DIM < 60, surfaced prominently |
| 調區候選 list (group reassignment) | Consultant's action list; currently manual | Medium | Logic: SCC trend + parity + DIM criteria |

**Rationale:** The Excel workflow requires consultants to manually scan rows looking for problems. Auto-surfacing the (B) and (E) flagged cows pre-visit saves 15–20 minutes of prep per farm.

### Dynamic On-Site Presentation Mode

| Feature | Value Proposition | Complexity | Notes |
|---------|------------------|------------|-------|
| Full-screen chart mode | Tablet presentation to farmer without distracting UI chrome | Low | CSS: hide nav, enlarge charts |
| Instant filter reapplication | Farmer asks "what about just 經產 cows?" — answer in 2 seconds | Low (given proper state management) | Requires client-side filtering, not round-trip API |
| Month-by-month navigation buttons | Consultant walks farmer through last 3 months sequentially | Low | Prev/Next buttons on month selector |

**Rationale:** Consultants currently bring a laptop and flip through Excel sheets. A web dashboard that responds instantly to "show me just this group" transforms the farm visit from a presentation into a dialogue.

### SCC Distribution Chart (乳品質 Sheet)

| Feature | Value Proposition | Complexity | Notes |
|---------|------------------|------------|-------|
| SCC histogram / bucket chart | Industry standard: <5, 5–20, 20–50, >50 萬/mL buckets | Medium | Matches 2-乳品質 sheet pattern; not a simple line chart |
| Trend of % cows above threshold | "Last 3 months: 12%, 18%, 22% above 20 萬" — trend in one number | Medium | Computed from cow table per month |

**Rationale:** SCC distribution is more actionable than average SCC alone. A herd with average 15 萬 could have 2 cows at 200 萬 dragging others up — the distribution reveals this.

### Historical Trend Beyond Current Month

| Feature | Value Proposition | Complexity | Notes |
|---------|------------------|------------|-------|
| 9-month lactation curve per cow | Matches 性能檢定轉換 sheet; shows productivity trajectory | High | Requires stitching cow records across months by cow ID |
| Herd average lactation curve overlay | Industry benchmark: compare farm to regional average | High | Needs reference data; mark as v2 unless reference data available |

---

## Anti-Features

Things to deliberately NOT build in v1.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Nutritional recommendation engine | Requires domain model, liability, farmer trust; out of scope per CLAUDE.md | Display raw metrics; let consultant interpret |
| LLM-powered "ask a question" chat | Explicitly out of scope; adds infrastructure complexity | Leave API hook point; implement in v2 |
| Real-time notifications / WebSocket | Monthly data has no real-time event; complexity without benefit | Static refresh on page load |
| Mobile-first responsive layout | Consultant uses laptop + tablet; phone is not a use case | Target 1024px+ breakpoints; do not optimize for 375px |
| Multi-language support (i18n) | 繁體中文is the only language; i18n boilerplate wastes time | Hard-code Traditional Chinese; no locale switching |
| Cow health event log (treatments, vet notes) | Different system (farm management software); out of scope | DHI data only; link to external records if needed later |
| Benchmarking against regional herd norms | Requires external data source or manual reference table | Can add if consultant provides reference values |
| Drag-and-drop dashboard customization | Nice-to-have; high frontend complexity for low payoff | Fixed layout optimized for on-site presentation |
| Audit log for every data change | Adds write overhead; data is imported not edited | Log upload events only (what PDF, when, who) |
| Cow photo or RFID integration | Hardware dependency; entirely different integration surface | Text-based ID only |

---

## Dashboard Patterns

Specific patterns for multi-farm consultant dashboards, grounded in how consultants actually work.

### Pattern 1: Farm-First Navigation

Structure the top-level as "choose farm, then explore." Do NOT default to a merged view of all farms — consultants are usually focused on one farm at a time during a visit.

```
Sidebar: [Farm A] [Farm B] [Farm C] + [Cross-Farm Comparison]
Main area: Current farm context, month selector at top
```

This matches the mental model: "I'm visiting Farm A today."

### Pattern 2: KPI Cards + Trend Charts in One View

The summary page should combine instant status (KPI cards with MoM delta) and historical trend (line charts for 6–12 months) without requiring tab navigation. Consultants need both simultaneously — current status AND whether it's getting better or worse.

Layout: 4–6 KPI cards at top → 2-column chart grid below → cow table last.

### Pattern 3: Persistent Filter Bar

Filters (parity, group, date range) must be:
- Always visible (sticky header or top-of-page bar, not in a modal)
- Applied simultaneously to all charts and the cow table on the same page
- Labeled with current active state ("Showing: 經產 | Last 6 months")

Rationale: On-site, the farmer will say "show me just the first-calvers" mid-conversation. The consultant cannot afford to hunt for a filter modal.

### Pattern 4: Cross-Farm Summary Table

When the consultant wants a quick portfolio view before farm visits, a single table with one row per farm and one column per key metric (current month) is faster than any chart. Include:
- 測乳日期 (which month's data)
- 泌乳頭數
- 乳量 (avg)
- SCC (avg + % above threshold)
- MoM delta arrows for each metric

### Pattern 5: Print-Friendly Layout Toggle

Two view modes: "dashboard mode" (interactive, dark/light, full nav) and "print mode" (white background, charts optimized for A4 paper, no interactive controls). Toggle via a button; do not rely on `@media print` alone since chart libraries need explicit sizing.

---

## Report Export Patterns

UX patterns for data export workflows that avoid common pain points.

### Export UX Anti-Pattern to Avoid

Do NOT implement "export" as a download button that blindly dumps all data. Consultants leave behind reports with the farmer — the report must be clean, clearly labeled, and match what was on screen.

### Recommended Export Flow

1. Consultant configures view (farm, month, filters applied)
2. "Export" button opens a side panel (not a modal) with:
   - Preview of what will be exported ("Showing: 林家和 | 2026.04 | 全部胎次")
   - Format selector: Excel / PDF
   - Optional: include/exclude sections (summary, charts, cow table)
   - Optional: add consultant name to footer
3. Click "Generate" → server-side generation → download starts
4. Loading indicator during generation (PDF takes 2–5 seconds)

### Excel Export Structure

Mirror the existing DHI整理.xlsx sheet structure because farmers already understand it:
- Sheet 1: Summary (1-總表 equivalent)
- Sheet 2: Monthly comparison (3-月比較 equivalent)
- Sheet 3: Cow detail table (4-牛群資料表 equivalent)
- Sheet 4: SCC quality distribution (2-乳品質 equivalent)

Use openpyxl with conditional formatting (red fill for high SCC, yellow for flagged cows). Do not export raw API JSON to a flat sheet — it will be unreadable.

### PDF Export Structure

Single-page-per-section layout for A4 printing:
- Page 1: Farm header + KPI summary + MoM comparison table
- Page 2: Charts (milk trend, SCC trend, parity distribution)
- Page 3: Cow detail table (may span multiple pages)
- Footer: Consultant name, generation date, farm name

Use WeasyPrint (Python-native, no headless Chrome dependency) or a server-rendered HTML → PDF approach. ECharts charts should be exported as SVG/PNG server-side before PDF embedding — avoid rendering charts in headless browser.

### Upload UX Flow

1. Upload screen: drag-and-drop zone accepting PDF files
2. System validates pairs in real time as files are dropped ("需要配對: 找到 性能檢定, 等待 牛乳品質")
3. Once pair detected: "準備轉檔: 2026.02 林家和 ✓" — confirm button appears
4. Conversion runs: progress indicator (spinner + "轉檔中...")
5. Success: "匯入完成，已新增 47 筆資料" or failure: specific error message
6. Redirect to that farm/month view automatically on success

This flow prevents the common error of uploading only one PDF and wondering why nothing appeared.

---

## Feature Dependencies

```
Upload PDF pair
  → Trigger conversion scripts (existing: src/milk_pdf_to_xlsx.py)
  → Store result in database
  → Farm/month becomes available in all views

Authentication
  → Role enforcement
  → Farm access control
  → Admin panel

Filter state (parity, group, date range)
  → Applied to: KPI cards, all charts, cow table, export
  → Must be single source of truth in frontend state (Pinia store)

Export
  → Requires filter state
  → Requires server-side rendering (not client-side)
  → PDF requires chart PNG generation step
```

## MVP Recommendation

Prioritize:
1. Authentication + role enforcement (without this, nothing else is safe to deploy)
2. Database layer + data importer (without this, the hardcoded FARM_FILES in extractor.py blocks everything)
3. Farm dashboard — KPI cards + trend charts + MoM comparison (core use case)
4. Dynamic parity/group filters (transforms static display into interactive tool)
5. PDF upload + conversion trigger (data ingestion path)
6. Excel export (consultant deliverable)

Defer to v2:
- PDF export (complex; Excel covers most needs)
- Cross-farm comparison view (single farm covers immediate need)
- Per-cow lactation curve (requires multi-month cow ID stitching)
- LLM integration (explicitly out of scope)

## Sources

- Codebase analysis: `backend/extractor.py` (data model), `backend/main.py` (API surface), `.planning/PROJECT.md` (requirements), CLAUDE.md (constraints)
- Domain knowledge: DHI data standards (CDCB, ICAR), DairyComp 305 UX patterns, DRMS web portal feature set — MEDIUM confidence (training data, no live verification)
- Agricultural SaaS patterns: Conservis, FarmLogs, Granular dashboard conventions — MEDIUM confidence
