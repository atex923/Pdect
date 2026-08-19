# Pdect / P找碴

Pdect 是一個繁體中文介面的 Windows PDF 標記工具，主打快速找字、批次標記、圖說註解與安全存檔。適合校稿、審圖、合約或工程文件比對時，把需要注意的文字與區域直接留在 PDF 裡。

## 特色

- 共用關鍵字欄可純搜尋、逐筆跳到命中位置，或批次套用螢光筆／刪除線，並可指定起始頁。
- 緊湊雙列工具列：第一列保留常用搜尋／批次標記，箭頭可持續展開第二列工具，再按一次才收合。
- 支援整份 PDF 連續垂直預覽、拖曳開檔、Ctrl + 滾輪縮放與快速跳頁。
- 3 組可自訂色塊，螢光筆、刪除線與手繪線共用目前選色。
- 手繪水平螢光線、水平刪除線、左上到右下斜線刪除線。
- 可隱藏／顯示畫面中的標記而不修改 PDF 內容。
- 快速窗選清除標記；按工具右側下拉箭頭可一鍵清除整份 PDF 標記，兩者皆可 Undo。
- 選擇文字工具可拖曳框選 PDF 文字並自動複製到系統剪貼簿，可貼到 Word、Google Docs 等文書編輯軟體。
- PDF 書籤下拉工具可輸入名稱、儲存目前頁、跳轉與刪除書籤，新增 / 刪除可 Undo / Redo。
- 再次開啟同一 PDF 時可選擇回到上次檢視頁面。
- 透明內部方框註記，框線顏色沿用目前色塊，粗細沿用刪除線寬度。
- 圖說支援紅框、箭頭、底色、字級調整、拖移、縮放、複製、刪除與雙擊改字。
- Undo / Redo 各最多 10 次，快捷鍵為 Ctrl+Z / Ctrl+Y。
- 正式存檔採安全暫存、驗證、替換、重開流程，降低直接覆寫來源 PDF 的風險。
- Recovery extension 提供 Ctrl+Alt+S 快速儲存、每分鐘 autosave 與異常復原提示。

## 目前版本

- App：V0.4.2
- Launcher：V0.4.2
- Recovery extension：V0.4.2

GitHub 主頁與根目錄只保留目前最新版。舊版來源統一收到 `history/`，並依版號分資料夾保存。

## 使用方式

安裝依賴：

```bash
pip install -r requirements.txt
```

Windows 建議執行：

```text
雙擊 Pdect_V0.4.2.pyw
```

除錯時可用：

```bash
python Pdect_V0.4.2.py
```

## 字型需求

圖說文字使用本機標楷體 `kaiu.ttf` 產生可嵌入 PDF 的向量文字。Windows 預設路徑為：

```text
C:\Windows\Fonts\kaiu.ttf
```

非 Windows 或自訂環境可設定 `PDECT_KAIU_FONT` 指向合法的本機 `kaiu.ttf`。請勿將字型檔提交到 repo 或打包進交付包。

## 專案檔案

- `Pdect_V0.4.2.pyw`：正式入口，載入失敗時會顯示錯誤並寫入 `Pdect_startup_error.log`。
- `Pdect_V0.4.2.py`：console 可見的除錯入口。
- `pdect_app.py`：主程式與 PDF 編輯邏輯。
- `pdect_recovery_ext.py`：Quick Save、autosave、recovery 擴充。
- `README_交接說明.md`：維護交接、架構與驗收清單。
- `src_versioned/`：目前最新版的版本化來源副本。
- `history/`：舊版號歷史區，依版本資料夾收存。

## 歷史版本

- `history/V0.3.5/`：V0.3.5 主程式與 recovery extension 歷史來源。
- `history/V0.3.6/`：V0.3.6 主程式與 recovery extension 歷史來源。
- `history/V0.3.7/`：V0.3.7 主程式與 recovery extension 歷史來源。
- `history/V0.3.8/`：V0.3.8 主程式與 recovery extension 歷史來源。
- `history/V0.4.0/`：V0.4.0 主程式與 recovery extension 歷史來源。
- `history/V0.4.1/`：V0.4.1 主程式與 recovery extension 歷史來源。
