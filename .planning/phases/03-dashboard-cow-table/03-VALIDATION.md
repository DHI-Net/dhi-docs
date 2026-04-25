---
phase: 3
slug: dashboard-cow-table
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-23
---

# Phase 3 -- Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Vitest (standard for Vite projects) |
| **Config file** | `frontend/vitest.config.js` (Wave 0 creation) |
| **Quick run command** | `cd frontend && npx vitest run --reporter=verbose` |
| **Full suite command** | `cd frontend && npx vitest run` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd frontend && npx vitest run --reporter=verbose`
- **After every plan wave:** Run `cd frontend && npx vitest run`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 3-01-01 | 01 | 0 | DASH-01 | -- | N/A | unit | `npx vitest run src/stores/__tests__/farm.test.js` | no W0 | pending |
| 3-01-02 | 01 | 1 | DASH-02 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useKpi.test.js` | no W0 | pending |
| 3-01-03 | 01 | 1 | DASH-03 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useTrendData.test.js` | no W0 | pending |
| 3-01-04 | 01 | 1 | DASH-04 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useChartData.test.js` | no W0 | pending |
| 3-01-05 | 01 | 1 | DASH-05 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useChartData.test.js` | no W0 | pending |
| 3-02-01 | 02 | 1 | FILT-01 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useFilteredCows.test.js` | no W0 | pending |
| 3-02-02 | 02 | 1 | FILT-02 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useFilteredCows.test.js` | no W0 | pending |
| 3-02-03 | 02 | 1 | FILT-03 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useTrendData.test.js` | no W0 | pending |
| 3-03-01 | 03 | 2 | COW-01 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useCowTable.test.js` | no W0 | pending |
| 3-03-02 | 03 | 2 | COW-02 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useCowTable.test.js` | no W0 | pending |
| 3-03-03 | 03 | 2 | COW-03 | -- | N/A | unit | `npx vitest run src/utils/__tests__/alerts.test.js` | no W0 | pending |
| 3-03-04 | 03 | 2 | COW-04 | -- | N/A | unit | `npx vitest run src/composables/__tests__/useCowTable.test.js` | no W0 | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `npm install -D vitest @vue/test-utils jsdom` -- test framework installation
- [ ] `frontend/vitest.config.js` -- Vitest configuration
- [ ] `frontend/src/stores/__tests__/` -- store test directory + stubs
- [ ] `frontend/src/composables/__tests__/` -- composable test directory + stubs
- [ ] `frontend/src/utils/__tests__/` -- utility test directory + stubs

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ECharts renders correctly in browser | DASH-03, DASH-04, DASH-05 | Visual rendering cannot be automated without E2E framework | Open dashboard, verify chart axes, legends, and data points display correctly |
| Responsive layout on mobile viewport | All | Visual layout check | Open Chrome DevTools, toggle mobile viewport, verify usability |
| ParityChart isolation from parity filter | DASH-04 | Visual behavioral check | Select "頭產" in filter, verify ParityChart still shows all parities |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
