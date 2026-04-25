# DHI_Net

## What This Is

DHI_Net 是一個供酪農業顧問使用的 DHI 月報表網頁系統。顧問（飼養管理顧問、獸醫、乳品廠指導員、飼料廠業務）可同時管理多個牧場的每月 DHI 資料，用於現場與酪農討論牛群現況，並產製客製化報告。酪農戶為次要使用者，僅能查閱自身牧場資料。

## Core Value

顧問能在現場即時篩選、比較多個牧場的牛群指標，並一鍵匯出報告，取代手動整理 Excel 的流程。

## Requirements

### Validated

- ✓ PDF 轉檔：牛乳品質 PDF → xlsx (`src/milk_pdf_to_xlsx.py`) — existing
- ✓ PDF 轉檔：性能檢定 PDF → xlsx (`src/performance_pdf_to_xlsx.py`) — existing
- ✓ FastAPI 後端雛型（xlsx 讀取 + REST API）— existing
- ✓ Vue 3 + ECharts 前端儀表板雛型（單頁 HTML）— existing
- ✓ 三個農場歷史資料（吳龍廷 94、林家和 06、顏御哲）— existing

### Active

- [ ] 使用者驗證與角色管理（管理者、顧問、酪農戶）
- [ ] 資料庫層（SQLite 開發 / PostgreSQL 生產）
- [ ] PDF 上傳介面 + 自動觸發轉檔流程
- [ ] 自動偵測 data/ 目錄新增 PDF 並觸發轉檔（可選）
- [ ] 多牧場顧問儀表板（牛群指標跨農場總覽）
- [ ] 牛群指標圖表（乳量趨勢、體細胞數、泌乳頭數、胎次分布、平均泌乳天數、空胎天數、配種次數）
- [ ] 月份比較（本月 vs 上月）
- [ ] 動態篩選（時間範圍、胎次、分群）
- [ ] 個別牛隻查詢（次要功能，可搜尋/排序）
- [ ] 報告匯出（Excel — 含篩選條件；PDF — 可列印）
- [ ] RWD 前端（筆電 + 平板）
- [ ] 前端改用 Vue 3 + Vite 建置（取代現有 CDN 雛型）
- [ ] 管理者後台（牧場管理、使用者管理、密碼保護 + 防呆機制）
- [ ] Docker Compose 部署（WSL 開發 → 正式主機搬遷）

### Out of Scope

- LLM + RAG 自然語言查詢 — 架構需留相容性介面，但此版本不實作
- 行動 App（iOS/Android）— Web RWD 優先，App 為未來版本
- 即時通知 / WebSocket — 月資料無即時需求
- 多語言（i18n）— 此版本繁體中文為唯一語言

## Context

- 現有雛型已能讀取 xlsx 並透過 API 提供資料，前端可顯示基本圖表
- 資料來源為兩份 PDF（性能檢定 + 牛乳品質），需成對才能合法轉檔；配對失敗只取消該月份，不影響其他月份
- `src/milk_pdf_to_xlsx.py` 固定不得修改轉檔邏輯
- 目前三個農場：吳龍廷（94）、林家和（06）、顏御哲
- 顧問的使用情境分兩種：現場動態展示（RWD 互動）、事後報告製作（匯出）
- 未來計畫引入 LLM+RAG，API 設計需為自然語言查詢留下擴充點

## Constraints

- **Tech — 轉檔程式**：`src/milk_pdf_to_xlsx.py` 固定，不得修改；性能檢定轉檔參考 `原始資料彙整(全)` 使用方式
- **Tech — 禁止 LLM**：轉檔或資料分析不得使用 LLM
- **Tech — 後端語言**：Python FastAPI（與轉檔腳本同語言，方便整合）
- **Tech — 資料庫**：SQLite（開發）→ PostgreSQL（正式），需無痛搬遷
- **Tech — 前端**：Vue 3 + Vite + ECharts（升級自現有雛型）
- **Security — 管理功能**：重要操作需唯一密碼保護 + 防呆機制（避免忘記密碼導致鎖死）
- **Deployment**：WSL 開發，Docker Compose 供正式搬遷使用

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Vue 3 + Vite 前端 | 升級自 CDN 雛型，獲得 hot-reload、打包最佳化、更好的狀態管理 | — Pending |
| ECharts 圖表庫 | 現有雛型已使用，繼續沿用避免重寫 | — Pending |
| SQLAlchemy ORM | 支援 SQLite/PostgreSQL 無痛切換 | — Pending |
| API-first 架構 | 前後端分離，同時為未來 LLM 整合留擴充點 | — Pending |
| JWT 驗證 | 無狀態 token，方便 Docker 水平擴展 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-22 after initialization*
