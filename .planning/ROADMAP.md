# Roadmap: DHI_Net

**Milestone:** v1 Launch
**Granularity:** Standard
**Coverage:** 36/36 requirements mapped

---

## Phases

- [ ] **Phase 1: 資料庫與驗證** - 建立資料庫模型、JWT 身份驗證與角色權限，所有後端基礎
- [ ] **Phase 2: 資料匯入流程** - PDF 上傳、配對驗證、自動轉檔、批次歷史資料匯入
- [ ] **Phase 3: 牧場儀表板與牛隻表格** - Vue 3 前端、KPI 卡片、趨勢圖表、動態篩選、牛隻列表
- [ ] **Phase 4: 跨牧場功能** - 跨農場總覽表、篩選組合儲存與還原
- [ ] **Phase 5: 報告匯出** - Excel 與 PDF 報告匯出，套用篩選狀態
- [ ] **Phase 6: 管理後台與部署** - 管理者面板、Docker Compose、PostgreSQL 搬遷

---

## Phase Details

### Phase 1: 資料庫與驗證
**Goal:** 建立資料庫層（SQLAlchemy + Alembic + SQLite）與 JWT 身份驗證系統，包含角色權限強制執行與管理者防鎖死機制，使所有後續功能有安全基礎可依賴
**Depends on:** —
**Requirements:** AUTH-01, AUTH-02, AUTH-03, AUTH-04, AUTH-05, AUTH-06, AUTH-07, AUTH-08, AUTH-09, AUTH-10, DEP-02, DEP-03
**Success Criteria** (what must be TRUE):
  1. 管理者可用帳號/密碼登入，並取得 JWT token；直接呼叫未授權農場的 API 端點回傳 403
  2. 顧問帳號可申請存取特定牧場，牧場帳號登入後可批准或拒絕申請
  3. 管理者初始化時產生的一次性恢復碼可在密碼遺失時重設管理者密碼，不會鎖死系統
  4. 切換 `DATABASE_URL` 環境變數可在 SQLite 與 PostgreSQL 之間無縫切換，Alembic 遷移腳本可在兩者上正常執行
**Plans:** TBD
**UI hint**: yes

### Phase 2: 資料匯入流程
**Goal:** 建立 PDF 上傳端點與 ConversionService，包含配對驗證、自動轉檔、匯入狀態追蹤，以及一次性批次歷史資料匯入工具
**Depends on:** Phase 1
**Requirements:** IMP-01, IMP-02, IMP-03, IMP-04, IMP-05
**Success Criteria** (what must be TRUE):
  1. 管理者或顧問拖曳上傳一對 PDF，系統在觸發轉檔前驗證農場代碼與日期前綴是否匹配；不匹配時回傳具體中文錯誤訊息，不觸發任何轉檔動作
  2. 配對驗證通過後，頁面顯示「轉檔中」狀態；成功後自動導向該農場月份頁面，失敗時顯示具體失敗原因
  3. 系統監控 `data/` 目錄，偵測到新增 PDF 後自動觸發配對驗證與轉檔流程
  4. 執行批次匯入工具後，`data/` 目錄下所有現有 xlsx 歷史資料完整寫入資料庫，儀表板可選取歷史月份
**Plans:** TBD

### Phase 3: 牧場儀表板與牛隻表格
**Goal:** 建立 Vue 3 + Vite 前端應用，包含側邊欄導覽、角色分流視圖、KPI 卡片、ECharts 趨勢圖表、多牧場篩選（含常用篩選儲存）、胎次/分群動態篩選、以及可排序搜尋的牛隻列表
**Depends on:** Phase 2
**Requirements:** DASH-01, DASH-02, DASH-03, DASH-04, DASH-05, FILT-01, FILT-02, FILT-03, COW-01, COW-02, COW-03, COW-04
**Success Criteria** (what must be TRUE):
  1. 頁面頂部常駐顯示當前農場與月份；切換農場或月份後，所有 KPI 卡片、趨勢圖表與牛隻列表同步更新，預設顯示最新月份
  2. KPI 卡片顯示當月平均乳量、平均 SCC、泌乳頭數、平均空胎天數，每張卡片附帶與上月的差值箭頭及色碼（上升/下降/持平）
  3. 切換胎次篩選（頭產/經產/全部）或分群篩選後，所有圖表、KPI 卡片與牛隻列表在一秒內同步更新，不觸發 API 請求
  4. 牛隻列表支援依任意欄位排序、依場內編號或統一編號搜尋，並以 A/B/C/D/E 色碼標籤顯示警示碼，每頁 50 筆分頁
