# Phase 03: 牧場儀表板與牛隻表格 - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning
**Source:** Design discussion in session (sidebar + role-based nav evolution)

<domain>
## Phase Boundary

Phase 3 delivers a complete Vue 3 + Vite frontend with:
1. **Sidebar navigation shell** replacing the top-bar navigation
2. **Role-based routing** — 顧問/管理者 see multi-farm views; 牧場 identity sees single-farm views
3. **Single-farm sub-views**: 儀表板, 比較圖, 牛群資料表, 警示 (4 pages under sidebar)
4. **Multi-farm sub-views**: 多牧場總覽 (farm cards), 趨勢比較 (cross-farm trend charts)
5. **Multi-farm filters** with saved presets (localStorage)

Note: Vite scaffold, stores (farm.js, filter.js), and most individual components (KpiCard, TrendChart, CowTable, etc.) are already implemented. Phase 3 replanning focuses on the **navigation architecture** and **new views/stores** not covered by the original plans.

</domain>

<decisions>
## Implementation Decisions

### D-01: Layout — Sidebar Shell
- Replace `TopBar.vue` horizontal navigation with a fixed **left sidebar** (`SideNav.vue`)
- Sidebar width: 256px (matches `code.html` / `code_comparison.html` reference designs)
- Main content area: `margin-left: 256px`, full height
- TopBar is **not removed** — it becomes a slim top strip for farm/month selectors (single-farm views only) or page title (multi-farm views)
- Sidebar shows role-appropriate nav items only

### D-02: Role-Based Navigation
- **顧問 / 管理者 role**: Sidebar shows multi-farm views
  - 多牧場儀表板 (farm cards overview)
  - 趨勢比較圖 (cross-farm trend charts)
- **牧場 role**: Sidebar shows single-farm views
  - 儀表板
  - 比較圖 (本月 vs 上月)
  - 牛群資料表
  - 警示
- Role switching for demo: simple state in Pinia (no real auth in Phase 3); a visible role selector in sidebar footer or top area
- Full auth/login deferred to later phase

### D-03: Single-Farm Sub-Views (4 pages)
| Route | View | Content |
|-------|------|---------|
| `/farm/dashboard` | `DashboardView.vue` | KPI cards + trend charts (existing) |
| `/farm/comparison` | `ComparisonView.vue` | 本月 vs 上月 bar charts per metric |
| `/farm/cows` | `CowTableView.vue` | Full cow table with sort/search/pagination/alerts |
| `/farm/alerts` | `AlertsView.vue` | Cows with active alert codes (A/B/C/D/E), grouped by alert type |

- Farm/month selector stays in TopBar (visible when in single-farm route)
- Filtering (parity/group via filter.js store) applies across all 4 views

### D-04: Multi-Farm Sub-Views (2 pages)
| Route | View | Content |
|-------|------|---------|
| `/overview` | `OverviewView.vue` | Farm cards (existing), comparison table |
| `/overview/trends` | `TrendComparisonView.vue` | Cross-farm trend charts per metric (乳量/泌乳頭數/SCC) |

- Farm/month selector NOT shown in TopBar for multi-farm routes (replaced by filter panel)
- `OverviewView.vue` already exists and covers the cards + table — keep it, just rewire nav

### D-05: Multi-Farm Filters (overviewFilter store — NEW)
New Pinia store `frontend/src/stores/overviewFilter.js` (separate from existing `filter.js`):

```js
selectedFarms     // Set<string> — which farms to show (default: all)
timeRange         // 3 | 6 | 12 | 'custom' (default: 12)
startDate         // 'YYYY.M' | null (custom range start)
endDate           // 'YYYY.M' | null (custom range end)
thresholds        // { scc: null, milk: null, open_days: null } — metric filter thresholds
alertTypes        // Set<string> — filter to farms with cows having these alerts: '(A)'...'(E)'
savedPresets      // Array<{ name: string, filters: FilterSnapshot }> — loaded from localStorage
```

Actions:
- `setSelectedFarms(farms)`, `toggleFarm(farmName)`
- `setTimeRange(value)`, `setCustomRange(start, end)`
- `setThreshold(metric, value)`, `clearThresholds()`
- `setAlertTypes(types)`
- `savePreset(name)` — snapshots current filter state to savedPresets + persists to localStorage
- `applyPreset(name)` — restores a saved preset
- `deletePreset(name)`
- `resetAll()` — resets to defaults

