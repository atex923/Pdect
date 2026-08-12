# Pdect / P找碴 V0.3.7 — Codex 交接

## 1. 執行方式
將以下三個檔案放在同一資料夾：

- `Pdect_V0.3.7.pyw`：防閃退啟動器，正式建議入口。
- `pdect_app.py`：主程式，所有 PDF 編輯 UI / 標記 / 圖說 / Undo / Redo 都在這裡。
- `pdect_recovery_ext.py`：可選擴充，負責快速儲存、每分鐘背景預存、異常復原。

GitHub 主頁與根目錄只保留目前最新版；舊版來源移到 `history/Vx.y.z/` 依版號分資料夾保存。

安裝：

```bash
pip install -r requirements.txt
```

Windows 執行：

```text
雙擊 Pdect_V0.3.7.pyw
```

啟動器採 fail-open：`pdect_recovery_ext.py` 載入失敗時只記錄錯誤，仍應繼續啟動 `pdect_app.py`。啟動錯誤寫入 `Pdect_startup_error.log`。

## 2. 目前版本
- 應用程式：V0.3.7
- 啟動器：V0.3.7
- Recovery / Quick Save extension：V0.3.7

## 3. 主要功能
- PDF 拖曳開啟、整份連續垂直預覽。
- Ctrl + 滾輪縮放；一般滾輪捲動；左鍵拖曳平移。
- 關鍵字搜尋後套用螢光筆或刪除線，可指定起始頁。
- 3 個標記色塊，預設紅 / 綠 / 藍；每格下方 `▼` 開色盤。
- 螢光筆透明度、刪除線寬度可調。
- 手繪水平螢光線、水平刪除線、左上到右下斜線刪除線。
- 選擇文字工具：拖曳框選頁面文字後複製到剪貼簿。
- PDF 書籤工具：左側 `+` / `-` 搭配可輸入下拉欄，新增目前頁書籤、刪除選取書籤、下拉跳轉；新增 / 刪除納入 Undo / Redo。
- 再次開啟同一 PDF 時，可選擇回到上次檢視頁面。
- 方框工具：內部透明無色，框線粗細與顏色沿用刪除線寬度與目前色塊。
- 略過已有標記區域。
- 快速窗選清除：紅色虛線框＋橡皮擦圖示；拖出矩形後批次刪除相交標記；圖說任一部分被框到即整組刪除。
- 圖說：紅框、淺米色底、實心紅箭頭、標楷體向量文字；可移動、縮放、拖箭頭、調字級、調底色、右鍵複製/刪除、雙擊修改內容。
- 圖說文字上、左內距 2 px。
- 圖說使用穩定 group ID，Annotation xref 重建後仍可再次修改。
- Undo 最多 10 次（Ctrl+Z）。
- Redo / 回復後一次動作最多 10 次（Ctrl+Y）；新編輯會清除 Redo 歷史。
- 底部快速跳頁（Ctrl+G）。
- 正式存檔使用 `_edit` 版本命名規則；目前主程式存檔策略以 `pdect_app.py` 為準。
- 快速儲存與每 1 分鐘背景預存由 `pdect_recovery_ext.py` 提供。
- 背景暫存預設位置：`%LOCALAPPDATA%\Pdect\autosave`；非 Windows fallback 為 `~/.pdect/autosave`。
- 啟動時掃描暫存與正式檔，異常未同步時提供回存、另存新版本或略過。

## 4. 圖說字型的重要限制
V0.3.x 圖說文字不再依賴一般 FreeText fallback，而是使用 Windows 標楷體實際字型檔：

`C:\Windows\Fonts\kaiu.ttf`

主程式 `_callout_font_path()` 目前找不到該檔時會拋出錯誤。不要把任何字型檔打包進交付包；若未來要支援其他平台，應改為由使用者選字型或建立明確 fallback 策略。

## 5. 存檔與安全性區域 — 修改時特別小心
1. 不要直接在來源 PDF 上做高風險覆寫。既有正式存檔流程會先寫暫存、驗證、再替換並重開。
2. 圖說會插入字型與自訂 content stream，存檔前可能執行 `subset_fonts()`。
3. Quick Save / Autosave 是獨立擴充；擴充失敗不得造成主程式無法啟動。
4. 背景 autosave 不應修改 `dirty=False`，也不應取代正式檔。
5. 正式存檔成功後，要清理相對應背景暫存。
6. Undo / Redo 快照是磁碟檔案，修改相關邏輯時要確保舊快照會刪除，避免 temp 長期堆積。
7. 新動作進入 Undo 歷史時必須清掉 Redo stack；但正在 replay Undo/Redo 時不可誤清掉另一側歷史。

