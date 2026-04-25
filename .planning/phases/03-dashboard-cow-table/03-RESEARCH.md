# Phase 3: 牧場儀表板與牛隻表格 - Research

**Researched:** 2026-04-23
**Domain:** Vue 3 + Vite frontend, ECharts data visualization, Tailwind CSS, client-side filtering
**Confidence:** HIGH

## Summary

Phase 3 replaces the current single-file CDN-loaded frontend (`frontend/index.html` with embedded `data.js`) with a proper Vue 3 + Vite SPA. The existing prototype already demonstrates the data shape and UI patterns needed -- the task is to migrate to a maintainable component architecture with proper state management via Pinia, ECharts integration via vue-echarts, and Tailwind CSS v4 via its native Vite plugin.

The API data structure is already well-defined from the current `backend/extractor.py`: each farm-month returns `{ measurement_date, summary: { current, comparison }, cows: [...] }` where `current` has `{ avg, heifer, multi }` breakdowns and `comparison` has `{ prev, curr }` pairs. Phase 2 will formalize this into database-backed API endpoints, but the response shape will remain the same. The cow array contains 25+ fields per record including alerts codes `["(A)", "(B)", ...]`.

**Primary recommendation:** Use Vue 3 Composition API + Pinia as single source of truth for filter state, vue-echarts for declarative chart binding, and Tailwind CSS v4 with the `@tailwindcss/vite` plugin. Load all cow data for a farm-month in one API call (30-150 records) and filter/sort entirely client-side.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DASH-01 | 儀表板頂部常駐農場+月份選擇器，預設最新月份 | Vue Router + Pinia store for current farm/month; API: `GET /api/farms` and `GET /api/farms/{farm}/months` |
| DASH-02 | KPI 卡片（平均乳量、SCC、泌乳頭數、空胎天數）+ MoM delta 箭頭色碼 | Data from `summary.current` and `summary.comparison`; component pattern in Code Examples |
| DASH-03 | 12 個月趨勢折線圖（乳量、SCC、泌乳頭數） | vue-echarts line chart; requires fetching multiple months or a dedicated trend API endpoint |
| DASH-04 | 胎次分布長條圖 | vue-echarts bar chart computed from `cows[].parity` client-side |
| DASH-05 | SCC 區間分布圖（<5, 5-20, 20-50, >50 萬/mL） | vue-echarts bar chart computed from `cows[].scc` client-side |
| FILT-01 | 胎次篩選（全部/頭產/經產）同步至圖表+KPI+表格 | Pinia `parityFilter` ref; computed properties derive filtered data |
| FILT-02 | 分群篩選同步至所有元件 | Pinia `groupFilter` ref; cow records have `group` field |
| FILT-03 | 時間範圍篩選（3/6/12 月 + 自訂）套用至趨勢圖 | Pinia `timeRange` ref; trend chart watches this to slice data |
| COW-01 | 牛隻列表依任意欄位排序 | Client-side sort with `Array.prototype.sort()` + `sortKey`/`sortDir` state |
| COW-02 | 依場內編號或統一編號搜尋 | Client-side filter on `farm_id` and `national_id` fields |
| COW-03 | A/B/C/D/E 警示碼色碼標籤 | `alerts` array already parsed; map to Tailwind badge colors |
| COW-04 | 分頁顯示每頁 50 筆 | Client-side pagination with `currentPage` ref |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| vue | 3.5.33 | UI framework | Project decision (CLAUDE.md) [VERIFIED: npm registry] |
| vite | 8.0.9 | Build tool + dev server | Standard Vue 3 build tool [VERIFIED: npm registry] |
| @vitejs/plugin-vue | 6.0.6 | Vue SFC support in Vite | Required for `.vue` files [VERIFIED: npm registry] |
| vue-router | 5.0.6 | Client-side routing | Dashboard pages, future multi-page support [VERIFIED: npm registry] |
| pinia | 3.0.4 | State management | Project decision (STATE.md): "Pinia 作為篩選狀態唯一來源" [VERIFIED: npm registry] |
| echarts | 6.0.0 | Chart library | Project decision (CLAUDE.md) [VERIFIED: npm registry] |
| vue-echarts | 8.0.1 | Vue 3 declarative ECharts wrapper | Composition API provide/inject, reactive options [VERIFIED: npm registry] |
| tailwindcss | 4.2.4 | Utility-first CSS | Project decision (CLAUDE.md) [VERIFIED: npm registry] |
| @tailwindcss/vite | 4.2.4 | Tailwind v4 Vite plugin | Native Vite integration, no PostCSS config needed [VERIFIED: npm registry] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| axios | (latest) | HTTP client | API calls to backend; cleaner than raw fetch for interceptors/error handling [ASSUMED] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| vue-echarts | Raw echarts + refs | More boilerplate, manual lifecycle management; vue-echarts handles resize/dispose automatically |
| axios | Native fetch | fetch is lighter but lacks interceptors for JWT token injection (needed for auth from Phase 1) |
| Tailwind CSS v4 | Tailwind CSS v3 | v3 requires PostCSS config + content globs; v4 has native Vite plugin with auto-detection |

