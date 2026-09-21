# 修改紀錄與索引追溯日誌 (Changelog & Modification Index)

本檔案記錄 awesome-stars 專案之重大架構變更、分類索引調整與各項功能演進維護紀錄。

---

## [MOD-20260922-01] 掌機繁體中文化共存版專案連結全面指向 main-zh 分支

- **索引編號**：`[MOD-20260922-01]`
- **日期**：2026-09-22
- **類別**：超連結路徑優化 / 分支導覽 (Routing / Branch Navigation)
- **作者**：yangyws

### 1. 修改動機與原本問題 (Why)
- 使用者指出，個人的 5 個中文化掌機共存專案的繁中在地化提交與發布工作流皆在 `main-zh` 分支上維護。若依預設連至倉庫根目錄，GitHub 會開啟上游同步分支（`main` 或 `android-port`），訪客無法直接閱覽繁中程式碼與 Release 資訊。

### 2. 涉及檔案與模組清單 (Where)
- 修改：[`scripts/generate_stars.py`](file:///D:/github/awesome-stars/scripts/generate_stars.py)
- 修改：[`README.md`](file:///D:/github/awesome-stars/README.md)
- 修改：[`CHANGELOG.md`](file:///D:/github/awesome-stars/CHANGELOG.md)
- 修改：[`D:\github\AGENTS.md`](file:///D:/github/AGENTS.md)

### 3. 具體技術解法與決策細節 (How)
1. 在 `generate_stars.py` 定義 `REPO_CUSTOM_URLS` 字典，將 5 大繁中共存專案之 URL 直接映射至 `/tree/main-zh`：
   - `yangyws/megingiard-zh` ➔ `https://github.com/yangyws/megingiard/tree/main-zh`
   - `yangyws/Dolphin-MMJR2-VBI-zh` ➔ `https://github.com/yangyws/Dolphin-MMJR2-VBI-zh/tree/main-zh`
   - `yangyws/azahar-zh` ➔ `https://github.com/yangyws/azahar-zh/tree/main-zh`
   - `yangyws/pulse-zh` ➔ `https://github.com/yangyws/pulse-zh/tree/main-zh`
   - `yangyws/Cemu-zh` ➔ `https://github.com/yangyws/Cemu-zh/tree/main-zh`
2. 增加 `REPO_NAME_ALIASES` 解決雙庫特例專案（`megingiard-zh` 實體庫名為 `megingiard`）的 API 查詢 404 問題。
3. 修正正則轉義警告 `replace("|", "\\|")`。
4. 重新執行腳本生成最新的 `README.md`。

### 4. 測試驗證結果 (Verification)
- 生成的 `README.md` 中 5 個專案超連結皆已精準導向 `/tree/main-zh`，點擊跳轉正常。

---

## [MOD-20260921-15] 新增「提供程式碼」欄位並追蹤開源狀態

- **索引編號**：`[MOD-20260921-15]`
- **日期**：2026-09-21
- **類別**：資料維度擴充 / 狀態標籤 (Schema Enhancement / Open Source Tracking)
- **作者**：yangyws

### 1. 修改動機與原本問題 (Why)
- 部分收錄專案為純 APK Release 發布庫、閉源工具或設定指南（無開源程式碼）。使用者要求新增「提供程式碼」欄位，以視覺化圖示（`✅ 是` / `❌ 否`）直觀區分。

### 2. 涉及檔案與模組清單 (Where)
- 修改：[`scripts/generate_stars.py`](file:///D:/github/awesome-stars/scripts/generate_stars.py)
- 修改：[`README.md`](file:///D:/github/awesome-stars/README.md)

### 3. 具體技術解法與決策細節 (How)
1. 實作 `check_has_code(repo_name, repo_obj)` 判定邏輯：比對 `NO_CODE_REPOS` 黑名單、`KNOWN_CODE_REPOS` 白名單以及 GitHub language 屬性。
2. 在 Markdown 表格新增居中欄位 `| 提供程式碼 |`，內容標示為 `✅ 是` 或 `❌ 否`。

### 4. 測試驗證結果 (Verification)
- 全庫 125 個專案皆已準確標註（如 5 大中文化共存專案皆為 `✅ 是`，`DualScreen-Launcher`、`wemu-release` 等為 `❌ 否`）。

---

## [MOD-20260921-14] 頂層分類標題統整為單層「掌機繁體中文化共存版」

- **索引編號**：`[MOD-20260921-14]`
- **日期**：2026-09-21
- **類別**：介面版面精簡 (UI / Table of Contents Simplification)
- **作者**：yangyws

### 1. 修改動機與原本問題 (Why)
- 使用者要求頂部中文化專區不需要次級子分類列表，直接保留單層「掌機繁體中文化共存版」即可。

### 2. 涉及檔案與模組清單 (Where)
- 修改：[`scripts/generate_stars.py`](file:///D:/github/awesome-stars/scripts/generate_stars.py)
- 修改：[`README.md`](file:///D:/github/awesome-stars/README.md)

### 3. 具體技術解法與決策細節 (How)
1. 在分類定義支援 `single_level: True` 標記。
2. 當具備此標記時，目錄區只產生單一目錄項，詳細內容區直接渲染表格，不重複產生次級標題。

### 4. 測試驗證結果 (Verification)
- `README.md` 目錄導覽與詳細清單中，中文化專區精簡為單一條目，錨點導覽 100% 正確。

---

## [MOD-20260921-13] 移除「主要語言」與「星星數」欄位

- **索引編號**：`[MOD-20260921-13]`
- **日期**：2026-09-21
- **類別**：表格簡化 (Markdown Table Cleanup)
- **作者**：yangyws

### 1. 修改動機與原本問題 (Why)
- 使用者要求簡化表格呈現，移除「主要語言」與「星星數」欄位，使焦點聚焦於專案名稱與特色定位。

### 2. 涉及檔案與模組清單 (Where)
- 修改：[`scripts/generate_stars.py`](file:///D:/github/awesome-stars/scripts/generate_stars.py)
- 修改：[`README.md`](file:///D:/github/awesome-stars/README.md)

### 3. 具體技術解法與決策細節 (How)
1. 調整 Markdown 表格格式為「儲存庫名稱」與「專案定位與亮點特色」，提升閱讀體驗。

### 4. 測試驗證結果 (Verification)
- 表格成功精簡，版面簡潔俐落。

---

## [MOD-20260921-11] 新增首位大分類「中文化」並收錄個人繁中共存專案

- **索引編號**：`[MOD-20260921-11]`
- **日期**：2026-09-21
- **類別**：首頁分類擴充 (Category Architecture)
- **作者**：yangyws

### 1. 修改動機與原本問題 (Why)
- 使用者要求在 `awesome-stars` 儲存庫中將個人的掌機繁體中文共存專案加入分類索引，並以第一大分類形式置頂呈現。

### 2. 涉及檔案與模組清單 (Where)
- 修改：[`scripts/generate_stars.py`](file:///D:/github/awesome-stars/scripts/generate_stars.py)
- 修改：[`README.md`](file:///D:/github/awesome-stars/README.md)

### 3. 具體技術解法與決策細節 (How)
1. 在分類定義最頂部建立第一大分類，收錄個人掌機繁中共存開源專案。
2. 建立精選專案容錯抓取機制（`fetch_single_repo`）與專案語言標註。

### 4. 測試驗證結果 (Verification)
- 成功抓取並置頂呈現繁中共存專區，目錄跳轉完全正常。
