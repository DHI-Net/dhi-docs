"""
DHI Net 架構圖產生器
用 matplotlib 繪製系統架構圖，輸出 PNG。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ── 中文字體設定 ────────────────────────────────────
from matplotlib import font_manager
_font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_manager.fontManager.addfont(_font_path)
_fp = font_manager.FontProperties(fname=_font_path)
plt.rcParams["font.family"] = _fp.get_name()
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(18, 13))
ax.set_xlim(0, 18)
ax.set_ylim(0, 13)
ax.axis("off")
fig.patch.set_facecolor("#F0F4F8")
ax.set_facecolor("#F0F4F8")

# ── 顏色定義 ────────────────────────────────────
C_DATA   = "#4A90D9"   # 資料層 - 藍
C_SRC    = "#E8873A"   # 轉檔層 - 橘
C_BE     = "#5BAD72"   # 後端   - 綠
C_FE     = "#9B59B6"   # 前端   - 紫
C_USER   = "#E74C3C"   # 使用者 - 紅
C_TODO   = "#BDC3C7"   # 待完成 - 灰
C_ARROW  = "#555555"
C_TODO_ARROW = "#AAAAAA"

TITLE_FS = 9.5
LABEL_FS = 8.5
SMALL_FS = 7.5
TINY_FS  = 6.8


def box(ax, x, y, w, h, color, alpha=1.0, radius=0.25, lw=1.5, ls="-"):
    fancy = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw,
        edgecolor=color,
        facecolor=(*matplotlib.colors.to_rgb(color), alpha),
        linestyle=ls,
        zorder=2,
    )
    ax.add_patch(fancy)


def label(ax, x, y, text, fs=LABEL_FS, color="white", bold=False, ha="center", va="center", wrap=False):
    weight = "bold" if bold else "normal"
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va,
            fontweight=weight, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=C_ARROW, lw=1.5, style="->", ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, connectionstyle="arc3,rad=0"),
                zorder=4)


def dashed_arrow(ax, x1, y1, x2, y2, color=C_TODO_ARROW, lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw,
                                linestyle="dashed", connectionstyle="arc3,rad=0"),
                zorder=4)


# ════════════════════════════════════════════════════════
# 標題
# ════════════════════════════════════════════════════════
ax.text(9, 12.55, "DHI Net — 現行系統架構（Demo Prototype）",
        fontsize=14, ha="center", va="center", fontweight="bold", color="#2C3E50")

# ════════════════════════════════════════════════════════
# 圖例
# ════════════════════════════════════════════════════════
legend_items = [
    (C_DATA, "資料 / 檔案"),
    (C_SRC,  "轉檔腳本"),
    (C_BE,   "後端 FastAPI"),
    (C_FE,   "前端 Vue"),
    (C_USER, "使用者"),
    (C_TODO, "待實作"),
]
lx = 0.3
for i, (col, txt) in enumerate(legend_items):
    bx = lx + i * 2.85
    box(ax, bx, 12.0, 0.35, 0.35, col, alpha=0.85, radius=0.08, lw=1.2)
    ax.text(bx + 0.5, 12.18, txt, fontsize=TINY_FS, color="#333", va="center")


# ════════════════════════════════════════════════════════
# Row 1 (y=9.8~11.6)：資料來源
# ════════════════════════════════════════════════════════
ax.text(9, 11.55, "── 原始資料層 ──",
        fontsize=SMALL_FS, ha="center", color="#555", style="italic")

# PDF 群組
pdf_farms = [
    ("吳龍廷 (94)\n2024.11–2026.03", 0.4),
    ("林家和 (06)\n2024.07–2026.04", 3.3),
    ("顏御哲\n2025.04–2026.03", 6.2),
]
for txt, bx in pdf_farms:
    box(ax, bx, 9.9, 2.6, 1.45, C_DATA, alpha=0.75, radius=0.2)
    label(ax, bx+1.3, 10.62, txt, fs=SMALL_FS)

# 性能檢定 PDF 標籤
for bx in [0.4, 3.3, 6.2]:
    ax.text(bx+0.08, 10.95, "性能檢定 PDF", fontsize=TINY_FS, color="#ddeeff", va="center")
    ax.text(bx+0.08, 10.60, "牛乳品質 PDF", fontsize=TINY_FS, color="#ddeeff", va="center")
    ax.text(bx+0.08, 10.25, "DHI整理.xlsx  ← 手動", fontsize=TINY_FS, color="#ffe599", va="center")

# 未知農場 raw box（右側）
box(ax, 9.3, 9.9, 2.6, 1.45, C_DATA, alpha=0.35, radius=0.2, lw=1.2, ls="--")
label(ax, 10.6, 10.62, "吳炎珍（未知）\n20260108_DHI.xlsx", fs=SMALL_FS, color="#888")

# data/ 總目錄標籤
ax.text(0.35, 9.75, "📁 data/   （3 農場 × 多月份 Excel + PDF）",
        fontsize=SMALL_FS, color="#2C3E50")


# ════════════════════════════════════════════════════════
# Row 2 (y=7.7~9.5)：轉檔腳本
# ════════════════════════════════════════════════════════
ax.text(9, 9.4, "── 轉檔腳本層 (src/) ──",
        fontsize=SMALL_FS, ha="center", color="#555", style="italic")

# milk_pdf_to_xlsx
box(ax, 0.4, 7.8, 3.8, 1.3, C_SRC, alpha=0.82, radius=0.2)
label(ax, 2.3, 8.58, "milk_pdf_to_xlsx.py", fs=LABEL_FS, bold=True)
label(ax, 2.3, 8.22, "牛乳品質 PDF → xlsx", fs=SMALL_FS)
label(ax, 2.3, 7.95, "（既有，不得修改）", fs=TINY_FS, color="#ffe09f")

# performance_pdf_to_xlsx
box(ax, 4.6, 7.8, 3.8, 1.3, C_SRC, alpha=0.82, radius=0.2)
label(ax, 6.5, 8.58, "performance_pdf_to_xlsx.py", fs=LABEL_FS, bold=True)
label(ax, 6.5, 8.22, "性能檢定 PDF → xlsx", fs=SMALL_FS)
label(ax, 6.5, 7.95, "（新開發完成）", fs=TINY_FS, color="#ffe09f")

# 待完成：上傳 pipeline
box(ax, 8.8, 7.8, 4.2, 1.3, C_TODO, alpha=0.35, radius=0.2, lw=1.2, ls="--")
label(ax, 10.9, 8.58, "上傳 Pipeline（待做）", fs=LABEL_FS, bold=True, color="#666")
label(ax, 10.9, 8.22, "PDF 上傳 → 配對 → 轉檔 → 入庫", fs=SMALL_FS, color="#888")
label(ax, 10.9, 7.95, "命名規則配對、錯誤防呆", fs=TINY_FS, color="#aaa")

# 箭頭：PDF → 轉檔腳本
for bx in [0.4, 3.3, 6.2]:
    arrow(ax, bx+1.3, 9.9, bx+1.3, 9.1, C_ARROW, lw=1.2)

# 箭頭：轉檔腳本 → extractor
arrow(ax, 2.3, 7.8, 5.5, 6.65, C_ARROW, lw=1.2)
arrow(ax, 6.5, 7.8, 6.5, 6.65, C_ARROW, lw=1.2)


# ════════════════════════════════════════════════════════
# Row 3 (y=5.2~7.4)：後端
# ════════════════════════════════════════════════════════
ax.text(9, 7.35, "── 後端 (backend/) ──",
        fontsize=SMALL_FS, ha="center", color="#555", style="italic")

# extractor.py
box(ax, 0.4, 5.3, 3.5, 1.75, C_BE, alpha=0.80, radius=0.2)
label(ax, 2.15, 6.92, "extractor.py", fs=LABEL_FS, bold=True)
label(ax, 2.15, 6.58, "load_all_data()", fs=SMALL_FS)
label(ax, 2.15, 6.28, "extract_summary()  ← 3-月比較", fs=TINY_FS)
label(ax, 2.15, 6.02, "extract_cows()  ← 原始資料彙整(全)", fs=TINY_FS)
label(ax, 2.15, 5.72, "extract_measurement_date()  ← 1-總表", fs=TINY_FS)
label(ax, 2.15, 5.45, "啟動時快取至記憶體", fs=TINY_FS, color="#d0ffd0")

# main.py
box(ax, 4.3, 5.3, 3.5, 1.75, C_BE, alpha=0.80, radius=0.2)
label(ax, 6.05, 6.92, "main.py (FastAPI)", fs=LABEL_FS, bold=True)
label(ax, 6.05, 6.58, "GET /api/data", fs=SMALL_FS)
label(ax, 6.05, 6.28, "GET /api/farms", fs=SMALL_FS)
label(ax, 6.05, 5.98, "GET /api/farms/{farm}/months", fs=SMALL_FS)
label(ax, 6.05, 5.68, "GET /api/farms/{farm}/{month}", fs=SMALL_FS)
label(ax, 6.05, 5.40, "CORS 全開 / Static 掛載", fs=TINY_FS, color="#d0ffd0")

# 待做：資料庫
box(ax, 8.2, 5.3, 3.4, 1.75, C_TODO, alpha=0.35, radius=0.2, lw=1.2, ls="--")
label(ax, 9.9, 6.92, "資料庫（待做）", fs=LABEL_FS, bold=True, color="#666")
label(ax, 9.9, 6.55, "SQLite → PostgreSQL", fs=SMALL_FS, color="#888")
label(ax, 9.9, 6.25, "SQLAlchemy models", fs=SMALL_FS, color="#888")
label(ax, 9.9, 5.95, "農場 / 月份 / 牛隻 table", fs=SMALL_FS, color="#888")
label(ax, 9.9, 5.65, "歷史資料批次匯入", fs=SMALL_FS, color="#888")

# 待做：認證
box(ax, 11.9, 5.3, 3.4, 1.75, C_TODO, alpha=0.35, radius=0.2, lw=1.2, ls="--")
label(ax, 13.6, 6.92, "認證系統（待做）", fs=LABEL_FS, bold=True, color="#666")
label(ax, 13.6, 6.55, "JWT / Session", fs=SMALL_FS, color="#888")
label(ax, 13.6, 6.25, "酪農 / 顧問 / 管理者", fs=SMALL_FS, color="#888")
label(ax, 13.6, 5.95, "管理功能密碼保護", fs=SMALL_FS, color="#888")
label(ax, 13.6, 5.65, "防呆機制", fs=SMALL_FS, color="#888")

# 箭頭：extractor → main
arrow(ax, 3.9, 6.18, 4.3, 6.18, C_ARROW, lw=1.5)


# ════════════════════════════════════════════════════════
# Row 4 (y=2.8~5.0)：前端
# ════════════════════════════════════════════════════════
ax.text(9, 5.15, "── 前端 (frontend/) ──",
        fontsize=SMALL_FS, ha="center", color="#555", style="italic")

# index.html
box(ax, 0.4, 2.9, 5.0, 1.9, C_FE, alpha=0.80, radius=0.2)
label(ax, 2.9, 4.57, "index.html  (847 行)", fs=LABEL_FS, bold=True)
label(ax, 2.9, 4.22, "Vue 3 (CDN)  +  ECharts 5  +  Tailwind CSS", fs=SMALL_FS)
label(ax, 2.9, 3.92, "農場選擇器  /  月份切換  /  摘要卡片", fs=TINY_FS)
label(ax, 2.9, 3.67, "月比較圖 (乳量/SCC/尿素氮…)", fs=TINY_FS)
label(ax, 2.9, 3.42, "逐頭牛資料表  /  注意事項標籤", fs=TINY_FS)
label(ax, 2.9, 3.15, "靜態資料 window.__DHI_DATA__ 嵌入", fs=TINY_FS, color="#e8d0ff")
label(ax, 2.9, 2.92, "（可離線預覽，無需後端）", fs=TINY_FS, color="#e8d0ff")

# data.js
box(ax, 5.8, 2.9, 2.5, 1.9, C_FE, alpha=0.55, radius=0.2)
label(ax, 7.05, 4.57, "data.js", fs=LABEL_FS, bold=True)
label(ax, 7.05, 4.22, "靜態 JSON 資料", fs=SMALL_FS)
label(ax, 7.05, 3.92, "（與 index.html", fs=TINY_FS)
label(ax, 7.05, 3.67, " 同步嵌入）", fs=TINY_FS)
label(ax, 7.05, 3.32, "3 農場 × 3 月", fs=TINY_FS)
label(ax, 7.05, 3.07, "最近資料", fs=TINY_FS)

# 待做：Vite 建置
box(ax, 8.6, 2.9, 3.2, 1.9, C_TODO, alpha=0.35, radius=0.2, lw=1.2, ls="--")
label(ax, 10.2, 4.57, "Vite 建置（待做）", fs=LABEL_FS, bold=True, color="#666")
label(ax, 10.2, 4.22, "Vue 3 + Vite 正式架構", fs=SMALL_FS, color="#888")
label(ax, 10.2, 3.87, "Component 拆分", fs=SMALL_FS, color="#888")
label(ax, 10.2, 3.57, "Router / Store", fs=SMALL_FS, color="#888")
label(ax, 10.2, 3.27, "API 串接（替換靜態資料）", fs=SMALL_FS, color="#888")
label(ax, 10.2, 2.97, "角色權限頁面", fs=SMALL_FS, color="#888")

# 待做：Docker
box(ax, 12.1, 2.9, 3.2, 1.9, C_TODO, alpha=0.35, radius=0.2, lw=1.2, ls="--")
label(ax, 13.7, 4.57, "Docker（待做）", fs=LABEL_FS, bold=True, color="#666")
label(ax, 13.7, 4.22, "docker-compose.yml", fs=SMALL_FS, color="#888")
label(ax, 13.7, 3.87, "backend container", fs=SMALL_FS, color="#888")
label(ax, 13.7, 3.57, "frontend (nginx)", fs=SMALL_FS, color="#888")
label(ax, 13.7, 3.27, "PostgreSQL container", fs=SMALL_FS, color="#888")
label(ax, 13.7, 2.97, "WSL → 新主機搬遷", fs=SMALL_FS, color="#888")

# 箭頭：main.py → index.html（API）
arrow(ax, 6.05, 5.3, 6.05, 4.8, C_ARROW, lw=1.5)
ax.text(6.2, 5.05, "JSON API", fontsize=TINY_FS, color=C_ARROW, va="center")

# 箭頭：data.js → index.html
arrow(ax, 5.8, 3.85, 5.4, 3.85, C_FE, lw=1.2)


# ════════════════════════════════════════════════════════
# Row 5 (y=0.5~2.5)：使用者
# ════════════════════════════════════════════════════════
ax.text(9, 2.72, "── 使用者層（待設計） ──",
        fontsize=SMALL_FS, ha="center", color="#555", style="italic")

user_roles = [
    ("酪農戶", "閱覽自己牧場"),
    ("顧問",   "預覽複數牧場"),
    ("管理者", "管理 + 密碼保護"),
]
for i, (role, desc) in enumerate(user_roles):
    bx = 1.5 + i * 3.8
    box(ax, bx, 0.55, 3.0, 1.8, C_USER, alpha=0.35, radius=0.2, lw=1.2, ls="--")
    label(ax, bx+1.5, 2.1, role, fs=LABEL_FS, bold=True, color="#c0392b")
    label(ax, bx+1.5, 1.75, desc, fs=SMALL_FS, color="#888")

# 箭頭：前端 → 使用者（虛線）
dashed_arrow(ax, 2.9, 2.9, 2.9, 2.35)
dashed_arrow(ax, 7.05, 2.9, 7.05, 2.35)


# ════════════════════════════════════════════════════════
# 輸出
# ════════════════════════════════════════════════════════
out_path = "/home/elier/Claude/DHI_Net/arch_diagram.png"
plt.tight_layout(pad=0.3)
plt.savefig(out_path, dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print(f"儲存至：{out_path}")