**Installation:**
```bash
npm create vite@latest frontend -- --template vue
cd frontend
npm install vue-router pinia echarts vue-echarts axios
npm install -D tailwindcss @tailwindcss/vite
```

**Note on ECharts v6:** ECharts 6.0.0 was recently released. [VERIFIED: npm registry] vue-echarts 8.0.1 should support it. If compatibility issues arise, pin echarts to `^5.5.0` as fallback. [ASSUMED]

## Architecture Patterns

### Recommended Project Structure
```
frontend/
├── index.html
├── vite.config.js
├── src/
│   ├── main.js              # App entry, router + pinia setup
│   ├── App.vue               # Root layout (top bar with farm/month selector)
│   ├── router/
│   │   └── index.js          # Route definitions
│   ├── stores/
│   │   ├── farm.js           # Current farm, month, available farms/months
│   │   └── filter.js         # Parity filter, group filter, time range
│   ├── composables/
│   │   ├── useFarmData.js    # Fetch + cache farm-month data
│   │   ├── useFilteredCows.js # Computed filtered cow list from store
│   │   └── useKpi.js         # Compute KPI values from filtered cows
│   ├── components/
│   │   ├── TopBar.vue         # Farm selector + month selector (DASH-01)
│   │   ├── KpiCard.vue        # Single KPI card with delta arrow (DASH-02)
│   │   ├── KpiRow.vue         # Row of 4 KPI cards
│   │   ├── TrendChart.vue     # 12-month line chart (DASH-03)
│   │   ├── ParityChart.vue    # Parity distribution bar chart (DASH-04)
│   │   ├── SccDistChart.vue   # SCC distribution bar chart (DASH-05)
│   │   ├── FilterBar.vue      # Parity + group + time range filters (FILT-01/02/03)
│   │   └── CowTable.vue       # Sortable, searchable, paginated table (COW-01/02/03/04)
│   ├── views/
│   │   └── DashboardView.vue  # Main dashboard page composing all components
│   ├── utils/
│   │   ├── api.js             # Axios instance with base URL
│   │   └── alerts.js          # Alert code → color/label mapping
│   └── assets/
│       └── main.css           # @import "tailwindcss";
```

### Pattern 1: Pinia as Single Source of Truth for Filters
**What:** All filter state (parity, group, time range) lives in a single Pinia store. Every component reads from the store, never from local state.
**When to use:** Whenever multiple components must stay in sync (KPI, charts, cow table, future export).
**Example:**
```javascript
// stores/filter.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFilterStore = defineStore('filter', () => {
  const parityFilter = ref('all')    // 'all' | 'heifer' | 'multi'
  const groupFilter = ref(null)       // null = all groups
  const timeRange = ref(12)           // months for trend chart

  return { parityFilter, groupFilter, timeRange }
})
```
[ASSUMED - standard Pinia pattern]

### Pattern 2: Client-Side Filtering (No API Call on Filter Change)
**What:** Load all cow data for a farm-month in one API call. Derive filtered views via computed properties.
**When to use:** Cow counts per farm-month are 30-150 (per STATE.md decision). Client-side filtering ensures sub-second response.
**Example:**
```javascript
// composables/useFilteredCows.js
import { computed } from 'vue'
import { useFilterStore } from '../stores/filter'

export function useFilteredCows(cows) {
  const filter = useFilterStore()

  return computed(() => {
    let result = cows.value
    if (filter.parityFilter === 'heifer') {
      result = result.filter(c => c.parity === 1)
    } else if (filter.parityFilter === 'multi') {
      result = result.filter(c => c.parity > 1)
    }
    if (filter.groupFilter) {
      result = result.filter(c => c.group === filter.groupFilter)
    }
    return result
  })
}
```
[ASSUMED - standard Vue computed pattern]

