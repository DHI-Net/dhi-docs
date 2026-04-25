# Project State

## Current Phase
Phase 1 — Not started

## Project Reference
See: .planning/PROJECT.md

**Core value:** 顧問能在現場即時篩選、比較多個牧場的牛群指標，並一鍵匯出報告
**Current focus:** Phase 1

## Phase Summary

| Phase | Name | Status |
|-------|------|--------|
| 1 | 資料庫與驗證 | Not started |
| 2 | 資料匯入流程 | Not started |
| 3 | 牧場儀表板與牛隻表格 | Not started |
| 4 | 跨牧場功能 | Not started |
| 5 | 報告匯出 | Not started |
| 6 | 管理後台與部署 | Not started |

## Performance Metrics

- Phases complete: 0/6
- Plans complete: 0/?
- Requirements delivered: 0/36

## Accumulated Context

### Key Decisions
- JWT: access token in memory + refresh token in httpOnly cookie（無狀態，Docker 相容）
- SQLAlchemy 2.x async + Alembic 從 Phase 1 起建置，確保 SQLite→PostgreSQL 遷移可驗證
- Pinia 作為篩選狀態唯一來源，避免圖表/表格/匯出不同步
- PDF 轉檔服務呼叫底層函式而非 `main()`，避免 tkinter GUI 觸發
- 牛隻資料以月份一次全量載入後在客戶端篩選（30-150 頭），避免 API race condition

### Blockers
- 無

### Todos
- 確認 `performance_pdf_to_xlsx.py` 是否有可直接呼叫的函式（非 `main()`）
- 確認顏御哲農場是否有固定案件編號（上傳驗證依賴一致的檔名後綴格式）
- Phase 3 開始前與顧問確認 Excel 匯出工作表結構是否符合實際需求

## Session Log
- 2026-04-22: Project initialized, roadmap created (6 phases, 36 v1 requirements)
