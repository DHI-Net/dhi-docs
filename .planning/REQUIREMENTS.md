# Requirements: DHI_Net

**Defined:** 2026-04-23
**Core Value:** 顧問能在現場即時篩選、比較多個牧場的牛群指標，並一鍵匯出報告，取代手動整理 Excel 的流程。

---

## v1 Requirements

### Authentication & Permissions (AUTH)

- [ ] **AUTH-01**: 管理者可建立顧問帳號與牧場帳號，並指派訂閱方案
- [ ] **AUTH-02**: 使用者可以帳號/密碼登入（JWT access token + httpOnly refresh token）
- [ ] **AUTH-03**: 角色權限在 API 層強制執行（顧問不得存取未授權牧場，僅前端 UI 限制不算）
- [ ] **AUTH-04**: 管理者設定帳號時產生一次性恢復碼，防止管理者密碼遺失鎖死系統
- [ ] **AUTH-05**: 顧問帳號有可存取牧場數量配額，依訂閱方案自動設定，管理者後台可調整
- [ ] **AUTH-06**: 顧問可向系統提出申請，要求存取特定牧場資料
- [ ] **AUTH-07**: 牧場帳號可登入後批准或拒絕顧問的存取申請
- [ ] **AUTH-08**: 管理者可代替牧場授權顧問存取牧場（需輸入密碼確認），支援批次授權（一牧場對多顧問 / 一顧問對多牧場）
- [ ] **AUTH-09**: 顧問可在帳號設定頁查看目前配額使用量 / 總配額，並點擊展開已授權牧場清單
- [ ] **AUTH-10**: 牧場帳號登入後可查看自己牧場的儀表板（功能與顧問相同，但僅限單一牧場）

### Data Import (IMP)

- [ ] **IMP-01**: 管理者或顧問可透過網頁拖曳上傳 PDF 一對（性能檢定 + 牛乳品質）
- [ ] **IMP-02**: 系統在觸發轉檔前驗證 PDF 配對（相同農場、相同月份）；配對不符則回傳具體錯誤訊息
- [ ] **IMP-03**: 系統自動監控 `data/` 目錄，偵測新增 PDF 檔案並觸發轉檔流程
- [ ] **IMP-04**: 上傳後顯示轉檔狀態（進行中 / 成功 / 失敗原因）；轉檔完成後自動導向該農場月份頁面
- [ ] **IMP-05**: 一次性批次匯入工具：掃描 `data/` 目錄中現有的 xlsx 歷史資料並寫入資料庫

### Farm Dashboard — Charts & KPI (DASH)

- [ ] **DASH-01**: 儀表板頂部常駐顯示當前農場 + 月份；提供農場切換選單與月份選取器（預設最新月份）
- [ ] **DASH-02**: KPI 卡片顯示當月核心指標（平均乳量、平均 SCC、泌乳頭數、平均空胎天數）及與上月的差值箭頭（MoM delta，色碼顯示）
- [ ] **DASH-03**: 12 個月趨勢折線圖（乳量、SCC、泌乳頭數各一條）
- [ ] **DASH-04**: 胎次分布長條圖（頭產 / 二胎 / 三胎以上）
- [ ] **DASH-05**: SCC 區間分布圖（<5、5–20、20–50、>50 萬/mL 各區間頭數）
- [ ] **DASH-06**: 跨牧場總覽表（僅管理者與顧問可見），每列一個農場，欄位為當月核心指標 + MoM 箭頭
- [ ] **DASH-07**: 跨牧場總覽：可篩選要同時顯示的農場（勾選/取消）
- [ ] **DASH-08**: 跨牧場總覽：顧問可儲存常用農場比較組合（命名後存入帳號）
- [ ] **DASH-09**: 跨牧場總覽：系統記憶顧問上次選定的組合，下次登入自動還原
- [ ] **DASH-10**: 跨牧場總覽：若當前選定組合非已儲存常用組合，自動存為臨時組合供下次讀取

### Dynamic Filtering (FILT)

- [ ] **FILT-01**: 胎次篩選（全部 / 頭產 / 經產），同時套用至所有圖表、KPI 卡片、牛隻表格與匯出
- [ ] **FILT-02**: 分群篩選（依農場分群名稱），同時套用至所有圖表與牛隻表格
- [ ] **FILT-03**: 時間範圍篩選（3 / 6 / 12 個月快速選項 + 自訂範圍），套用至趨勢圖表

### Individual Cow Table (COW)

- [ ] **COW-01**: 牛隻列表支援所有欄位排序（點擊欄位標題排序）
- [ ] **COW-02**: 可依場內編號或統一編號搜尋特定牛隻
- [ ] **COW-03**: 警示碼顯示（A/B/C/D/E 各碼用色碼標籤顯示於每列）
- [ ] **COW-04**: 分頁顯示（每頁 50 筆）

### Report Export (EXP)

- [ ] **EXP-01**: Excel 匯出（.xlsx），工作表結構對應 DHI整理.xlsx（1-總表、3-月比較、4-牛群資料表、2-乳品質），含條件格式（高 SCC 紅色、警示碼黃色）
- [ ] **EXP-02**: Excel 匯出套用當前篩選條件（胎次、分群、時間範圍）
- [ ] **EXP-03**: PDF 報告匯出（A4 可列印格式，包含 KPI 摘要、圖表嵌入圖片、牛隻資料表），含顧問名稱與產製日期頁尾