### Pattern 3: KPI Delta Calculation
**What:** KPI cards show current value + delta arrow compared to previous month.
**When to use:** DASH-02 requires MoM comparison with color coding.
**Example:**
```javascript
// composables/useKpi.js
export function computeKpi(current, previous) {
  const delta = current - previous
  const direction = delta > 0 ? 'up' : delta < 0 ? 'down' : 'flat'
  return { current, delta, direction }
}
```
**Color mapping:**
- `up` on positive metrics (milk yield): green arrow
- `up` on negative metrics (SCC, open days): red arrow (higher is worse)
- `down` on positive metrics: red arrow
- `down` on negative metrics: green arrow
- `flat`: gray dash

[ASSUMED - domain logic from CLAUDE.md normal ranges]

### Anti-Patterns to Avoid
- **API call per filter change:** Data is small enough to filter client-side. Making API calls creates race conditions and latency.
- **Duplicating filter state across components:** Use Pinia store, not props drilling or local state copies.
- **Embedding data in HTML:** Current prototype uses `window.__DHI_DATA__` embedded in HTML. Phase 3 must fetch from API.
- **Using ECharts imperatively in Vue:** Don't call `echarts.init()` manually; use vue-echarts `<v-chart>` component for automatic lifecycle management.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Chart rendering + resize | Manual echarts.init/dispose/resize | vue-echarts `<v-chart>` | Handles resize observer, dispose on unmount, reactive options |
| CSS utility system | Custom CSS classes | Tailwind CSS v4 | Consistent design tokens, responsive utilities |
| State management | Event bus or provide/inject for global state | Pinia | DevTools support, SSR-ready, type-safe |
| Client-side routing | Manual hash-based routing | Vue Router | Navigation guards for auth, nested routes |
| Table sorting | Custom sort implementation | Native `Array.sort()` with a composable | Simple enough to not need a library, but abstract into composable for reuse |
| Pagination | Complex pagination logic | Simple `computed` slice | With max 150 records and 50/page, this is 3 pages max |

**Key insight:** The data volume is small (30-150 cows per farm-month). This means no virtual scrolling, no server-side pagination, no debounced search -- simple client-side operations suffice.

## Common Pitfalls

### Pitfall 1: ECharts Instance Not Disposing on Route Change
**What goes wrong:** Memory leaks when navigating away from dashboard without disposing ECharts instances.
**Why it happens:** Raw `echarts.init()` in `onMounted` without cleanup.
**How to avoid:** Use vue-echarts which handles dispose automatically. If using raw ECharts, call `chart.dispose()` in `onUnmounted`.
**Warning signs:** Browser memory steadily increasing on repeated navigation.

### Pitfall 2: Tailwind v4 Breaking Changes from v3
**What goes wrong:** Tailwind v4 has a completely different configuration system. No `tailwind.config.js`, no `content` array, no `postcss.config.js`.
**Why it happens:** v4 uses CSS-first configuration with `@theme` directive instead of JS config.
**How to avoid:** Use `@tailwindcss/vite` plugin. Configuration goes in CSS files using `@theme { }` blocks. Do NOT create `tailwind.config.js`.
**Warning signs:** Classes not being detected; old tutorials showing `tailwind.config.js` setup.

### Pitfall 3: KPI Delta Arrow Polarity Confusion
**What goes wrong:** Showing green "up" arrow for SCC increase (which is bad -- higher SCC means infection risk).
**Why it happens:** Applying the same color logic to all metrics without considering polarity.
**How to avoid:** Define a `polarity` map: positive metrics (milk) vs negative metrics (SCC, open_days). Flip the color for negative-polarity metrics.
**Warning signs:** Users seeing green arrows for worsening health indicators.

### Pitfall 4: Month Key Format Inconsistency
**What goes wrong:** API returns months as `"2026.1"` (no leading zero) but UI displays or sorts them differently.
**Why it happens:** The existing convention uses `"YYYY.M"` format (e.g., `"2026.1"`, `"2026.12"`).
**How to avoid:** Always use the raw month key for API calls; use a display formatter for UI. Sort months by parsing to Date objects.
**Warning signs:** Month selector showing months in wrong order.

### Pitfall 5: ECharts v6 Compatibility with vue-echarts
**What goes wrong:** ECharts recently released v6.0.0. vue-echarts may have compatibility issues.
**Why it happens:** Major version bump in ECharts may change APIs.
**How to avoid:** Test with ECharts v6 first. If issues arise, pin to `echarts@^5.5.0`. Check vue-echarts GitHub issues for v6 compatibility reports.
**Warning signs:** Chart rendering errors, missing chart types.