**Plans:** 5 plans
Plans:
- [ ] 03-01-PLAN.md — SideNav + AppShell + router restructure + role switching
- [ ] 03-02-PLAN.md — overviewFilter store + saved presets (localStorage)
- [ ] 03-03-PLAN.md — TrendComparisonView + ComparisonView (new chart views)
- [ ] 03-04-PLAN.md — CowTableView + AlertsView (dedicated routes)
- [ ] 03-05-PLAN.md — OverviewView filter integration + visual verification
**UI hint**: yes

### Phase 4: 跨牧場功能
**Goal:** 為管理者與顧問提供跨牧場總覽表，支援農場勾選篩選、常用組合儲存，以及登入後自動還原上次選定組合
**Depends on:** Phase 3
**Requirements:** DASH-06, DASH-07, DASH-08, DASH-09, DASH-10
**Success Criteria** (what must be TRUE):
  1. 管理者與顧問登入後可看到跨牧場總覽表，每列一個農場，欄位顯示當月核心指標與 MoM 箭頭；牧場帳號無法存取此頁面
  2. 顧問可勾選/取消勾選要同時顯示的農場，並將當前組合命名後儲存為常用組合
  3. 顧問下次登入後，自動還原上次選定的組合；若當前組合未命名儲存，系統自動存為臨時組合供下次讀取
**Plans:** TBD
**UI hint**: yes

### Phase 5: 報告匯出
**Goal:** 提供 Excel 與 PDF 報告匯出功能，匯出內容對應 DHI整理.xlsx 工作表結構，並套用當前篩選條件與條件格式
**Depends on:** Phase 4
**Requirements:** EXP-01, EXP-02, EXP-03
**Success Criteria** (what must be TRUE):
  1. 點擊匯出 Excel 後，下載的 .xlsx 包含 1-總表、2-乳品質、3-月比較、4-牛群資料表四個工作表，高 SCC 欄位以紅色條件格式標示，警示碼欄位以黃色標示
  2. 匯出的 Excel 與 PDF 內容反映當前篩選狀態（農場、月份、胎次篩選、分群篩選、時間範圍），而非完整資料
  3. 匯出的 PDF 為 A4 可列印格式，包含 KPI 摘要、圖表嵌入圖片、牛隻資料表，頁尾顯示顧問名稱與產製日期
**Plans:** TBD
**UI hint**: yes

### Phase 6: 管理後台與部署
**Goal:** 建立管理者後台（帳號/牧場管理、配額監控、轉檔記錄），完成 Docker Compose 設定（開發用 SQLite + 正式用 PostgreSQL），並驗證 Alembic 遷移可在 PostgreSQL 上正常執行
**Depends on:** Phase 5
**Requirements:** ADM-01, ADM-02, ADM-03, ADM-04, ADM-05, ADM-06, DEP-01
**Success Criteria** (what must be TRUE):
  1. 管理者後台可新增/停用帳號、指派角色與訂閱配額，並在聯表中查看所有顧問的配額使用量；審核顧問存取申請與批次授權操作需輸入密碼確認
  2. 管理者可在後台查看所有 PDF 上傳與轉檔記錄，欄位包含上傳者、時間、農場月份、成功/失敗狀態
  3. 執行 `docker compose up` 可在 WSL 環境啟動後端服務（使用 SQLite）；切換 `DATABASE_URL` 至 PostgreSQL 並執行 Alembic migrate 後，系統正常運作且資料完整
**Plans:** TBD
**UI hint**: yes

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. 資料庫與驗證 | 0/? | Not started | - |
| 2. 資料匯入流程 | 0/? | Not started | - |
| 3. 牧場儀表板與牛隻表格 | 0/5 | Planned | - |
| 4. 跨牧場功能 | 0/? | Not started | - |
| 5. 報告匯出 | 0/? | Not started | - |
| 6. 管理後台與部署 | 0/? | Not started | - |