### D-06: Saved Filter Presets
- Storage: `localStorage` key `dhi_overview_presets` (demo phase)
- Format: `[{ name: string, filters: { selectedFarms, timeRange, startDate, endDate, thresholds, alertTypes } }]`
- UI: dropdown/panel showing preset list + "儲存目前篩選" button + delete per preset
- Migration path: in future phase, replace localStorage read/write with API calls (`GET/POST /api/user/presets`)

### D-07: Trend Chart Time Range
- Trend comparison charts (`TrendComparisonView`) share `overviewFilter.timeRange`
- No independent time axis on the trend page — both OverviewView and TrendComparisonView react to the same filter state
- **Why:** Simpler store design; user sets time range once in the filter panel, both pages update consistently

### D-08: Trend Comparison Charts (TrendComparisonView — NEW)
Inspired by `code_comparison.html` reference, implemented with **ECharts** (not SVG polylines):
- Chart 1: 平均乳量 (kg) — one line per farm
- Chart 2: 泌乳頭數 (頭) — one line per farm
- Chart 3: 平均體細胞數 (萬/mL) — one line per farm
- X-axis: months within selected timeRange
- Each farm gets a distinct color from a fixed palette
- Legend shows farm names; clicking toggles farm visibility

### D-09: Alert Grouping (AlertsView — NEW)
- Groups cows by alert code (A/B/C/D/E)
- Shows: alert code label, count, list of cows (farm_id, milk, relevant metric)
- References existing `alerts.js` utility and alert code definitions from CLAUDE.md:
  - (A) = 高乳脂, (B) = 高體細胞數, (C) = 低乳量, (D) = 低泌乳天數, (E) = 高游離脂肪酸

### Claude's Discretion
- Exact sidebar visual style: follow `code.html` Material Design 3 direction but mapped to existing `brand-*` Tailwind palette (not full MD3 token overhaul — keep tailwind.config.js simple)
- ComparisonView chart type: ECharts grouped bar chart (本月 vs 上月)
- Filter UI placement: collapsible filter panel in the main content area (not a modal), shown/hidden via sidebar button or top-right icon
- Pagination and sort in AlertsView: not required (cows per alert type are usually few)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Implementation (read to understand current state)
- `frontend/src/stores/farm.js` — existing farm/month state
- `frontend/src/stores/filter.js` — existing single-farm filter (parity, group, time range)
- `frontend/src/components/TopBar.vue` — current nav component to be restructured
- `frontend/src/views/DashboardView.vue` — existing single-farm dashboard
- `frontend/src/views/OverviewView.vue` — existing multi-farm overview (to be kept)
- `frontend/src/router/index.js` — current routes to be restructured
- `frontend/src/utils/alerts.js` — alert code utilities

### Reference Designs
- `code.html` (root dir) — visual reference for sidebar + KPI bento grid design
- `code_comparison.html` (root dir) — visual reference for trend comparison charts layout

### Project Spec
- `.planning/REQUIREMENTS.md` — DASH-*, FILT-*, COW-* requirement IDs
- `.planning/ROADMAP.md` — Phase 3 success criteria
- `.planning/phases/03-dashboard-cow-table/03-UI-SPEC.md` — original UI spec (single-farm focused; sidebar decisions supersede nav section)
- `CLAUDE.md` — alert code definitions (A/B/C/D/E), tech stack, conventions

</canonical_refs>

<specifics>
## Specific Ideas

- Sidebar active state: left border accent (`border-l-4 border-brand-600`) matching `code_comparison.html` style
- Farm cards in OverviewView: clicking a card switches to single-farm role + navigates to `/farm/dashboard`
- Filter preset saved with timestamp: show "儲存於 MM/DD HH:mm" in preset list
- AlertsView: badge counts next to alert labels in sidebar nav (shows total alert cows for selected farm/month)
- TrendComparisonView color palette: use ECharts default palette (first 3-5 colors) for farm lines

</specifics>

<deferred>
## Deferred Ideas

- Full auth/login system — deferred to later phase (CLAUDE.md: passwords/security in separate phase)
- Backend user preferences API for saved presets — demo uses localStorage; API migration is a future phase
- Dark mode — not in scope for Phase 3
- Mobile responsive sidebar (hamburger menu) — not in scope for Phase 3
- ComparisonView: month-over-month for more than 2 months — Phase 3 only does current vs previous
- Export to PDF/Excel — deferred

</deferred>

---

*Phase: 03-dashboard-cow-table*
*Context gathered: 2026-04-24 from design discussion (sidebar + role-based nav)*