### Pitfall 6: CORS and API Base URL in Development
**What goes wrong:** Vite dev server runs on port 5173, FastAPI on port 8000. API calls fail due to CORS or wrong URL.
**Why it happens:** Development setup has separate frontend and backend servers.
**How to avoid:** Configure Vite proxy in `vite.config.js` to forward `/api` requests to FastAPI backend.
**Warning signs:** Network errors in browser console during development.

## Code Examples

### Vite Configuration with Tailwind v4 and API Proxy
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```
[CITED: tailwindcss.com/docs - Vite installation guide, ASSUMED for proxy config]

### Tailwind CSS v4 Entry Point
```css
/* src/assets/main.css */
@import "tailwindcss";

/* Custom theme overrides if needed */
@theme {
  --color-primary: #2563eb;
  --color-danger: #dc2626;
  --color-success: #16a34a;
  --color-warning: #d97706;
}
```
[CITED: tailwindcss.com/blog/tailwindcss-v4]

### vue-echarts Line Chart (Trend)
```vue
<template>
  <v-chart :option="chartOption" autoresize style="height: 300px" />
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const props = defineProps({ trendData: Object })

const chartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['乳量', 'SCC', '泌乳頭數'] },
  xAxis: { type: 'category', data: props.trendData.months },
  yAxis: [
    { type: 'value', name: '乳量 (kg)' },
    { type: 'value', name: 'SCC (萬/mL)' },
  ],
  series: [
    { name: '乳量', type: 'line', data: props.trendData.milk },
    { name: 'SCC', type: 'line', yAxisIndex: 1, data: props.trendData.scc },
    { name: '泌乳頭數', type: 'line', data: props.trendData.count },
  ],
}))
</script>
```
[ASSUMED - standard vue-echarts pattern with tree-shaking]

### Alert Code Color Mapping
```javascript
// utils/alerts.js
export const ALERT_CONFIG = {
  '(A)': { label: 'A 高乳脂',        color: 'bg-yellow-100 text-yellow-800' },
  '(B)': { label: 'B 高體細胞數',    color: 'bg-red-100 text-red-800' },
  '(C)': { label: 'C 低乳量',        color: 'bg-orange-100 text-orange-800' },
  '(D)': { label: 'D 低泌乳天數',    color: 'bg-blue-100 text-blue-800' },
  '(E)': { label: 'E 高游離脂肪酸',  color: 'bg-purple-100 text-purple-800' },
}
```
[VERIFIED: alert codes from CLAUDE.md]

### KPI Card Component
```vue
<template>
  <div class="rounded-lg bg-white p-4 shadow">
    <div class="text-sm text-gray-500">{{ label }}</div>
    <div class="mt-1 text-2xl font-bold">{{ formatted }}</div>
    <div class="mt-1 flex items-center text-sm" :class="arrowColor">
      <span v-if="direction === 'up'">&#9650;</span>
      <span v-else-if="direction === 'down'">&#9660;</span>
      <span v-else>&#9644;</span>
      <span class="ml-1">{{ Math.abs(delta).toFixed(1) }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: Number,
  delta: Number,
  unit: { type: String, default: '' },
  positiveIsGood: { type: Boolean, default: true },
})