### Admin Panel (ADM)

- [ ] **ADM-01**: 管理者可新增、停用帳號，指派角色（顧問 / 牧場）與訂閱方案（含配額上限）
- [ ] **ADM-02**: 管理者後台顯示所有顧問帳號的配額監控聯表（使用量 / 總額度）
- [ ] **ADM-03**: 管理者可新增、編輯、刪除牧場（專案編號、名稱）
- [ ] **ADM-04**: 管理者可查看顧問存取申請佇列，並審核（批准/拒絕）
- [ ] **ADM-05**: 管理者可代替牧場批次授權顧問存取（需輸入密碼，支援一對多/多對一）
- [ ] **ADM-06**: 管理者可查看所有 PDF 上傳與轉檔記錄（上傳者、時間、農場月份、成功/失敗）

### Deployment (DEP)

- [ ] **DEP-01**: 提供 Docker Compose 設定（backend + frontend + PostgreSQL），支援 WSL → 正式主機搬遷
- [ ] **DEP-02**: 資料庫透過 `DATABASE_URL` 環境變數切換 SQLite（開發）/ PostgreSQL（正式），程式碼無需修改
- [ ] **DEP-03**: Alembic 資料庫遷移腳本從第一個 Phase 起建置，確保 SQLite → PostgreSQL 遷移可驗證

---

## v2 Requirements

### Advanced Admin
- **ADM-V2-01**: 高級管理者 vs 一般管理者角色區分（v1 管理者為單一角色）
- **ADM-V2-02**: 訂閱方案自動計費整合

### Analytics
- **COW-V2-01**: 個別牛隻 9 個月泌乳曲線（需跨月份 national_id 串聯）
- **DASH-V2-01**: 跨牧場趨勢折線疊加比較（多農場乳量曲線同圖）
- **DASH-V2-02**: 與區域基準對比（需外部參考資料）

### AI Integration
- **LLM-V2-01**: LLM + RAG 自然語言查詢（「這個月哪頭牛 SCC 最高？」）
- **LLM-V2-02**: AI 輔助報告文字生成

---

## Out of Scope

| Feature | Reason |
|---------|--------|
| 行動 App（iOS/Android）| Web RWD 優先；App 為未來版本 |
| 即時通知 / WebSocket | 月資料無即時需求 |
| 多語言（i18n）| 此版本繁體中文為唯一語言 |
| 飼養建議 / 營養分析 | 超出 DHI 數據範疇；顧問自行解讀 |
| 個別牛隻治療紀錄 | 屬於場內管理系統功能，不在 DHI 資料中 |
| 系統使用記錄 / Audit log | 只記錄上傳事件，不記錄每次查看 |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 1 | Pending |
| AUTH-02 | Phase 1 | Pending |
| AUTH-03 | Phase 1 | Pending |
| AUTH-04 | Phase 1 | Pending |
| AUTH-05 | Phase 1 | Pending |
| AUTH-06 | Phase 1 | Pending |
| AUTH-07 | Phase 1 | Pending |
| AUTH-08 | Phase 1 | Pending |
| AUTH-09 | Phase 1 | Pending |
| AUTH-10 | Phase 1 | Pending |
| DEP-02 | Phase 1 | Pending |
| DEP-03 | Phase 1 | Pending |
| IMP-01 | Phase 2 | Pending |
| IMP-02 | Phase 2 | Pending |
| IMP-03 | Phase 2 | Pending |
| IMP-04 | Phase 2 | Pending |
| IMP-05 | Phase 2 | Pending |
| DASH-01 | Phase 3 | Pending |
| DASH-02 | Phase 3 | Pending |
| DASH-03 | Phase 3 | Pending |
| DASH-04 | Phase 3 | Pending |
| DASH-05 | Phase 3 | Pending |
| FILT-01 | Phase 3 | Pending |
| FILT-02 | Phase 3 | Pending |
| FILT-03 | Phase 3 | Pending |
| COW-01 | Phase 3 | Pending |
| COW-02 | Phase 3 | Pending |
| COW-03 | Phase 3 | Pending |
| COW-04 | Phase 3 | Pending |
| DASH-06 | Phase 4 | Pending |
| DASH-07 | Phase 4 | Pending |
| DASH-08 | Phase 4 | Pending |
| DASH-09 | Phase 4 | Pending |
| DASH-10 | Phase 4 | Pending |
| EXP-01 | Phase 5 | Pending |
| EXP-02 | Phase 5 | Pending |
| EXP-03 | Phase 5 | Pending |
| ADM-01 | Phase 6 | Pending |
| ADM-02 | Phase 6 | Pending |
| ADM-03 | Phase 6 | Pending |
| ADM-04 | Phase 6 | Pending |
| ADM-05 | Phase 6 | Pending |
| ADM-06 | Phase 6 | Pending |
| DEP-01 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 44 total (AUTH×10 + IMP×5 + DASH×10 + FILT×3 + COW×4 + EXP×3 + ADM×6 + DEP×3)
- Mapped to phases: 44
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-23*
*Last updated: 2026-04-22 after roadmap creation*
