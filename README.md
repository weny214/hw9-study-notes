# Study Notes

生成式 AI 課程的 Homework 9。網站整理 Prompt、RAG 和 AGENTS.md 三個主題，並用同一份範本產生筆記頁。

## 連結

- 網站：https://weny214.github.io/hw9-study-notes/
- GitHub：https://github.com/weny214/hw9-study-notes

## 功能

- 首頁可以依分類或關鍵字找筆記。
- 每篇都有重點說明、例子、常見錯誤和練習。
- 可以勾選「我已閱讀」，紀錄會留在目前的瀏覽器。

閱讀紀錄不會跨裝置同步，清除瀏覽器資料後也會消失。

## 開啟網站

直接開啟 `index.html` 即可閱讀，也可以在專案根目錄執行：

```bash
python -m http.server 8000
```

接著開啟 http://localhost:8000/ 。網站沒有使用外部套件，不需要 API key。

## 新增一篇筆記

1. 先讀 [AGENTS.md](AGENTS.md)，確認欄位與命名規則。
2. 參考 `templates/note-data.json`，在 `content/notes.json` 加入一筆資料。
3. 執行 `python tools/build.py`，產生新的文章頁和首頁卡片。
4. 檢查分類、搜尋、文章內容與返回連結，再提交修改。

`index.html` 和 `notes/` 是產生的結果。內容請改 `content/notes.json`，版面請改 `templates/note.html`，共用樣式放在 `assets/style.css`。

Windows 也可以使用 `py`，macOS 或 Linux 可依環境使用 `python3`。

## 發布

把專案檔案放在 GitHub 儲存庫根目錄，包含建置好的 `index.html` 與 `notes/`。GitHub Pages 使用 `main` 分支的根目錄。發布後還要開啟正式網址，確認頁面與連結都正常。

## AI 協作

本專案由 ChatGPT 協助整理規則、撰寫初版程式與筆記。專案規則保存在 `AGENTS.md`，之後新增內容時可繼續使用。