const formatted = computed(() =>
  props.value != null ? `${props.value.toFixed(1)}${props.unit}` : '--'
)
const direction = computed(() =>
  props.delta > 0 ? 'up' : props.delta < 0 ? 'down' : 'flat'
)
const arrowColor = computed(() => {
  if (direction.value === 'flat') return 'text-gray-400'
  const isPositive = direction.value === 'up'
  return (isPositive === props.positiveIsGood) ? 'text-green-600' : 'text-red-600'
})
</script>
```
[ASSUMED - standard Vue pattern]

### API Data Structure (from existing extractor.py)
```javascript
// What the API returns for GET /api/farms/{farm}/{month}
{
  measurement_date: "2026-01-14",
  summary: {
    current: {
      count: { avg: 54, heifer: 15, multi: 39 },
      milk:  { avg: 33.4, heifer: 30.5, multi: 34.5 },
      scc:   { avg: 13.2, heifer: 5.4, multi: 16.2 },
      // ... other metrics with avg/heifer/multi breakdown
    },
    comparison: {
      count: { prev: 52, curr: 54 },
      milk:  { prev: 32.3, curr: 33.4 },
      // ... other metrics with prev/curr pairs
    },
  },
  cows: [
    {
      farm_id: "1234", national_id: "TW12345",
      milk: 35.2, scc: 8.5, urea: 12.3,
      parity: 2, dim: 120, open_days: 85,
      alerts: ["(A)", "(B)"], group: "高產",
      // ... 25+ fields total
    },
    // ... 30-150 cows
  ],
}
```
[VERIFIED: from backend/extractor.py source code]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Tailwind v3 (JS config + PostCSS) | Tailwind v4 (CSS-first + Vite plugin) | Jan 2025 | No `tailwind.config.js`, no PostCSS config; use `@import "tailwindcss"` and `@theme {}` |
| ECharts v5 | ECharts v6 | 2025 | Major version bump; vue-echarts 8.x supports it [ASSUMED] |
| Vue CDN loading | Vue + Vite SFC build | Standard since Vue 3.0 | Proper component system, HMR, tree-shaking |
| Options API | Composition API (`<script setup>`) | Vue 3.2+ | Cleaner composables, better TypeScript support |

**Deprecated/outdated:**
- `tailwind.config.js` / `postcss.config.js`: Not needed with Tailwind v4 + `@tailwindcss/vite`
- `window.__DHI_DATA__` embedded data: Must be replaced with API fetch calls
- CDN-loaded Vue/ECharts: Must be replaced with npm packages + Vite bundling

## DASH-03 Trend Data Strategy

DASH-03 requires 12-month trend data (乳量, SCC, 泌乳頭數 over time). The current API structure returns data per-month. Two approaches:

**Option A: Multiple API calls** -- Fetch each month individually, extract summary values client-side. Simple but requires N API calls.

**Option B: Dedicated trend endpoint** -- Backend provides `GET /api/farms/{farm}/trend?months=12` returning pre-aggregated time series. Single call, but requires backend work (Phase 2 scope).

**Recommendation:** The existing API already has `GET /api/farms/{farm}/months` returning available months. Phase 2 should include a trend endpoint or the dashboard can batch-fetch summaries. Since STATE.md says "牛隻資料以月份一次全量載入後在客戶端篩選", a reasonable approach is to fetch all available months' summaries in parallel on farm selection. With 3-12 months of data, this is a small payload. [ASSUMED]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | vue-echarts 8.0.1 is compatible with ECharts 6.0.0 | Standard Stack | Charts won't render; fallback: pin echarts@^5.5.0 |
| A2 | axios is preferred over fetch for HTTP | Standard Stack | Low risk; fetch works fine, axios adds auth interceptors for Phase 1 JWT |
| A3 | DASH-03 trend data can be assembled from parallel month fetches | DASH-03 Strategy | If too slow, need a dedicated backend trend endpoint |
| A4 | Tailwind v4 color utilities (bg-red-100, text-green-600) work the same as v3 | Code Examples | May need @theme adjustments; core utilities are the same |

## Open Questions

1. **DASH-03 Trend API Endpoint**
   - What we know: Current API returns single-month data. Trend chart needs 12 months.
   - What's unclear: Will Phase 2 provide a dedicated trend endpoint, or should the frontend fetch each month separately?
   - Recommendation: Plan for client-side aggregation from parallel fetches; if Phase 2 adds a trend endpoint, use it instead.

2. **ECharts v6 Stability**
   - What we know: ECharts 6.0.0 was just released. vue-echarts 8.0.1 is the latest wrapper.
   - What's unclear: Whether vue-echarts fully supports ECharts v6.
   - Recommendation: Start with ECharts v6 + vue-echarts 8.x. If issues, fallback to ECharts 5.5.x.

3. **Group Names for FILT-02**
   - What we know: Cow records have a `group` field (e.g., "高產"). Groups vary by farm.
   - What's unclear: Full list of possible group values.
   - Recommendation: Dynamically extract unique group values from loaded cow data. No hardcoding.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | Vite build, npm | Yes | v20.20.2 | -- |
| npm | Package management | Yes | 10.8.2 | -- |
| Python + FastAPI | Backend API (Phase 2) | Yes | 3.13 | -- |

**Missing dependencies with no fallback:** None.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Vitest (standard for Vite projects) [ASSUMED] |
| Config file | `frontend/vitest.config.js` (Wave 0 creation) |
| Quick run command | `cd frontend && npx vitest run --reporter=verbose` |
| Full suite command | `cd frontend && npx vitest run` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DASH-01 | Farm/month selector updates store | unit | `npx vitest run src/stores/__tests__/farm.test.js` | No - Wave 0 |
| DASH-02 | KPI delta calculation + polarity | unit | `npx vitest run src/composables/__tests__/useKpi.test.js` | No - Wave 0 |
| DASH-03 | Trend data aggregation | unit | `npx vitest run src/composables/__tests__/useTrend.test.js` | No - Wave 0 |
| DASH-04 | Parity distribution computed | unit | `npx vitest run src/composables/__tests__/useChartData.test.js` | No - Wave 0 |
| DASH-05 | SCC distribution buckets | unit | `npx vitest run src/composables/__tests__/useChartData.test.js` | No - Wave 0 |
| FILT-01 | Parity filter applies to all data | unit | `npx vitest run src/composables/__tests__/useFilteredCows.test.js` | No - Wave 0 |
| FILT-02 | Group filter applies to all data | unit | Same as FILT-01 | No - Wave 0 |
| FILT-03 | Time range filter slices trend data | unit | Same as DASH-03 | No - Wave 0 |
| COW-01 | Sort by any column | unit | `npx vitest run src/composables/__tests__/useSortedCows.test.js` | No - Wave 0 |
| COW-02 | Search by farm_id/national_id | unit | Same as COW-01 | No - Wave 0 |
| COW-03 | Alert code mapping | unit | `npx vitest run src/utils/__tests__/alerts.test.js` | No - Wave 0 |
| COW-04 | Pagination (50 per page) | unit | Same as COW-01 | No - Wave 0 |

### Sampling Rate
- **Per task commit:** `cd frontend && npx vitest run --reporter=verbose`
- **Per wave merge:** `cd frontend && npx vitest run`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `npm install -D vitest @vue/test-utils jsdom` -- test framework installation
- [ ] `frontend/vitest.config.js` -- Vitest configuration
- [ ] `frontend/src/stores/__tests__/` -- store test directory
- [ ] `frontend/src/composables/__tests__/` -- composable test directory
- [ ] `frontend/src/utils/__tests__/` -- utility test directory

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No (Phase 1 scope) | JWT handled by backend; frontend stores token in memory |
| V3 Session Management | No (Phase 1 scope) | httpOnly refresh cookie set by backend |
| V4 Access Control | Partial | Frontend hides unauthorized farms from selector; enforcement is backend-side (AUTH-03) |
| V5 Input Validation | Yes | Sanitize search input in cow table; no user-generated content rendered as HTML |
| V6 Cryptography | No | No crypto operations in frontend |

### Known Threat Patterns for Vue 3 SPA

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| XSS via `v-html` | Tampering | Never use `v-html` with user data; Vue auto-escapes `{{ }}` |
| Token exposure in localStorage | Information Disclosure | Store JWT in memory (variable), refresh token in httpOnly cookie |
| Open redirect via router | Spoofing | Validate navigation targets in route guards |

## Sources

### Primary (HIGH confidence)
- npm registry -- verified versions for vue 3.5.33, vite 8.0.9, echarts 6.0.0, vue-echarts 8.0.1, pinia 3.0.4, vue-router 5.0.6, tailwindcss 4.2.4, @tailwindcss/vite 4.2.4
- `backend/extractor.py` -- verified API data structure and cow record fields
- `frontend/index.html` + `frontend/data.js` -- verified existing prototype structure
- STATE.md -- locked decisions (Pinia, client-side filtering)

### Secondary (MEDIUM confidence)
- [Tailwind CSS v4 announcement](https://tailwindcss.com/blog/tailwindcss-v4) -- CSS-first configuration, Vite plugin
- [Tailwind CSS Vite installation docs](https://tailwindcss.com/docs) -- @tailwindcss/vite setup
- [vue-echarts GitHub](https://github.com/ecomfe/vue-echarts) -- Vue 3 Composition API integration

### Tertiary (LOW confidence)
- ECharts v6 + vue-echarts 8.x compatibility -- not verified with official compatibility matrix

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all versions verified against npm registry, project decisions locked in STATE.md
- Architecture: HIGH -- patterns derived from existing data structures and Vue 3 best practices
- Pitfalls: MEDIUM -- Tailwind v4 migration and ECharts v6 compatibility are based on recent changes

**Research date:** 2026-04-23
**Valid until:** 2026-05-23 (30 days -- stable ecosystem, no fast-moving dependencies)