## 6. 近期最重要改版
### V0.3.7
- 新增選擇文字工具，拖曳框選 PDF 文字後複製到剪貼簿。
- 新增 PDF 書籤下拉工具列，支援輸入名稱、`+` 儲存目前頁、`-` 刪除選取書籤、下拉跳轉，新增 / 刪除可 Undo / Redo。
- 新增上次檢視頁面記憶，再次開啟同一檔案時提示是否回到上次頁面。
- 新增透明內部方框註記，框線顏色沿用目前色塊，粗細沿用刪除線寬度。

### V0.3.6
- 啟動依賴檢查同步涵蓋 PySide6 與 PyMuPDF，缺套件時顯示一致安裝提示。
- 圖說標楷體路徑支援 `PDECT_KAIU_FONT` 環境變數；找不到字型時列出已檢查路徑與處理方式。
- Undo / Redo 歷史快照清空或裁切後會同步回收空暫存資料夾。
- Recovery extension 會清理超過 24 小時仍不完整、無法復原的暫存資料夾。

### V0.3.5
- 新增 Redo / 回復後一次動作，Ctrl+Y。
- Undo 前先保存目前 PDF 快照，使刪除、窗選清除、圖說修改等都可重新做回去。
- 新編輯後自動清空 Redo。

### V0.3.4
- 修正圖說第一次修改後，第二次雙擊可能失效。
- 選取圖說新增穩定 group ID；xref 失效時可重新綁定同一群組。
- 雙擊前清掉 move / resize / arrow 暫態操作狀態。

### V0.3.3
- 新增快速窗選清除標記。
- 圖說任一部分相交即整組刪除。
- 整批刪除只建立一次 Undo。

### V0.3.2 / Recovery extension
- 防閃退啟動器。
- 找不到 `pdect_app.py` 時顯示錯誤並寫 log，不再靜默閃退。
- Recovery extension 載入錯誤時 fail-open。

### V0.3.1 / Recovery extension
- 快速儲存按鈕，圖示為磁碟＋閃電，快捷鍵 Ctrl+Alt+S。
- 每 60 秒背景 autosave。
- 開機檢查 autosave 與正式檔是否同步，提供回存／另存新版本／略過。

## 7. 驗收清單
Codex 修改後至少應逐項確認：

- [ ] `python -m py_compile Pdect_V0.3.7.py pdect_app.py pdect_recovery_ext.py` 無 SyntaxError。
- [ ] 沒有 `pdect_recovery_ext.py` 時仍可啟動主程式。
- [ ] 缺少 `pdect_app.py` 時 launcher 顯示訊息而非閃退。
- [ ] 開啟一般 PDF、拖曳 PDF 均正常。
- [ ] Ctrl+滾輪縮放與普通滾輪捲動正常。
- [ ] 關鍵字螢光筆、刪除線正常。
- [ ] 3 色色塊及 `▼` 色盤正常。
- [ ] 手繪三種線正常。
- [ ] 選擇文字框選後會複製文字到剪貼簿。
- [ ] 書籤可新增、下拉跳轉、刪除，新增 / 刪除可 Ctrl+Z / Ctrl+Y。
- [ ] 重新開啟同一 PDF 時會詢問是否回到上次檢視頁面。
- [ ] 方框內部透明無色，框線粗細與顏色沿用設定。
- [ ] 快速窗選清除只刪框內相交標記，框外保留。
- [ ] 圖說可建立、移動、縮放、拖箭頭、改字、連續改字、複製、刪除。
- [ ] Ctrl+Z 連續 Undo 正常，最多 10 次。
- [ ] Ctrl+Y 連續 Redo 正常；Undo 後做新動作，Redo 應清空。
- [ ] 正式存檔後 PDF 可重新開啟，圖說中文字無破字。
- [ ] Quick Save 正常，且不誤蓋不應覆蓋的原始 PDF。
- [ ] 修改後等待 60 秒會建立 autosave；正式存檔後相對應 autosave 被清除。
- [ ] 模擬異常退出後重新啟動，可看到未同步暫存復原提示。

## 8. 版本規則
目前專案已到 `V0.3.7`。一般 bugfix / 小功能請增加第三碼，例如 `V0.3.8`；大型功能或架構調整再增加第二碼。

修改版本時同步更新：
- `pdect_app.py` 的 `APP_VERSION` 與檔頭 changelog。
- `Pdect_V*.pyw` 啟動器的 `APP_VERSION`。
- `pdect_recovery_ext.py` 的 `EXT_VERSION`（若擴充有改）。
- 交付檔名與 ZIP 名稱。
- 舊版來源移入 `history/` 對應版號資料夾，根目錄與 GitHub 主頁維持最新版。
