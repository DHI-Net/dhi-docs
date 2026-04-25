# dhi-docs

專案規劃文件管理。這個 repo 只有文件，沒有執行程式碼。

## 這個 Repo 的內容

```
dhi-docs/
├── .planning/
│   ├── PROJECT.md        # 專案定義、核心價值、使用場景
│   ├── REQUIREMENTS.md   # 44 項需求（AUTH/IMP/DASH/FILT/COW/EXP/ADM/DEP）
│   ├── ROADMAP.md        # 6 Phase 路線圖
│   ├── STATE.md          # GSD 工作流程狀態
│   ├── codebase/         # 現有程式碼分析（由 /gsd-map-codebase 產生）
│   ├── research/         # 技術研究（由 /gsd-research-phase 產生）
│   └── phases/           # 各 phase 的 PLAN、UI-SPEC、VALIDATION
├── CLAUDE.md
├── DESIGN.md             # UI/UX 設計決策
├── DEMO.md               # Demo 部署說明
└── draw_arch.py          # 架構圖產生腳本（matplotlib）
```

## 6 Phase 路線圖

| Phase | 名稱 | 負責 Repo |
|-------|------|-----------|
| 1 | 資料庫與驗證 | dhi-backend |
| 2 | 資料匯入流程 | dhi-backend |
| 3 | 牧場儀表板 | dhi-frontend ✅ |
| 4 | 跨牧場功能 | dhi-frontend |
| 5 | 報告匯出 | dhi-backend + dhi-frontend |
| 6 | 管理後台 + 部署 | dhi-backend |

## 使用者角色

- **顧問**：主要使用者，同時管理多個牧場，現場討論 + 事後報告
- **酪農戶**：次要，只看自己牧場
- **管理者**：系統管理，重要操作需密碼 + 防呆

## 農場資料

| 農場 | 案件編號 |
|------|---------|
| 吳龍廷 | 94 |
| 林家和 | 06 |
| 顏御哲 | — |

## DHI 核心欄位

| 欄位 | 正常範圍 | 重要度 |
|------|---------|--------|
| 乳量 (kg) | 依牛而定 | ★★★ |
| 體細胞數 (萬/mL) | <20 | ★★★ |
| 尿素氮 (mg/dL) | 11–17 | ★★ |
| 檸檬酸 (mg/dL) | 119–190 | ★★ |
| P/F | 0.85–0.88 | ★★ |
| 游離脂肪酸 (mmol) | <1.5 | ★★ |
| 空胎日數 | <120 佳 | ★★ |

## 注意事項代碼

| 代碼 | 含義 |
|------|------|
| (A) | 高乳脂 |
| (B) | 高體細胞數（乳房炎風險） |
| (C) | 低乳量 |
| (D) | 低泌乳天數（剛分娩） |
| (E) | 高游離脂肪酸（能量負平衡） |

## 文件工作規則

- 只更新文件，不寫程式碼
- Phase 計畫（PLAN.md）異動需同步更新 ROADMAP.md
- UI 設計決策記錄在 `phases/0X-*/0X-UI-SPEC.md` 和 `DESIGN.md`
- 程式碼相關的架構說明放 `codebase/ARCHITECTURE.md`

## 相關 Repo

| Repo | 說明 |
|------|------|
| dhi-backend | API、轉檔、資料庫 |
| dhi-frontend | Vue 3 前端儀表板 |
