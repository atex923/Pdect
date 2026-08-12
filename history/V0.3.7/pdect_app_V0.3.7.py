# -*- coding: utf-8 -*-
"""
Pdect - P找碴 V0.3.7
PDF 關鍵字螢光筆 / 刪除線工具

需求套件：
    pip install PySide6 PyMuPDF

V0.3.7：
- 新增選擇文字工具：拖曳框選 PDF 文字後複製到剪貼簿
- 新增 PDF 書籤下拉工具列：可輸入書籤名，以 + 儲存目前頁，以 - 刪除選取書籤，新增 / 刪除納入 Undo / Redo
- 新增上次檢視頁面記憶：再次開啟同一檔案時可選擇回到上次頁面
- 新增透明內部方框註記：框線顏色沿用目前色塊，粗細沿用刪除線寬度

V0.3.6：
- 啟動前同步檢查 PySide6 與 PyMuPDF，缺少套件時給出一致安裝提示
- 圖說標楷體支援 PDECT_KAIU_FONT 環境變數指定合法本機字型路徑，非 Windows / 字型缺失時錯誤更清楚
- 清除 Undo / Redo 歷史時同步回收空的磁碟快照暫存資料夾，降低長時間使用後的暫存殘留

V0.3.4：
- 修正圖說第一次修改後再次雙擊可能無法重新進入文字編輯的問題
- 圖說選取新增穩定 group ID 追蹤，Annotation 重建 / xref 改變後仍可持續修改
- 雙擊圖說時清除拖移 / 縮放的暫態滑鼠狀態，避免第二次點擊被拖移模式攔截

V0.3.3：
- 新增「快速清除標記」窗選工具：在單一 PDF 頁面拖曳矩形，一次刪除框內相交的標記
- 工具列圖示為紅色虛線框，中間搭配橡皮擦圖案
- 圖說只要框到任一部分就整組刪除；一般螢光筆、刪除線、手繪線依相交範圍刪除
- 每次窗選清除只建立一筆 Undo，可由 Ctrl+Z 回復，最多沿用既有 10 次回復

V0.0.16：
- 工具列標記顏色改為 3 個色塊，預設紅 / 綠 / 藍
- 點色塊直接切換目前顏色；色塊下方小倒三角形可開啟色盤，自訂各色塊顏色
- 螢光筆、搜尋刪除線、手繪螢光線、水平 / 斜線刪除線共用目前選中的色塊

V0.0.17：
- 關鍵字輸入欄寬度縮減為原本的一半（210 px -> 105 px）

V0.3.5：
- 新增「重做／回復後一次動作」功能，工具列位於復原右側，快捷鍵 Ctrl+Y
- 連續復原多個動作後可依序重做；新增任何新編輯後會自動清除重做歷史
- 重做以 PDF 安全快照保存復原前狀態，支援新增標記、刪除、快速框選清除與圖說修改等動作

V0.3.0：
- 圖說文字改用實際 kaiu.ttf 建立向量標楷體內容，不再依賴 FreeText 字型替代
- 標楷體嵌入 PDF 並於存檔前原生子集化，避免破字與完整字型造成容量膨脹
- 圖說底色與文字內容串流加入穩定群組標記，支援壓縮重新編號後移動、刪除與復原
- 開啟 V0.2.x PDF 時自動將舊版 Pdect FreeText 圖說修復為新版格式
- 每次開檔採獨立字型資源，確保已子集化 PDF 再次編輯仍可加入新中文字
V0.2.1：
- 工具列固定為單列，開啟、存檔、復原改用圖示
- 「螢光筆透明度」簡化為「透明度」，移除「顏色」文字
- 加粗手繪螢光筆圖示，移除複製圖說按鈕
- 起始頁欄縮為三位數寬度，「頁」移至欄位外
- 移除下方操作說明列
V0.2.0：
- 下方快速跳頁輸入框隱藏上下調整鍵
- 保留直接輸入頁碼、Enter、前往按鈕與 Ctrl+G 快捷操作
V0.1.3：
- 復原按鈕名稱簡化為「復原」，次數移至提示文字
- 螢光筆透明度改為數字輸入，取消拉條
- 刪除線寬度名稱簡化為「寬度」，寬度與起始頁碼輸入取消上下鍵
- 「略過已有標記區域」簡化為「略過標記」
- 工具列寬度不足時自動展開第二列，足夠時合併回單列
V0.1.2：
- 下方狀態列新增快速跳頁欄位與前往按鈕
- 支援輸入頁碼後按 Enter，以及 Ctrl+G 快速聚焦頁碼欄
- 跳頁範圍隨目前 PDF 頁數更新，捲動時同步顯示所在頁碼
V0.1.1：
- 依 330 頁實際 PDF 分析，儲存改用 garbage=2 + object streams 快速無損壓縮
- 避免 garbage=3 在約 85,000 xref 文件上的長時間重複物件掃描
- 儲存狀態顯示快速無損壓縮與前後容量倍率
V0.1.0：
- 取消 V0.0.19 新增的「獨立程序無損壓縮」功能，恢復保守穩定的安全存檔流程
- 儲存流程維持：安全暫存 -> 驗證 -> 關閉工作檔 -> 正式取代 -> 重新開啟
- 圖說文字保留距方框上緣 2 px、左緣 2 px 的內距

V0.0.18：
- 圖說工具列新增「複製圖說」功能鍵
- 圖說上按右鍵可選擇「複製圖說」或「刪除圖說」
- 圖說箭頭改為紅色實心箭頭
- 圖說上雙擊左鍵可修改既有文字內容，並納入 10 次 Undo

V0.0.15：
- 預設標記顏色改為紅色
- 圖說文字改用一般 FreeText，不再使用 Rich Text FreeText，避免中文字型 / HTML appearance 在存檔時造成 MuPDF 底層異常
- 開啟舊版 Pdect 圖說時，存檔前會自動把 Rich Text 圖說文字轉成穩定的一般 FreeText
- 儲存流程改為：寫入同資料夾暫存檔 -> 完整開啟驗證 -> 關閉目前工作 PDF -> 原子取代 / 相容性複製 -> 重新開啟剛儲存的檔案
- 每次存檔成功後重新綁定到實際輸出檔，避免後續覆蓋 / 版本另存時工作文件與檔名不同步
- 存檔統一採保守參數，優先確保大型 PDF 與圖說文件可穩定儲存

V0.0.13：
- 修正加入 Rich Text 圖說後儲存可能使 MuPDF 底層直接異常關閉的問題
- 偵測到本程式圖說時，自動改用「圖說安全儲存模式」：不使用 object streams、字型/圖片重壓縮與高壓縮強度
- 儲存前釋放目前選取的 Annotation 物件參照並執行記憶體整理，降低 Rich Text 註記存檔風險
- 一般沒有圖說的 PDF 仍使用原本的壓縮儲存模式，不影響一般檔案容量優化

V0.0.10：
- Undo / Ctrl+Z 改為最多保留最近 10 次動作
- 新增圖說工具：拖曳建立紅色方框、淺米黃色底色、可延伸箭頭
- 圖說方框可拖曳右下角調整大小，箭頭端點可拖曳延伸
- 圖說方框旁提供直排 + / - 調整字體大小、< / > 調整底色深淺
- 圖說預設字體採標楷體家族（DFKai-SB / BiauKai / KaiTi fallback）
- 儲存改用 object streams + font/image deflate + garbage=3 的無損壓縮策略，降低另存後容量暴增

V0.0.9：
- 增加斜線刪除線手繪按鈕，放在水平手繪刪除線右側
- 斜線方向限定左上到右下，但角度 / 斜率不限
- 斜線刪除線沿用目前選擇顏色與刪除線寬度，透明度固定 100%
- 斜線刪除線支援 Delete、Ctrl+Z 與下方狀態顯示

V0.0.8：
- 視窗下方增加固定「執行狀態」顯示列，統一顯示開檔、搜尋、標記、手繪、刪除、Undo、縮放與儲存結果
- 修正儲存大型 / 多註記 PDF 時可能卡住或失敗的問題
- 儲存改為同資料夾暫存檔 -> 驗證可開啟與頁數 -> 原子取代 _edit.pdf，失敗不會先刪除舊檔
- 取消 garbage=4 + clean=True 的高耗能重度清理，改用較穩定的快速儲存參數並提供備援模式
- 儲存前釋放大型刪除 Undo 快照，降低高頁數 PDF 存檔時的記憶體峰值

V0.0.7：
- 增加手繪螢光線與手繪刪除線，拖曳時強制保持水平
- 手繪按鈕分別放在「螢光筆」與「刪除線」右側
- 手繪螢光線按鈕使用黃色線條圖示；手繪刪除線按鈕使用藍色刪除線圖示
- 手繪註記支援 Delete 刪除與 Ctrl+Z 回復

V0.0.6：
- 工具列增加「目前檢視頁碼」顯示
- 移除工具列的縮放 +/- 功能按鈕，保留 Ctrl+滑鼠滾輪縮放
- 刪除線寬度預設改為 2.5 pt
- 大量頁面搜尋 / 標記效能優化：既有標記每頁只建立一次空間索引
- 新增標記的 Undo 改為只記錄新增註記 xref，不再先壓縮整份 PDF 快照
- 標記完成後只重繪目前需要的頁面，不再重跑整份頁面幾何更新

V0.0.5：
- 修正 Ctrl+滾輪縮放時整份 PDF 重複重建縮圖的異常
- 縮放改為防抖處理，連續滾動時只在停止後重新渲染一次
- 改為可視頁面延遲渲染，畫面外頁面不反覆產生縮圖
- PDF 預覽採 2 倍超取樣渲染，提高文字與線條清晰度

V0.0.4：
- 增加「從第幾頁開始」搜尋與標記
- 增加「略過已有標記區域」勾選功能
- 已有螢光筆 / 文字醒目提示 / 刪除線 / 線條等註記與命中文字區域重疊時可略過，不重複標記

V0.0.2：
- 支援 PDF 拖曳進視窗開啟
- 整份 PDF 連續垂直顯示
- 滑鼠滾輪捲動整份 PDF
- Ctrl + 滑鼠滾輪縮放
- 按住滑鼠左鍵拖曳頁面進行平移
- 增加「回復上一次動作」與 Ctrl+Z
- 搜尋標記拆成「螢光筆」與「刪除線」兩個按鈕
- 螢光筆透明度預設 50%，不再提供外框 / 框線寬度
- 刪除線透明度固定 100%，可調整「刪除線寬度」
- 點選既有註記後按 Delete 刪除
- 儲存成來源檔名 + _edit.pdf；若目前檔名已屬 _edit 系列，可選擇覆蓋或另存 _01、_02…版本
"""

from __future__ import annotations

import sys
import os
import gc
import uuid
import json
import hashlib
import tempfile
import shutil
import re
import time
from pathlib import Path
from bisect import bisect_right
from typing import Optional, Tuple

# PyMuPDF is not needed until the first document is opened. Loading it lazily
# removes a substantial import from the application's cold-start path.
fitz = None


def load_pdf_engine() -> bool:
    """Load and cache PyMuPDF on first use."""
    global fitz
    if fitz is not None:
        return True
    try:
        try:
            import pymupdf as fitz_module
        except ImportError:
            import fitz as fitz_module
        fitz = fitz_module

        return True
    except ImportError:

        return False

try:
    from PySide6.QtCore import Qt, Signal, QRectF, QTimer, QLineF, QEventLoop, QPointF
    from PySide6.QtGui import QAction, QColor, QImage, QPixmap, QPainter, QPen, QKeySequence, QIcon
    from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QFileDialog,
        QMessageBox,
        QToolBar,
        QStyle,
        QLineEdit,
        QPushButton,
        QLabel,
        QDoubleSpinBox,
        QSpinBox,
        QAbstractSpinBox,
        QCheckBox,
        QComboBox,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QScrollArea,
        QSizePolicy,
        QColorDialog,
        QFrame,
        QInputDialog,
        QMenu,
    )
except ImportError:
    # 讓程式仍可進入 main() 顯示缺少套件的提示，而不是在 class 定義階段直接中斷。
    QApplication = None
    QMainWindow = object
    QScrollArea = object
    QLabel = object

    def Signal(*args, **kwargs):
        return None


APP_TITLE = "P找碴"
APP_VERSION = "V0.3.7"

MIN_ZOOM = 0.45
MAX_ZOOM = 4.0
ZOOM_STEP = 0.12

# 預覽品質：以顯示尺寸的 2 倍解析度渲染，再由 Qt 高品質縮回顯示尺寸。
# 只渲染可視頁面，因此提升清晰度時不會讓整份多頁 PDF 同時占用大量記憶體。
RENDER_OVERSAMPLE = 2.0
VISIBLE_PAGE_BUFFER = 900  # 可視區上下預先渲染的像素緩衝
ZOOM_RENDER_DEBOUNCE_MS = 140
SCROLL_RENDER_DEBOUNCE_MS = 45
PAGE_LAYOUT_MARGIN = 18
PAGE_LAYOUT_SPACING = 18
EXISTING_MARK_GRID = 72.0  # 既有標記空間索引格尺寸（PDF point）
HAND_HIGHLIGHT_WIDTH = 12.0  # 手繪螢光線寬度（PDF point）
UNDO_LIMIT = 10
PDECT_KAIU_FONT_ENV = "PDECT_KAIU_FONT"
CALLOUT_DEFAULT_FONT_SIZE = 14.0
CALLOUT_MIN_FONT_SIZE = 6.0
CALLOUT_MAX_FONT_SIZE = 48.0
CALLOUT_BORDER_WIDTH = 1.5
CALLOUT_TEXT_MARGIN_PX = 2.0
PDF_POINTS_PER_CSS_PIXEL = 72.0 / 96.0
CALLOUT_TEXT_MARGIN_PT = CALLOUT_TEXT_MARGIN_PX * PDF_POINTS_PER_CSS_PIXEL
CALLOUT_FONT_FAMILY = "DFKai-SB"
CALLOUT_FONT_RESOURCE_PREFIX = "PdectKaiV030_"
CALLOUT_MIN_RENDER_SCALE = 0.60
CALLOUT_SUBJECT_PREFIX = "PdectCallout:"
CALLOUT_FILL_SHADES = [
    (1.00, 0.985, 0.92),
    (1.00, 0.965, 0.84),
    (1.00, 0.94, 0.74),
    (0.98, 0.89, 0.62),
    (0.95, 0.82, 0.50),
]


class PdfScrollArea(QScrollArea):
    """支援 Ctrl+滾輪縮放，普通滾輪維持 QScrollArea 的自然捲動。"""

    zoomRequested = Signal(float)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta:
                self.zoomRequested.emit(ZOOM_STEP if delta > 0 else -ZOOM_STEP)
                event.accept()
                return
        super().wheelEvent(event)


class PdfPageLabel(QLabel):
    """單一 PDF 頁面；支援選註記、手繪線、圖說建立與圖說幾何編輯。"""

    clicked = Signal(int, float, float)
    panRequested = Signal(int, int)
    manualLineDrawn = Signal(int, float, float, float, float, str)
    calloutBoxDrawn = Signal(int, float, float, float, float)
    calloutControlRequested = Signal(int, str)
    calloutResizeRequested = Signal(int, float, float, float, float)
    calloutMoveRequested = Signal(int, float, float, float, float, float, float)
    calloutArrowRequested = Signal(int, float, float)
    calloutContextRequested = Signal(int, float, float, object)
    calloutDoubleClicked = Signal(int, float, float)
    clearMarksBoxDrawn = Signal(int, float, float, float, float)
    textSelectionBoxDrawn = Signal(int, float, float, float, float)
    squareBoxDrawn = Signal(int, float, float, float, float)

    def __init__(self, page_index: int, parent=None):
        super().__init__(parent)
        self.page_index = page_index
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setScaledContents(True)
        self.setStyleSheet("background: white; border: 1px solid #d0d0d0;")

        self._display_scale = 1.0
        self._selected_rect: Optional[QRectF] = None
        self._press_pos = None
        self._last_global_pos = None
        self._dragging = False
        self._manual_draw_mode: Optional[str] = None
        self._manual_start_pos = None
        self._manual_preview_end_pos = None

        # 圖說選取 / 操作 overlay（PDF 座標保留，縮放時重新換算）
        self._callout_pdf_box = None
        self._callout_pdf_arrow = None
        self._callout_box_rect: Optional[QRectF] = None
        self._callout_arrow_point: Optional[QPointF] = None
        self._callout_control_rects: list[tuple[QRectF, str]] = []
        self._callout_edit_kind: Optional[str] = None
        self._callout_edit_box: Optional[QRectF] = None
        self._callout_edit_arrow: Optional[QPointF] = None
        self._callout_edit_press_pos: Optional[QPointF] = None
        self._callout_edit_origin_box: Optional[QRectF] = None
        self._callout_edit_origin_arrow: Optional[QPointF] = None

    def set_display_scale(self, scale: float):
        self._display_scale = max(0.01, float(scale))
        if self._selected_rect is not None:
            # 一般選取框由 MainWindow 重新設定；此處只同步圖說 overlay。
            pass
        self._sync_callout_overlay()

    def set_selected_pdf_rect(self, rect: Optional[Tuple[float, float, float, float]]):
        if rect is None:
            self._selected_rect = None
        else:
            x0, y0, x1, y1 = rect
            s = self._display_scale
            self._selected_rect = QRectF(x0 * s, y0 * s, (x1 - x0) * s, (y1 - y0) * s)
        self.update()

    def set_callout_overlay(self, box=None, arrow=None):
        if box is None or arrow is None:
            self._callout_pdf_box = None
            self._callout_pdf_arrow = None
            self._callout_box_rect = None
            self._callout_arrow_point = None
            self._callout_control_rects = []
            self._callout_edit_kind = None
            self._callout_edit_press_pos = None
            self._callout_edit_origin_box = None
            self._callout_edit_origin_arrow = None
        else:
            self._callout_pdf_box = tuple(float(v) for v in box)
            self._callout_pdf_arrow = (float(arrow[0]), float(arrow[1]))
            self._sync_callout_overlay()
        self.update()

    def _sync_callout_overlay(self):
        if self._callout_pdf_box is None or self._callout_pdf_arrow is None:
            return
        x0, y0, x1, y1 = self._callout_pdf_box
        s = self._display_scale
        self._callout_box_rect = QRectF(x0*s, y0*s, (x1-x0)*s, (y1-y0)*s)
        self._callout_arrow_point = QPointF(self._callout_pdf_arrow[0]*s, self._callout_pdf_arrow[1]*s)
        self._update_callout_control_rects()

    def _update_callout_control_rects(self):
        self._callout_control_rects = []
        r = self._callout_box_rect
        if r is None:
            return
        w, h, gap = 24.0, 22.0, 2.0
        x = r.right() + 6.0
        if x + w > self.width() - 2:
            x = max(2.0, r.left() - w - 6.0)
        y = max(2.0, min(float(self.height()) - (h+gap)*4 - 2.0, r.top()))
        for i, action in enumerate(("font_plus", "font_minus", "shade_lighter", "shade_darker")):
            self._callout_control_rects.append((QRectF(x, y+i*(h+gap), w, h), action))

    def set_manual_draw_mode(self, mode: Optional[str]):
        self._manual_draw_mode = mode
        self._manual_start_pos = None
        self._manual_preview_end_pos = None
        if mode:
            self.setCursor(Qt.CrossCursor)
        else:
            self.unsetCursor()
        self.update()

    @staticmethod
    def _near_point(a: QPointF, b: QPointF, radius=10.0):
        dx = a.x()-b.x(); dy = a.y()-b.y()
        return dx*dx + dy*dy <= radius*radius

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and self.pixmap() is not None:
            pos = event.position()
            self.calloutContextRequested.emit(
                self.page_index,
                pos.x() / self._display_scale,
                pos.y() / self._display_scale,
                event.globalPosition().toPoint(),
            )
            event.accept()
            return

        if event.button() == Qt.LeftButton and self.pixmap() is not None:
            pos = event.position()

            # 圖說旁的 + - < > 操作鈕優先於頁面拖曳。
            if self._manual_draw_mode is None and self._callout_box_rect is not None:
                self._update_callout_control_rects()
                for rect, action in self._callout_control_rects:
                    if rect.contains(pos):
                        self.calloutControlRequested.emit(self.page_index, action)
                        event.accept()
                        return

                # 箭頭端點可拖曳延伸。
                if self._callout_arrow_point is not None and self._near_point(pos, self._callout_arrow_point, 11.0):
                    self._callout_edit_kind = "arrow"
                    self._callout_edit_arrow = QPointF(pos)
                    self._callout_edit_box = QRectF(self._callout_box_rect)
                    self._callout_edit_press_pos = QPointF(pos)
                    self._callout_edit_origin_box = QRectF(self._callout_box_rect)
                    self._callout_edit_origin_arrow = QPointF(self._callout_arrow_point) if self._callout_arrow_point else None
                    self.setCursor(Qt.CrossCursor)
                    event.accept(); return

                # 方框右下角 resize handle。
                handle = QRectF(self._callout_box_rect.right()-8, self._callout_box_rect.bottom()-8, 16, 16)
                if handle.contains(pos):
                    self._callout_edit_kind = "resize"
                    self._callout_edit_box = QRectF(self._callout_box_rect)
                    self._callout_edit_arrow = QPointF(self._callout_arrow_point) if self._callout_arrow_point else None
                    self._callout_edit_press_pos = QPointF(pos)
                    self._callout_edit_origin_box = QRectF(self._callout_box_rect)
                    self._callout_edit_origin_arrow = QPointF(self._callout_arrow_point) if self._callout_arrow_point else None
                    self.setCursor(Qt.SizeFDiagCursor)
                    event.accept(); return

                # 在圖說方框內拖曳：整組搬移（方框、文字與箭頭一起移動）。
                if self._callout_box_rect.contains(pos):
                    self._callout_edit_kind = "move"
                    self._callout_edit_box = QRectF(self._callout_box_rect)
                    self._callout_edit_arrow = QPointF(self._callout_arrow_point) if self._callout_arrow_point else None
                    self._callout_edit_press_pos = QPointF(pos)
                    self._callout_edit_origin_box = QRectF(self._callout_box_rect)
                    self._callout_edit_origin_arrow = QPointF(self._callout_arrow_point) if self._callout_arrow_point else None
                    self.setCursor(Qt.SizeAllCursor)
                    event.accept(); return

            if self._manual_draw_mode:
                self._manual_start_pos = pos
                self._manual_preview_end_pos = pos
                self._dragging = True
                event.accept(); self.update(); return

            self._press_pos = pos
            self._last_global_pos = event.globalPosition()
            self._dragging = False
            self.setCursor(Qt.ClosedHandCursor)
            event.accept(); return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position()

        if self._callout_edit_kind and (event.buttons() & Qt.LeftButton):
            x = max(0.0, min(float(self.width()), pos.x()))
            y = max(0.0, min(float(self.height()), pos.y()))
            if self._callout_edit_kind == "arrow":
                self._callout_edit_arrow = QPointF(x, y)
            elif self._callout_edit_kind == "resize" and self._callout_edit_box is not None:
                # 不再限制方框的固定最小長寬；僅保留 1px 以維持有效矩形。
                self._callout_edit_box.setRight(max(self._callout_edit_box.left()+1.0, min(float(self.width()), x)))
                self._callout_edit_box.setBottom(max(self._callout_edit_box.top()+1.0, min(float(self.height()), y)))
            elif (
                self._callout_edit_kind == "move"
                and self._callout_edit_box is not None
                and self._callout_edit_arrow is not None
                and self._callout_edit_press_pos is not None
            ):
                # 以按下位置為基準計算位移，並讓方框 + 箭頭整組保持在頁面範圍內。
                base_box = QRectF(self._callout_edit_origin_box or self._callout_box_rect)
                base_arrow = QPointF(self._callout_edit_origin_arrow or self._callout_arrow_point)
                dx = pos.x() - self._callout_edit_press_pos.x()
                dy = pos.y() - self._callout_edit_press_pos.y()
                min_x = min(base_box.left(), base_arrow.x())
                max_x = max(base_box.right(), base_arrow.x())
                min_y = min(base_box.top(), base_arrow.y())
                max_y = max(base_box.bottom(), base_arrow.y())
                dx = max(-min_x, min(float(self.width())-max_x, dx))
                dy = max(-min_y, min(float(self.height())-max_y, dy))
                self._callout_edit_box = QRectF(base_box.translated(dx, dy))
                self._callout_edit_arrow = QPointF(base_arrow.x()+dx, base_arrow.y()+dy)
            self.update(); event.accept(); return

        if self._manual_draw_mode and self._manual_start_pos is not None and (event.buttons() & Qt.LeftButton):
            if self._manual_draw_mode in ("highlight", "strike"):
                x = max(0.0, min(float(self.width()), pos.x()))
                self._manual_preview_end_pos = QPointF(x, self._manual_start_pos.y())
            elif self._manual_draw_mode == "strike_diag":
                x = max(float(self._manual_start_pos.x()), min(float(self.width()), pos.x()))
                y = max(float(self._manual_start_pos.y()), min(float(self.height()), pos.y()))
                self._manual_preview_end_pos = QPointF(x, y)
            else:  # callout / clear_marks / select_text / square：自由拖出矩形
                x = max(0.0, min(float(self.width()), pos.x()))
                y = max(0.0, min(float(self.height()), pos.y()))
                self._manual_preview_end_pos = QPointF(x, y)
            self.update(); event.accept(); return

        if self._last_global_pos is not None and (event.buttons() & Qt.LeftButton):
            current = event.globalPosition()
            dx = current.x() - self._last_global_pos.x(); dy = current.y() - self._last_global_pos.y()
            if self._press_pos is not None:
                local_delta = pos - self._press_pos
                if abs(local_delta.x()) + abs(local_delta.y()) >= 4:
                    self._dragging = True
            if self._dragging:
                self.panRequested.emit(int(dx), int(dy))
                self._last_global_pos = current
                event.accept(); return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._callout_edit_kind:
            kind = self._callout_edit_kind
            box = self._callout_edit_box
            arrow = self._callout_edit_arrow
            origin_box = self._callout_edit_origin_box
            origin_arrow = self._callout_edit_origin_arrow
            self._callout_edit_kind = None
            self._callout_edit_press_pos = None
            self._callout_edit_origin_box = None
            self._callout_edit_origin_arrow = None
            self.unsetCursor()
            self.update()
            if kind == "resize" and box is not None:
                s = self._display_scale
                self.calloutResizeRequested.emit(self.page_index, box.left()/s, box.top()/s, box.right()/s, box.bottom()/s)
            elif kind == "move" and box is not None and arrow is not None:
                s = self._display_scale
                # 位移量為 0 時不建立無意義 Undo。
                oldb = origin_box
                olda = origin_arrow
                changed = (
                    oldb is None or olda is None
                    or abs(box.left()-oldb.left()) > 0.5
                    or abs(box.top()-oldb.top()) > 0.5
                    or abs(arrow.x()-olda.x()) > 0.5
                    or abs(arrow.y()-olda.y()) > 0.5
                )
                if changed:
                    self.calloutMoveRequested.emit(
                        self.page_index,
                        box.left()/s, box.top()/s, box.right()/s, box.bottom()/s,
                        arrow.x()/s, arrow.y()/s,
                    )
            elif kind == "arrow" and arrow is not None:
                s = self._display_scale
                self.calloutArrowRequested.emit(self.page_index, arrow.x()/s, arrow.y()/s)
            event.accept(); return

        if event.button() == Qt.LeftButton and self._manual_draw_mode and self._manual_start_pos is not None:
            start = self._manual_start_pos
            end = self._manual_preview_end_pos if self._manual_preview_end_pos is not None else event.position()
            mode = self._manual_draw_mode

            if mode in ("callout", "clear_marks", "select_text", "square"):
                x0d, x1d = sorted((float(start.x()), float(end.x())))
                y0d, y1d = sorted((float(start.y()), float(end.y())))
                self._manual_start_pos = None; self._manual_preview_end_pos = None; self._dragging = False; self.update()
                s = self._display_scale
                if mode == "callout":
                    if (x1d-x0d) >= 30.0 and (y1d-y0d) >= 20.0:
                        self.calloutBoxDrawn.emit(self.page_index, x0d/s, y0d/s, x1d/s, y1d/s)
                elif mode == "clear_marks":
                    if (x1d-x0d) >= 4.0 and (y1d-y0d) >= 4.0:
                        self.clearMarksBoxDrawn.emit(self.page_index, x0d/s, y0d/s, x1d/s, y1d/s)
                elif mode == "select_text":
                    if (x1d-x0d) >= 4.0 and (y1d-y0d) >= 4.0:
                        self.textSelectionBoxDrawn.emit(self.page_index, x0d/s, y0d/s, x1d/s, y1d/s)
                else:
                    if (x1d-x0d) >= 4.0 and (y1d-y0d) >= 4.0:
                        self.squareBoxDrawn.emit(self.page_index, x0d/s, y0d/s, x1d/s, y1d/s)
                event.accept(); return

            if mode in ("highlight", "strike"):
                end_x = max(0.0, min(float(self.width()), float(end.x())))
                end_y = float(start.y())
            else:
                end_x = max(float(start.x()), min(float(self.width()), float(end.x())))
                end_y = max(float(start.y()), min(float(self.height()), float(end.y())))

            x0 = float(start.x()) / self._display_scale; y0 = float(start.y()) / self._display_scale
            x1 = end_x / self._display_scale; y1 = end_y / self._display_scale
            self._manual_start_pos = None; self._manual_preview_end_pos = None; self._dragging = False; self.update()
            dx = end_x - float(start.x()); dy = end_y - float(start.y())
            if (dx*dx + dy*dy) ** 0.5 >= 3.0:
                self.manualLineDrawn.emit(self.page_index, x0, y0, x1, y1, mode)
            event.accept(); return

        if event.button() == Qt.LeftButton and self._last_global_pos is not None:
            self.unsetCursor()
            if not self._dragging and self.pixmap() is not None:
                pos = event.position()
                self.clicked.emit(self.page_index, pos.x()/self._display_scale, pos.y()/self._display_scale)
            self._press_pos = None; self._last_global_pos = None; self._dragging = False
            event.accept(); return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.pixmap() is not None:
            pos = event.position()
            # Qt 的雙擊序列會先送出第二次 mousePressEvent。若圖說已被選取，
            # 該次 press 可能先把狀態切成 move / resize / arrow；若不清掉，
            # 對話框關閉後的 release 會再處理舊幾何狀態，造成後續雙擊失效。
            self._callout_edit_kind = None
            self._callout_edit_box = None
            self._callout_edit_arrow = None
            self._callout_edit_press_pos = None
            self._callout_edit_origin_box = None
            self._callout_edit_origin_arrow = None
            self._press_pos = None
            self._last_global_pos = None
            self._dragging = False
            self.unsetCursor()
            # 正在使用手繪 / 窗選工具時，不把雙擊誤判成圖說文字編輯。
            if self._manual_draw_mode is None:
                self.calloutDoubleClicked.emit(
                    self.page_index,
                    pos.x() / self._display_scale,
                    pos.y() / self._display_scale,
                )
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = None
        if self._selected_rect is not None:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(220, 30, 30), 2, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self._selected_rect)

        # 圖說選取 overlay：框、resize handle、箭頭端點、直排控制鈕。
        box = self._callout_edit_box if self._callout_edit_kind in ("resize", "move") else self._callout_box_rect
        arrow = self._callout_edit_arrow if self._callout_edit_kind in ("arrow", "move") else self._callout_arrow_point
        if box is not None and arrow is not None:
            if painter is None: painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(QPen(QColor(220, 30, 30), 2, Qt.DashLine))
            painter.setBrush(Qt.NoBrush); painter.drawRect(box)
            # 視覺提示箭頭控制線
            attach = QPointF(box.left(), max(box.top(), min(box.bottom(), arrow.y())))
            painter.setPen(QPen(QColor(210, 35, 35, 180), 1.5, Qt.DashLine))
            painter.drawLine(QLineF(arrow, attach))
            painter.setBrush(QColor(255,255,255)); painter.setPen(QPen(QColor(210,35,35),2))
            painter.drawEllipse(arrow, 5, 5)
            painter.setBrush(QColor(255,255,255)); painter.drawRect(QRectF(box.right()-6, box.bottom()-6, 12, 12))

            if self._callout_edit_kind is None:
                self._callout_box_rect = QRectF(box)
            self._update_callout_control_rects()
            symbols = {"font_plus":"+", "font_minus":"-", "shade_lighter":"<", "shade_darker":">"}
            for cr, action in self._callout_control_rects:
                painter.setBrush(QColor(250,250,250,245)); painter.setPen(QPen(QColor(120,120,120),1))
                painter.drawRoundedRect(cr, 3, 3)
                painter.setPen(QPen(QColor(40,40,40),1))
                painter.drawText(cr, Qt.AlignCenter, symbols[action])

        if self._manual_draw_mode and self._manual_start_pos is not None and self._manual_preview_end_pos is not None:
            if painter is None: painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            if self._manual_draw_mode in ("callout", "clear_marks", "select_text", "square"):
                x0,x1=sorted((self._manual_start_pos.x(), self._manual_preview_end_pos.x()))
                y0,y1=sorted((self._manual_start_pos.y(), self._manual_preview_end_pos.y()))
                r=QRectF(x0,y0,x1-x0,y1-y0)
                if self._manual_draw_mode == "callout":
                    painter.setBrush(QColor(255,245,205,150)); painter.setPen(QPen(QColor(220,25,25),2))
                    painter.drawRect(r)
                elif self._manual_draw_mode == "clear_marks":
                    painter.setBrush(Qt.NoBrush)
                    painter.setPen(QPen(QColor(220,30,30), 2, Qt.DashLine))
                    painter.drawRect(r)
                    # 框選中心顯示簡化橡皮擦，讓目前工具一眼可辨識。
                    cx, cy = r.center().x(), r.center().y()
                    er = QRectF(cx-11, cy-6, 22, 12)
                    painter.save()
                    painter.translate(er.center())
                    painter.rotate(-28)
                    er2 = QRectF(-11, -6, 22, 12)
                    painter.setPen(QPen(QColor(120,55,55), 1.2))
                    painter.setBrush(QColor(245,150,150,220))
                    painter.drawRoundedRect(er2, 2, 2)
                    painter.setBrush(QColor(245,245,245,235))
                    painter.drawRect(QRectF(2, -6, 9, 12))
                    painter.restore()
                elif self._manual_draw_mode == "select_text":
                    painter.setBrush(QColor(70, 135, 245, 34))
                    painter.setPen(QPen(QColor(45, 115, 220), 2, Qt.DashLine))
                    painter.drawRect(r)
                else:
                    painter.setBrush(Qt.NoBrush)
                    painter.setPen(QPen(QColor(45, 115, 220), max(1.5, 2.0*self._display_scale)))
                    painter.drawRect(r)
            else:
                if self._manual_draw_mode == "highlight":
                    color = QColor(255, 213, 79, 150); width = max(4.0, HAND_HIGHLIGHT_WIDTH*self._display_scale)
                else:
                    color = QColor(45, 115, 220, 235); width = max(2.0, 2.5*self._display_scale)
                painter.setPen(QPen(color, width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(QLineF(self._manual_start_pos, self._manual_preview_end_pos))

        if painter is not None:
            painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_TITLE}  {APP_VERSION}")
        self.resize(1250, 850)
        self.setAcceptDrops(True)

        self.doc: Optional[fitz.Document] = None
        self.pdf_path: Optional[Path] = None
        self.zoom = 1.25
        # 三格標記色盤：預設紅、綠、藍。current_color 永遠指向目前選中的色格。
        self.palette_colors = [QColor("#FF0000"), QColor("#00A83B"), QColor("#0066FF")]
        self.active_color_index = 0
        self.current_color = QColor(self.palette_colors[self.active_color_index])
        self.color_swatch_buttons: list[QPushButton] = []
        self.color_drop_buttons: list[QPushButton] = []
        self.manual_draw_mode: Optional[str] = None
        self.dirty = False
        # 每次開啟文件使用新的資源名，避免已子集化字型無法加入新字元。
        self.callout_font_resource = CALLOUT_FONT_RESOURCE_PREFIX + uuid.uuid4().hex[:8]
        self._callout_font_needs_subset = False

        self.page_labels: list[PdfPageLabel] = []
        self.page_top_positions: list[int] = []
        # 僅記錄「目前縮放倍率下」已完成高解析度渲染的頁面。
        # QLabel 自己持有 QPixmap，不另外複製一份快取，避免大型 PDF 記憶體暴增。
        self.rendered_pages: set[int] = set()
        self.selected_page_index: Optional[int] = None
        self.selected_annot_xref: Optional[int] = None
        # 圖說的 Annotation 在修改時會整組重建，xref 可能改變；group ID 才是穩定識別。
        self.selected_callout_group_id: Optional[str] = None
        self.selected_annot_rect: Optional[Tuple[float, float, float, float]] = None

        # Undo 最多保留 10 次。新增註記採 xref 輕量記錄；刪除 / 圖說修改採磁碟快照，避免 RAM 暴增。
        self.undo_stack: list[dict] = []
        # Redo history mirrors Undo. Redo states are stored as disk snapshots so
        # both lightweight annotation additions and destructive edits can be replayed reliably.
        self.redo_stack: list[dict] = []
        self._history_replaying = False
        # Full PDF snapshots are only needed by destructive edits. Avoid disk
        # I/O during startup by creating this directory on first use.
        self.undo_temp_dir: Optional[Path] = None
        self._view_state_timer = QTimer(self)
        self._view_state_timer.setSingleShot(True)
        self._view_state_timer.timeout.connect(self._save_current_view_state)

        self._build_ui()

        # 可視頁面延遲渲染：快速捲動 / 快速 Ctrl+滾輪時不會每個事件都重畫整份 PDF。
        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self.render_visible_pages)
        self.scroll.verticalScrollBar().valueChanged.connect(self._on_vertical_scroll)
        self.scroll.horizontalScrollBar().valueChanged.connect(
            lambda _value: self.schedule_visible_render(SCROLL_RENDER_DEBOUNCE_MS)
        )

        self._update_controls()

    # ---------- UI ----------
    def _build_ui(self):
        toolbar = QToolBar("工具列", self)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        self.open_action = QAction("開啟 PDF", self)
        self.open_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        self.open_action.setToolTip("開啟 PDF（Ctrl+O）")
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.open_pdf)
        toolbar.addAction(self.open_action)

        self.save_action = QAction("存檔", self)
        self.save_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.save_action.setToolTip("存檔（Ctrl+S）")
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_pdf)
        toolbar.addAction(self.save_action)

        self.undo_action = QAction("復原", self)
        self.undo_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
        self.undo_action.setShortcut(QKeySequence.Undo)
        self.undo_action.triggered.connect(self.undo_last_action)
        toolbar.addAction(self.undo_action)

        self.redo_action = QAction("重做", self)
        self.redo_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        self.redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        self.redo_action.setToolTip("回復後一次動作（Ctrl+Y）")
        self.redo_action.triggered.connect(self.redo_last_action)
        toolbar.addAction(self.redo_action)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("搜尋："))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("輸入關鍵字")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setFixedWidth(105)
        self.search_edit.returnPressed.connect(self.mark_highlight)
        toolbar.addWidget(self.search_edit)

        toolbar.addWidget(QLabel("從第"))
        self.start_page_spin = QSpinBox()
        self.start_page_spin.setRange(1, 1)
        self.start_page_spin.setValue(1)
        self.start_page_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.start_page_spin.setFixedWidth(48)
        self.start_page_spin.setToolTip("從指定頁碼開始搜尋並標記，一直到文件最後一頁")
        toolbar.addWidget(self.start_page_spin)
        toolbar.addWidget(QLabel("頁"))

        self.skip_existing_check = QCheckBox("略過標記")
        self.skip_existing_check.setChecked(False)
        self.skip_existing_check.setToolTip(
            "勾選後，如果命中文字區域已和螢光筆、文字醒目提示、刪除線、線條等 PDF 註記重疊，則不重複標記"
        )
        toolbar.addWidget(self.skip_existing_check)

        self.color_palette_widget = QWidget()
        palette_layout = QHBoxLayout(self.color_palette_widget)
        palette_layout.setContentsMargins(0, 0, 0, 0)
        palette_layout.setSpacing(3)
        self.color_swatch_buttons.clear()
        self.color_drop_buttons.clear()
        color_names = ["紅色色塊", "綠色色塊", "藍色色塊"]
        for index, color_name in enumerate(color_names):
            color_cell = QWidget()
            color_cell_layout = QVBoxLayout(color_cell)
            color_cell_layout.setContentsMargins(0, 0, 0, 0)
            color_cell_layout.setSpacing(0)

            swatch = QPushButton("")
            swatch.setFixedSize(28, 22)
            swatch.setToolTip(f"{color_name}：點一下直接選用這個顏色")
            swatch.clicked.connect(lambda _checked=False, i=index: self.set_active_color(i))
            color_cell_layout.addWidget(swatch, 0, Qt.AlignHCenter)

            drop = QPushButton("▼")
            drop.setFixedSize(28, 12)
            drop.setToolTip(f"修改{color_name}：開啟色盤")
            drop.clicked.connect(lambda _checked=False, i=index: self.choose_palette_color(i))
            color_cell_layout.addWidget(drop, 0, Qt.AlignHCenter)

            self.color_swatch_buttons.append(swatch)
            self.color_drop_buttons.append(drop)
            palette_layout.addWidget(color_cell)

        self._refresh_color_palette()
        toolbar.addWidget(self.color_palette_widget)

        toolbar.addWidget(QLabel("透明度"))
        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(5, 100)
        self.opacity_spin.setValue(50)
        self.opacity_spin.setSuffix(" %")
        self.opacity_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.opacity_spin.setKeyboardTracking(False)
        self.opacity_spin.setFixedWidth(68)
        self.opacity_spin.setToolTip("直接輸入 5–100 的透明度百分比")
        self.opacity_spin.valueChanged.connect(self._opacity_changed)
        toolbar.addWidget(self.opacity_spin)

        toolbar.addWidget(QLabel("寬度"))
        self.strike_width_spin = QDoubleSpinBox()
        self.strike_width_spin.setRange(0.5, 12.0)
        self.strike_width_spin.setSingleStep(0.5)
        self.strike_width_spin.setDecimals(1)
        self.strike_width_spin.setValue(2.5)
        self.strike_width_spin.setSuffix(" pt")
        self.strike_width_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.strike_width_spin.setFixedWidth(72)
        toolbar.addWidget(self.strike_width_spin)

        self.highlight_btn = QPushButton("螢光筆")
        self.highlight_btn.setToolTip("搜尋關鍵字並套用螢光筆")
        self.highlight_btn.clicked.connect(self.mark_highlight)
        toolbar.addWidget(self.highlight_btn)

        self.manual_highlight_btn = QPushButton()
        self.manual_highlight_btn.setIcon(self._make_manual_tool_icon("highlight"))
        self.manual_highlight_btn.setFixedSize(34, 28)
        self.manual_highlight_btn.setCheckable(True)
        self.manual_highlight_btn.setToolTip("手繪螢光線（只能水平拖曳）")
        self.manual_highlight_btn.clicked.connect(lambda checked: self.set_manual_draw_mode("highlight" if checked else None))
        toolbar.addWidget(self.manual_highlight_btn)

        self.strike_btn = QPushButton("刪除線")
        self.strike_btn.setToolTip("搜尋關鍵字並套用刪除線；透明度固定 100%")
        self.strike_btn.clicked.connect(self.mark_strikeout)
        toolbar.addWidget(self.strike_btn)

        self.manual_strike_btn = QPushButton()
        self.manual_strike_btn.setIcon(self._make_manual_tool_icon("strike"))
        self.manual_strike_btn.setFixedSize(34, 28)
        self.manual_strike_btn.setCheckable(True)
        self.manual_strike_btn.setToolTip("手繪刪除線（只能水平拖曳）")
        self.manual_strike_btn.clicked.connect(lambda checked: self.set_manual_draw_mode("strike" if checked else None))
        toolbar.addWidget(self.manual_strike_btn)

        self.manual_diag_strike_btn = QPushButton()
        self.manual_diag_strike_btn.setIcon(self._make_manual_tool_icon("strike_diag"))
        self.manual_diag_strike_btn.setFixedSize(34, 28)
        self.manual_diag_strike_btn.setCheckable(True)
        self.manual_diag_strike_btn.setToolTip("斜線刪除線（限定左上到右下，角度不限）")
        self.manual_diag_strike_btn.clicked.connect(
            lambda checked: self.set_manual_draw_mode("strike_diag" if checked else None)
        )
        toolbar.addWidget(self.manual_diag_strike_btn)

        self.clear_marks_btn = QPushButton()
        self.clear_marks_btn.setIcon(self._make_manual_tool_icon("clear_marks"))
        self.clear_marks_btn.setFixedSize(34, 28)
        self.clear_marks_btn.setCheckable(True)
        self.clear_marks_btn.setToolTip("快速清除標記：在單一頁面拖曳紅色虛線框，一次刪除框內相交的標記")
        self.clear_marks_btn.clicked.connect(
            lambda checked: self.set_manual_draw_mode("clear_marks" if checked else None)
        )
        toolbar.addWidget(self.clear_marks_btn)

        self.select_text_btn = QPushButton("選字")
        self.select_text_btn.setCheckable(True)
        self.select_text_btn.setToolTip("選擇文字：拖曳框選 PDF 文字，放開後複製到剪貼簿")
        self.select_text_btn.clicked.connect(lambda checked: self.set_manual_draw_mode("select_text" if checked else None))
        toolbar.addWidget(self.select_text_btn)

        self.square_btn = QPushButton("方框")
        self.square_btn.setCheckable(True)
        self.square_btn.setToolTip("方框：拖曳建立透明內部方框；框線顏色沿用目前色塊，粗細沿用刪除線寬度")
        self.square_btn.clicked.connect(lambda checked: self.set_manual_draw_mode("square" if checked else None))
        toolbar.addWidget(self.square_btn)

        self.callout_btn = QPushButton("圖說")
        self.callout_btn.setCheckable(True)
        self.callout_btn.setToolTip(
            "圖說文字：拖曳建立紅框與實心箭頭；選取後可拖移、自由調大小；"
            "雙擊可改文字，右鍵可複製或刪除"
        )
        self.callout_btn.clicked.connect(lambda checked: self.set_manual_draw_mode("callout" if checked else None))
        toolbar.addWidget(self.callout_btn)

        toolbar.addSeparator()

        self.bookmark_add_btn = QPushButton("+")
        self.bookmark_add_btn.setFixedSize(24, 24)
        self.bookmark_add_btn.setToolTip("新增 PDF 書籤：用右側名稱儲存目前頁面")
        self.bookmark_add_btn.clicked.connect(self.add_pdf_bookmark)
        toolbar.addWidget(self.bookmark_add_btn)

        self.bookmark_delete_btn = QPushButton("-")
        self.bookmark_delete_btn.setFixedSize(24, 24)
        self.bookmark_delete_btn.setToolTip("刪除 PDF 書籤：刪除目前下拉選單選到的書籤")
        self.bookmark_delete_btn.clicked.connect(self.delete_pdf_bookmark)
        toolbar.addWidget(self.bookmark_delete_btn)

        self.bookmark_combo = QComboBox()
        self.bookmark_combo.setEditable(True)
        self.bookmark_combo.setInsertPolicy(QComboBox.NoInsert)
        self.bookmark_combo.setMaxVisibleItems(12)
        self.bookmark_combo.setFixedWidth(160)
        self.bookmark_combo.setToolTip("PDF 書籤：可輸入書籤名後按 +；下拉選擇既有書籤會跳到該頁")
        self.bookmark_combo.lineEdit().setPlaceholderText("書籤名")
        self.bookmark_combo.activated.connect(self.go_to_pdf_bookmark)
        toolbar.addWidget(self.bookmark_combo)

        # 工具列固定單列；依完整內容設定視窗最小寬度，避免工具被 overflow 隱藏。
        self.primary_toolbar = toolbar
        QTimer.singleShot(0, self._lock_single_toolbar_width)

        # 縮放 +/- 按鈕與頁碼 / 縮放資訊皆不放在工具列。
        # 頁碼、總頁數與縮放倍率統一移到下方狀態列右側。

        # PDF 連續預覽區
        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        self.scroll = PdfScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.zoomRequested.connect(self.change_zoom)

        self.pages_host = QWidget()
        self.pages_layout = QVBoxLayout(self.pages_host)
        self.pages_layout.setContentsMargins(PAGE_LAYOUT_MARGIN, PAGE_LAYOUT_MARGIN, PAGE_LAYOUT_MARGIN, PAGE_LAYOUT_MARGIN)
        self.pages_layout.setSpacing(PAGE_LAYOUT_SPACING)
        self.pages_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.empty_label = QLabel("拖曳 PDF 到視窗\n或按「開啟 PDF」")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 18px; color: #777; padding: 80px;")
        self.pages_layout.addWidget(self.empty_label, 0, Qt.AlignCenter)

        self.scroll.setWidget(self.pages_host)
        central_layout.addWidget(self.scroll, 1)

        bottom = QWidget()
        bottom_layout = QVBoxLayout(bottom)
        bottom_layout.setContentsMargins(8, 4, 8, 5)
        bottom_layout.setSpacing(3)

        # 保留選取狀態供程式內部更新，但不再顯示下方操作說明列。
        self.selection_label = QLabel("未選取註記")
        self.selection_label.hide()

        # 單一狀態列：左側顯示執行結果；右側固定顯示頁碼與縮放資訊。
        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)
        status_row.setSpacing(8)

        status_title = QLabel("狀態：")
        status_title.setStyleSheet("font-weight: 600;")
        self.result_status_label = QLabel(f"{APP_TITLE} {APP_VERSION}｜可直接拖曳 PDF 進視窗")
        self.result_status_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_status_label.setStyleSheet(
            "QLabel { background: #f3f3f3; border: 1px solid #d3d3d3; "
            "border-radius: 3px; padding: 3px 7px; color: #333; }"
        )

        self.current_page_label = QLabel("頁碼：- / -")
        self.current_page_label.setMinimumWidth(105)
        self.current_page_label.setAlignment(Qt.AlignCenter)
        self.current_page_label.setToolTip("目前畫面中央頁碼 / PDF 總頁數")
        self.current_page_label.setStyleSheet(
            "QLabel { background: #f3f3f3; border: 1px solid #d3d3d3; "
            "border-radius: 3px; padding: 3px 7px; color: #333; }"
        )

        self.jump_page_title = QLabel("跳頁：")
        self.jump_page_spin = QSpinBox()
        self.jump_page_spin.setRange(1, 1)
        self.jump_page_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.jump_page_spin.setFixedWidth(72)
        self.jump_page_spin.setAlignment(Qt.AlignCenter)
        self.jump_page_spin.setEnabled(False)
        self.jump_page_spin.setToolTip("輸入頁碼後按 Enter，或按「前往」")
        self.jump_page_spin.lineEdit().returnPressed.connect(self.jump_to_page)

        self.jump_page_button = QPushButton("前往")
        self.jump_page_button.setFixedWidth(48)
        self.jump_page_button.setEnabled(False)
        self.jump_page_button.setToolTip("立即跳到指定頁面（Ctrl+G 可快速聚焦頁碼欄）")
        self.jump_page_button.clicked.connect(self.jump_to_page)

        self.zoom_label = QLabel("縮放：125%")
        self.zoom_label.setMinimumWidth(82)
        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.setToolTip("使用 Ctrl + 滑鼠滾輪調整縮放")
        self.zoom_label.setStyleSheet(
            "QLabel { background: #f3f3f3; border: 1px solid #d3d3d3; "
            "border-radius: 3px; padding: 3px 7px; color: #333; }"
        )

        # 保留相容性欄位供既有更新函式使用，但不再額外顯示「總頁數」一格。
        self.page_count_label = QLabel("0 頁")
        self.page_count_label.hide()

        status_row.addWidget(status_title)
        status_row.addWidget(self.result_status_label, 1)
        status_row.addWidget(self.current_page_label, 0)
        status_row.addWidget(self.jump_page_title, 0)
        status_row.addWidget(self.jump_page_spin, 0)
        status_row.addWidget(self.jump_page_button, 0)
        status_row.addWidget(self.zoom_label, 0)
        bottom_layout.addLayout(status_row)
        central_layout.addWidget(bottom)

        self.setCentralWidget(central)
        # 不再建立 QMainWindow 內建 StatusBar，避免下方出現兩行重複狀態。
        self._set_status(f"{APP_TITLE} {APP_VERSION}｜可直接拖曳 PDF 進視窗")

        self.delete_action = QAction(self)
        self.delete_action.setShortcut(QKeySequence(Qt.Key_Delete))
        self.delete_action.triggered.connect(self.delete_selected_annotation)
        self.addAction(self.delete_action)

        self.jump_focus_action = QAction(self)
        self.jump_focus_action.setShortcut(QKeySequence("Ctrl+G"))
        self.jump_focus_action.triggered.connect(self.focus_jump_page)
        self.addAction(self.jump_focus_action)

    def _lock_single_toolbar_width(self):
        """Keep every toolbar control visible on one row."""
        if not hasattr(self, "primary_toolbar"):
            return
        required_width = self.primary_toolbar.sizeHint().width() + 20
        self.setMinimumWidth(max(self.minimumWidth(), required_width))

    def _make_manual_tool_icon(self, mode: str) -> QIcon:
        """以 QPainter 直接畫工具圖示，不依賴外部圖片檔。"""
        pix = QPixmap(26, 18)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing, True)

        if mode == "highlight":
            # 黃色半透明寬線，模擬螢光筆。
            pen = QPen(QColor(255, 210, 35, 220), 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            p.setPen(pen)
            p.drawLine(4, 10, 22, 10)
            p.setPen(QPen(QColor(150, 120, 0, 150), 1))
            p.drawLine(4, 14, 22, 14)
        elif mode == "select_text":
            p.setBrush(QColor(70, 135, 245, 45))
            p.setPen(QPen(QColor(45, 115, 220), 1.8, Qt.DashLine))
            p.drawRect(3, 3, 20, 12)
            p.setPen(QPen(QColor(60, 60, 60), 1.2))
            p.drawLine(7, 7, 19, 7)
            p.drawLine(7, 11, 17, 11)
        elif mode == "square":
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor(45, 115, 220), 2.2))
            p.drawRect(4, 3, 18, 13)
        elif mode == "strike_diag":
            # 淺灰文字線 + 藍色左上到右下斜線。
            p.setPen(QPen(QColor(125, 125, 125), 2))
            p.drawLine(5, 6, 20, 6)
            p.drawLine(5, 13, 20, 13)
            p.setPen(QPen(QColor(45, 115, 220), 3, Qt.SolidLine, Qt.RoundCap))
            p.drawLine(4, 4, 22, 15)
        elif mode == "clear_marks":
            # 紅色虛線窗選框 + 中央橡皮擦。
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(QColor(220, 35, 35), 1.8, Qt.DashLine))
            p.drawRect(2, 2, 22, 14)
            p.save()
            p.translate(13, 9)
            p.rotate(-28)
            p.setPen(QPen(QColor(120, 55, 55), 1))
            p.setBrush(QColor(245, 140, 140))
            p.drawRoundedRect(QRectF(-7, -4, 14, 8), 1.5, 1.5)
            p.setBrush(QColor(245, 245, 245))
            p.drawRect(QRectF(1, -4, 6, 8))
            p.restore()
        else:
            # 淺灰文字線 + 藍色水平刪除線。
            p.setPen(QPen(QColor(125, 125, 125), 2))
            p.drawLine(5, 6, 20, 6)
            p.drawLine(5, 13, 20, 13)
            p.setPen(QPen(QColor(45, 115, 220), 3, Qt.SolidLine, Qt.RoundCap))
            p.drawLine(3, 9, 23, 9)

        p.end()
        return QIcon(pix)

    def _set_status(self, text: str):
        """統一把所有功能結果顯示在視窗下方的單一狀態列。"""
        text = str(text)
        if hasattr(self, "result_status_label"):
            self.result_status_label.setText(text)
            self.result_status_label.setToolTip(text)
        # 立即刷新狀態文字，特別是進入耗時搜尋 / 儲存前。
        if QApplication is not None:
            try:
                QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
            except Exception:
                QApplication.processEvents()

    def set_manual_draw_mode(self, mode: Optional[str]):
        if mode not in (None, "highlight", "strike", "strike_diag", "clear_marks", "select_text", "square", "callout"):
            mode = None
        if self.doc is None:
            mode = None

        self.manual_draw_mode = mode
        if hasattr(self, "manual_highlight_btn"):
            self.manual_highlight_btn.blockSignals(True)
            self.manual_highlight_btn.setChecked(mode == "highlight")
            self.manual_highlight_btn.blockSignals(False)
        if hasattr(self, "manual_strike_btn"):
            self.manual_strike_btn.blockSignals(True)
            self.manual_strike_btn.setChecked(mode == "strike")
            self.manual_strike_btn.blockSignals(False)
        if hasattr(self, "manual_diag_strike_btn"):
            self.manual_diag_strike_btn.blockSignals(True)
            self.manual_diag_strike_btn.setChecked(mode == "strike_diag")
            self.manual_diag_strike_btn.blockSignals(False)
        if hasattr(self, "clear_marks_btn"):
            self.clear_marks_btn.blockSignals(True)
            self.clear_marks_btn.setChecked(mode == "clear_marks")
            self.clear_marks_btn.blockSignals(False)
        if hasattr(self, "select_text_btn"):
            self.select_text_btn.blockSignals(True)
            self.select_text_btn.setChecked(mode == "select_text")
            self.select_text_btn.blockSignals(False)
        if hasattr(self, "square_btn"):
            self.square_btn.blockSignals(True)
            self.square_btn.setChecked(mode == "square")
            self.square_btn.blockSignals(False)
        if hasattr(self, "callout_btn"):
            self.callout_btn.blockSignals(True)
            self.callout_btn.setChecked(mode == "callout")
            self.callout_btn.blockSignals(False)

        for label in self.page_labels:
            label.set_manual_draw_mode(mode)

        if mode == "highlight":
            self._set_status("手繪螢光線：在 PDF 頁面按住左鍵水平拖曳；線條會自動保持水平")
        elif mode == "strike":
            self._set_status("手繪刪除線：在 PDF 頁面按住左鍵水平拖曳；線條會自動保持水平")
        elif mode == "strike_diag":
            self._set_status("斜線刪除線：由左上往右下拖曳，角度不限；寬度沿用刪除線寬度")
        elif mode == "clear_marks":
            self._set_status("快速清除標記：在單一 PDF 頁面拖曳紅色虛線框，放開後一次刪除框內相交的標記")
        elif mode == "select_text":
            self._set_status("選擇文字：在 PDF 頁面拖曳框選文字，放開後會複製到剪貼簿")
        elif mode == "square":
            self._set_status("方框模式：拖曳建立內部透明無色方框；框線顏色沿用目前色塊，粗細沿用刪除線寬度")
        elif mode == "callout":
            self._set_status("圖說模式：拖曳方框後輸入文字；箭頭為紅色實心；建立後可拖移/縮放/延伸，雙擊改文字，右鍵複製或刪除")
        elif self.doc is not None:
            self._set_status("已離開手繪模式")

    def _opacity_changed(self, value: int):
        if hasattr(self, "result_status_label"):
            self._set_status(f"螢光筆透明度：{value}%")

    def _refresh_color_palette(self):
        """更新三格色塊外觀；目前選中的色塊使用較粗外框。"""
        for index, button in enumerate(getattr(self, "color_swatch_buttons", [])):
            color = self.palette_colors[index].name()
            if index == self.active_color_index:
                border = "3px solid #202020"
            else:
                border = "1px solid #777777"
            button.setStyleSheet(
                f"QPushButton {{ background-color: {color}; border: {border}; "
                "border-radius: 2px; padding: 0px; }}"
                "QPushButton:hover { border-color: #000000; }"
            )

        for drop in getattr(self, "color_drop_buttons", []):
            drop.setStyleSheet(
                "QPushButton { border: none; padding: 0px; font-size: 8px; "
                "background: transparent; color: #444444; }"
                "QPushButton:hover { color: #000000; background: #EAEAEA; }"
            )

    def set_active_color(self, index: int):
        if not (0 <= index < len(self.palette_colors)):
            return
        self.active_color_index = index
        self.current_color = QColor(self.palette_colors[index])
        self._refresh_color_palette()
        self._set_status(
            f"目前標記顏色：第 {index + 1} 格 {self.current_color.name().upper()}"
        )

    def choose_palette_color(self, index: int):
        if not (0 <= index < len(self.palette_colors)):
            return
        color = QColorDialog.getColor(
            self.palette_colors[index], self, f"選擇第 {index + 1} 格標記顏色"
        )
        if not color.isValid():
            return
        self.palette_colors[index] = QColor(color)
        if index == self.active_color_index:
            self.current_color = QColor(color)
        self._refresh_color_palette()
        self._set_status(
            f"第 {index + 1} 格顏色已改為：{color.name().upper()}"
        )

    def _update_controls(self):
        try:
            has_doc = self.doc is not None and not self.doc.is_closed and len(self.doc) > 0
        except Exception:
            has_doc = False
        self.save_action.setEnabled(has_doc)
        self.highlight_btn.setEnabled(has_doc)
        self.strike_btn.setEnabled(has_doc)
        if hasattr(self, "manual_highlight_btn"):
            self.manual_highlight_btn.setEnabled(has_doc)
        if hasattr(self, "manual_strike_btn"):
            self.manual_strike_btn.setEnabled(has_doc)
        if hasattr(self, "manual_diag_strike_btn"):
            self.manual_diag_strike_btn.setEnabled(has_doc)
        if hasattr(self, "clear_marks_btn"):
            self.clear_marks_btn.setEnabled(has_doc)
        if hasattr(self, "select_text_btn"):
            self.select_text_btn.setEnabled(has_doc)
        if hasattr(self, "square_btn"):
            self.square_btn.setEnabled(has_doc)
        if hasattr(self, "callout_btn"):
            self.callout_btn.setEnabled(has_doc)
        if hasattr(self, "bookmark_add_btn"):
            self.bookmark_add_btn.setEnabled(has_doc)
        if hasattr(self, "bookmark_delete_btn"):
            self.bookmark_delete_btn.setEnabled(has_doc and self._selected_bookmark_index() is not None)
        if hasattr(self, "bookmark_combo"):
            self.bookmark_combo.setEnabled(has_doc)

        self.undo_action.setEnabled(bool(self.undo_stack))
        self.undo_action.setText("復原")
        self.undo_action.setToolTip(f"復原上一個動作｜可復原 {len(self.undo_stack)} / {UNDO_LIMIT}")
        if hasattr(self, "redo_action"):
            self.redo_action.setEnabled(bool(self.redo_stack))
            self.redo_action.setText("重做")
            self.redo_action.setToolTip(f"回復後一次動作（Ctrl+Y）｜可重做 {len(self.redo_stack)} / {UNDO_LIMIT}")
        self.page_count_label.setText(f"{len(self.doc)} 頁" if has_doc else "0 頁")
        if hasattr(self, "jump_page_spin"):
            max_page = len(self.doc) if has_doc else 1
            self.jump_page_spin.setRange(1, max_page)
            self.jump_page_spin.setEnabled(has_doc)
            self.jump_page_button.setEnabled(has_doc)
            if self.jump_page_spin.value() > max_page:
                self.jump_page_spin.setValue(max_page)
        if hasattr(self, "start_page_spin"):
            max_page = len(self.doc) if has_doc else 1
            self.start_page_spin.setRange(1, max_page)
            self.start_page_spin.setEnabled(has_doc)
            if self.start_page_spin.value() > max_page:
                self.start_page_spin.setValue(max_page)
        if hasattr(self, "skip_existing_check"):
            self.skip_existing_check.setEnabled(has_doc)
        self.zoom_label.setText(f"縮放：{int(round(self.zoom * 100))}%")
        self._update_current_page_label()

    # ---------- 拖曳開檔 ----------
    def dragEnterEvent(self, event):
        urls = event.mimeData().urls() if event.mimeData().hasUrls() else []
        if any(Path(url.toLocalFile()).suffix.lower() == ".pdf" for url in urls):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.suffix.lower() == ".pdf" and path.exists():
                self.open_pdf_path(path)
                event.acceptProposedAction()
                return
        event.ignore()

    # ---------- PDF 開啟 / 連續顯示 ----------
    def open_pdf(self):
        if not load_pdf_engine():
            QMessageBox.critical(self, "缺少套件", "找不到 PyMuPDF。\n請先執行：pip install PyMuPDF")
            return

        path, _ = QFileDialog.getOpenFileName(self, "開啟 PDF", "", "PDF Files (*.pdf)")
        if path:
            self.open_pdf_path(Path(path))

    def open_pdf_path(self, path: Path):
        if not load_pdf_engine():
            QMessageBox.critical(self, "缺少套件", "找不到 PyMuPDF。\n請先執行：pip install PyMuPDF")
            return

        if self.dirty:
            reply = QMessageBox.question(
                self,
                "尚未存檔",
                "目前 PDF 有尚未儲存的修改，仍要開啟其他檔案嗎？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        self._save_current_view_state()
        remembered_page = self._remembered_view_page(path)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            if self.doc is not None:
                self.doc.close()

            self.doc = fitz.open(str(path))
            self.pdf_path = path
            self.dirty = False
            self.callout_font_resource = CALLOUT_FONT_RESOURCE_PREFIX + uuid.uuid4().hex[:8]
            self._callout_font_needs_subset = False
            self._clear_undo_stack()
            converted = self._migrate_legacy_pdect_callouts()
            self.dirty = converted > 0
            self.start_page_spin.setRange(1, max(1, len(self.doc)))
            self.start_page_spin.setValue(1)
            self.set_manual_draw_mode(None)
            self._clear_selection(update_view=False)
            self._refresh_bookmark_combo()
            self.render_all_pages(preserve_scroll=False)
            if converted:
                self._set_status(
                    f"已開啟：{path.name}｜共 {len(self.doc)} 頁｜已修復 {converted} 個舊版圖說字型，請存檔"
                )
            else:
                self._set_status(f"已開啟：{path.name}｜共 {len(self.doc)} 頁")
            if remembered_page is not None:
                QTimer.singleShot(180, lambda p=Path(path), page=remembered_page: self._prompt_restore_view_page(p, page))
        except Exception as e:
            self._set_status(f"開啟失敗：{e}")
            QMessageBox.critical(self, "開啟失敗", f"無法開啟 PDF：\n{e}")
            self.doc = None
            self.pdf_path = None
            self._refresh_bookmark_combo()
            self.show_empty_view()
        finally:
            QApplication.restoreOverrideCursor()
            self._update_controls()

    def _clear_pages_layout(self):
        while self.pages_layout.count():
            item = self.pages_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.page_labels.clear()
        self.page_top_positions.clear()
        self.rendered_pages.clear()

    def show_empty_view(self):
        self._clear_pages_layout()
        self.empty_label = QLabel("拖曳 PDF 到視窗\n或按「開啟 PDF」")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("font-size: 18px; color: #777; padding: 80px;")
        self.pages_layout.addWidget(self.empty_label, 0, Qt.AlignCenter)
        self._update_controls()

    def _logical_page_size(self, page_index: int) -> tuple[int, int]:
        page = self.doc[page_index]
        rect = page.rect
        width = max(1, int(round(rect.width * self.zoom)))
        height = max(1, int(round(rect.height * self.zoom)))
        return width, height

    def _apply_page_geometry(self, label: PdfPageLabel, page_index: int):
        width, height = self._logical_page_size(page_index)
        label.set_display_scale(self.zoom)
        label.setFixedSize(width, height)
        if label.pixmap() is None:
            label.setText(f"第 {page_index + 1} 頁")
        if (
            self.selected_page_index == page_index
            and self.selected_annot_rect is not None
            and getattr(label, "_callout_pdf_box", None) is None
        ):
            label.set_selected_pdf_rect(self.selected_annot_rect)
        else:
            label.set_selected_pdf_rect(None)

    def _ensure_page_labels(self):
        """建立連續頁面容器；縮放時重用既有 QLabel，不再重建整份頁面。"""
        if self.doc is None:
            return

        if len(self.page_labels) == len(self.doc):
            for page_index, label in enumerate(self.page_labels):
                self._apply_page_geometry(label, page_index)
            self.pages_layout.activate()
            self.pages_host.adjustSize()
            self._rebuild_page_positions()
            return

        self._clear_pages_layout()
        for page_index in range(len(self.doc)):
            label = PdfPageLabel(page_index)
            label.clicked.connect(self.select_annotation_at)
            label.panRequested.connect(self.pan_view)
            label.manualLineDrawn.connect(self.add_manual_line)
            label.calloutBoxDrawn.connect(self.add_callout)
            label.calloutControlRequested.connect(self.adjust_selected_callout)
            label.calloutResizeRequested.connect(self.resize_selected_callout)
            label.calloutMoveRequested.connect(self.move_selected_callout)
            label.calloutArrowRequested.connect(self.move_selected_callout_arrow)
            label.calloutContextRequested.connect(self.show_callout_context_menu)
            label.calloutDoubleClicked.connect(self.edit_callout_at)
            label.clearMarksBoxDrawn.connect(self.clear_marks_in_rect)
            label.textSelectionBoxDrawn.connect(self.select_text_in_rect)
            label.squareBoxDrawn.connect(self.add_square_annotation)
            self._apply_page_geometry(label, page_index)
            label.set_manual_draw_mode(self.manual_draw_mode)
            self.page_labels.append(label)
            self.pages_layout.addWidget(label, 0, Qt.AlignHCenter)

        self.pages_layout.activate()
        self.pages_host.adjustSize()
        self._rebuild_page_positions()

    def _rebuild_page_positions(self):
        """依連續頁面尺寸建立頁面頂端位置快取，讓檢視頁碼可 O(log n) 更新。"""
        self.page_top_positions.clear()
        y = PAGE_LAYOUT_MARGIN
        for label in self.page_labels:
            self.page_top_positions.append(int(y))
            y += label.height() + PAGE_LAYOUT_SPACING

    def _update_current_page_label(self):
        if not hasattr(self, "current_page_label"):
            return
        if self.doc is None or not self.page_labels:
            self.current_page_label.setText("頁碼：- / -")
            return
        page_index = self._current_view_page_index()
        current_page = page_index + 1
        self.current_page_label.setText(f"頁碼：{current_page} / {len(self.doc)}")
        if hasattr(self, "jump_page_spin") and not self.jump_page_spin.lineEdit().hasFocus():
            self.jump_page_spin.blockSignals(True)
            self.jump_page_spin.setValue(current_page)
            self.jump_page_spin.blockSignals(False)

    def _current_view_page_index(self) -> int:
        if not self.page_labels:
            return 0
        if not self.page_top_positions or len(self.page_top_positions) != len(self.page_labels):
            self._rebuild_page_positions()
        center_y = self.scroll.verticalScrollBar().value() + self.scroll.viewport().height() // 2
        page_index = bisect_right(self.page_top_positions, center_y) - 1
        return max(0, min(len(self.page_labels) - 1, page_index))

    def jump_to_page_number(self, page_number: int, *, update_status: bool = True):
        if self.doc is None or not self.page_labels:
            return
        if len(self.page_top_positions) != len(self.page_labels):
            self._rebuild_page_positions()
        page_number = max(1, min(int(page_number), len(self.page_labels)))
        page_index = page_number - 1
        target = max(0, self.page_top_positions[page_index] - PAGE_LAYOUT_MARGIN)
        vbar = self.scroll.verticalScrollBar()
        vbar.setValue(min(target, vbar.maximum()))
        self._update_current_page_label()
        self.schedule_visible_render(0)
        self._schedule_view_state_save()
        if update_status:
            self._set_status(f"已跳至第 {page_number} 頁｜共 {len(self.doc)} 頁")

    def focus_jump_page(self):
        """Focus and select the bottom page field for keyboard-first navigation."""
        if hasattr(self, "jump_page_spin") and self.jump_page_spin.isEnabled():
            self.jump_page_spin.setFocus(Qt.ShortcutFocusReason)
            self.jump_page_spin.lineEdit().selectAll()

    def jump_to_page(self):
        """Scroll directly to the page selected in the bottom page field."""
        if self.doc is None or not self.page_labels:
            return
        self.jump_to_page_number(int(self.jump_page_spin.value()), update_status=True)

    def _on_vertical_scroll(self, _value: int):
        self._update_current_page_label()
        self._schedule_view_state_save()
        self.schedule_visible_render(SCROLL_RENDER_DEBOUNCE_MS)

    @staticmethod
    def _state_root() -> Path:
        local = os.environ.get("LOCALAPPDATA")
        root = Path(local) / "Pdect" if local else Path.home() / ".pdect"
        root.mkdir(parents=True, exist_ok=True)
        return root

    @classmethod
    def _view_state_file(cls) -> Path:
        return cls._state_root() / "view_state.json"

    @staticmethod
    def _view_state_key(path: Path) -> str:
        try:
            text = str(path.resolve(strict=False)).casefold()
        except Exception:
            text = str(path).casefold()
        return hashlib.sha256(text.encode("utf-8", "surrogatepass")).hexdigest()

    @staticmethod
    def _pdf_file_fingerprint(path: Path) -> dict:
        try:
            stat = path.stat()
            return {"size": int(stat.st_size), "mtime_ns": int(stat.st_mtime_ns)}
        except Exception:
            return {}

    @classmethod
    def _load_view_state_store(cls) -> dict:
        try:
            path = cls._view_state_file()
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    @classmethod
    def _save_view_state_store(cls, store: dict) -> None:
        path = cls._view_state_file()
        tmp = path.with_name(path.name + f".tmp_{os.getpid()}_{time.time_ns()}")
        try:
            tmp.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(tmp, path)
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass

    def _schedule_view_state_save(self):
        if getattr(self, "_view_state_timer", None) is None:
            return
        if self.doc is None or self.pdf_path is None or not self.page_labels:
            return
        self._view_state_timer.start(900)

    def _save_current_view_state(self):
        if self.doc is None or self.pdf_path is None or not self.page_labels:
            return
        try:
            page_number = self._current_view_page_index() + 1
            store = self._load_view_state_store()
            store[self._view_state_key(self.pdf_path)] = {
                "path": str(self.pdf_path),
                "fingerprint": self._pdf_file_fingerprint(self.pdf_path),
                "page": int(page_number),
                "updated_at": int(time.time()),
            }
            self._save_view_state_store(store)
        except Exception:
            pass

    def _remembered_view_page(self, path: Path) -> Optional[int]:
        try:
            item = self._load_view_state_store().get(self._view_state_key(path))
            if not isinstance(item, dict):
                return None
            if item.get("fingerprint") != self._pdf_file_fingerprint(path):
                return None
            page = int(item.get("page", 0))
            if page > 0:
                return page
        except Exception:
            pass
        return None

    def _prompt_restore_view_page(self, path: Path, page_number: Optional[int]):
        if self.doc is None or page_number is None or page_number < 1:
            return
        page_number = min(page_number, len(self.doc))
        if page_number <= 1:
            return
        reply = QMessageBox.question(
            self,
            "回到上次檢視頁面",
            f"上次檢視 {path.name} 停在第 {page_number} 頁。\n\n是否回到上次檢視的頁面？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            self.jump_to_page_number(page_number, update_status=False)
            self._set_status(f"已回到上次檢視頁面：第 {page_number} 頁")

    def _selected_bookmark_index(self) -> Optional[int]:
        if not hasattr(self, "bookmark_combo"):
            return None
        index = self.bookmark_combo.currentIndex()
        return index if index >= 0 else None

    def _refresh_bookmark_combo(self):
        if not hasattr(self, "bookmark_combo"):
            return
        combo = self.bookmark_combo
        combo.blockSignals(True)
        combo.clear()
        if self.doc is not None:
            try:
                for row_index, row in enumerate(self.doc.get_toc(simple=True)):
                    if len(row) < 3:
                        continue
                    level, title, page = row[:3]
                    title = str(title).strip()
                    page = int(page)
                    if title and page > 0:
                        combo.addItem(title, {"row": row_index, "page": page, "title": title, "level": int(level)})
            except Exception:
                pass
        combo.setCurrentIndex(-1)
        combo.setEditText("")
        combo.blockSignals(False)
        self._update_controls()

    def _current_bookmark_name(self) -> str:
        if not hasattr(self, "bookmark_combo"):
            return ""
        return self.bookmark_combo.currentText().strip()

    def add_pdf_bookmark(self):
        if self.doc is None:
            return
        name = self._current_bookmark_name()
        if not name:
            self._set_status("請先在書籤欄輸入書籤名")
            self.bookmark_combo.setFocus(Qt.ShortcutFocusReason)
            return
        page_number = self._current_view_page_index() + 1
        undo_entry = None
        try:
            toc = self.doc.get_toc(simple=True)
            undo_entry = self._snapshot_entry(f"新增 PDF 書籤「{name}」", "undo")
            toc.append([1, name, page_number])
            toc.sort(key=lambda row: (int(row[2]), str(row[1]).casefold()))
            self.doc.set_toc(toc)
            self._push_undo_entry(undo_entry)
            undo_entry = None
            self.dirty = True
            self._refresh_bookmark_combo()
            self.bookmark_combo.setEditText("")
            self._set_status(f"已新增 PDF 書籤：{name}｜第 {page_number} 頁｜可 Ctrl+Z 回復")
        except Exception as e:
            if undo_entry is not None:
                self._delete_history_entry_file(undo_entry)
            self._set_status(f"新增書籤失敗：{e}")
            QMessageBox.critical(self, "新增書籤失敗", f"無法新增 PDF 書籤：\n{e}")
        finally:
            self._update_controls()

    def delete_pdf_bookmark(self):
        if self.doc is None or not hasattr(self, "bookmark_combo"):
            return
        index = self._selected_bookmark_index()
        name = self._current_bookmark_name()
        if index is None and not name:
            self._set_status("請先從下拉選單選擇要刪除的書籤")
            return
        undo_entry = None
        try:
            toc = self.doc.get_toc(simple=True)
            if not toc:
                self._set_status("目前 PDF 沒有可刪除的書籤")
                return
            remove_index = None
            data = self.bookmark_combo.itemData(index) if index is not None else None
            if isinstance(data, dict):
                target_page = int(data.get("page", 0))
                target_title = str(data.get("title", ""))
                for row_index, row in enumerate(toc):
                    if len(row) >= 3 and str(row[1]) == target_title and int(row[2]) == target_page:
                        remove_index = row_index
                        break
            if remove_index is None and name:
                for row_index, row in enumerate(toc):
                    if len(row) >= 2 and str(row[1]) == name:
                        remove_index = row_index
                        break
            if remove_index is None:
                self._set_status(f"找不到要刪除的書籤：{name}")
                return

            removed = toc.pop(remove_index)
            undo_entry = self._snapshot_entry(f"刪除 PDF 書籤「{removed[1]}」", "undo")
            self.doc.set_toc(toc)
            self._push_undo_entry(undo_entry)
            undo_entry = None
            self.dirty = True
            self._refresh_bookmark_combo()
            self.bookmark_combo.setEditText("")
            self._set_status(f"已刪除 PDF 書籤：{removed[1]}｜可 Ctrl+Z 回復")
        except Exception as e:
            if undo_entry is not None:
                self._delete_history_entry_file(undo_entry)
            self._set_status(f"刪除書籤失敗：{e}")
            QMessageBox.critical(self, "刪除書籤失敗", f"無法刪除 PDF 書籤：\n{e}")
        finally:
            self._update_controls()

    def go_to_pdf_bookmark(self, index: int):
        if self.doc is None or not hasattr(self, "bookmark_combo") or index < 0:
            return
        data = self.bookmark_combo.itemData(index)
        if not isinstance(data, dict):
            return
        page = int(data.get("page", 0))
        title = str(data.get("title", ""))
        if page > 0:
            self.jump_to_page_number(page, update_status=False)
            self._set_status(f"已前往書籤：{title}｜第 {page} 頁")
            self._update_controls()

    def _refresh_annotation_pages(self, page_indexes):
        """Annotation 改變不影響頁面尺寸；只讓受影響頁面在需要時重新 rasterize。"""
        if self.doc is None:
            return
        for page_index in set(page_indexes):
            if 0 <= page_index < len(self.page_labels):
                self.rendered_pages.discard(page_index)
        self.schedule_visible_render(0)

    def render_all_pages(self, preserve_scroll: bool = True):
        """
        舊名稱保留給搜尋 / Undo / 刪除等功能呼叫。

        V0.0.5 起不再同步 rasterize 全部頁面，只更新連續頁面幾何並把
        目前可視範圍排入高解析度渲染。
        """
        if self.doc is None or len(self.doc) == 0:
            self.show_empty_view()
            return

        hbar = self.scroll.horizontalScrollBar()
        vbar = self.scroll.verticalScrollBar()
        h_ratio = hbar.value() / max(1, hbar.maximum()) if preserve_scroll else 0.0
        v_ratio = vbar.value() / max(1, vbar.maximum()) if preserve_scroll else 0.0

        # 內容或縮放倍率可能已變更：標記所有頁面為待重新渲染。
        # 既有 pixmap 暫時保留並平滑縮放，避免 Ctrl+滾輪時畫面閃白。
        self.rendered_pages.clear()
        self._ensure_page_labels()
        self._update_controls()

        def restore_scroll_and_render():
            if preserve_scroll:
                hbar.setValue(int(h_ratio * hbar.maximum()))
                vbar.setValue(int(v_ratio * vbar.maximum()))
            else:
                hbar.setValue(0)
                vbar.setValue(0)
            self._update_current_page_label()
            self.schedule_visible_render(0)

        QTimer.singleShot(0, restore_scroll_and_render)

    def schedule_visible_render(self, delay_ms: int = SCROLL_RENDER_DEBOUNCE_MS):
        if self.doc is None or not self.page_labels:
            return
        self._render_timer.stop()
        self._render_timer.start(max(0, int(delay_ms)))

    def _nearby_page_indices(self, buffer_px: int = VISIBLE_PAGE_BUFFER) -> range:
        """Return viewport-near page indexes using the cached O(log n) layout index."""
        count = len(self.page_labels)
        if count == 0:
            return range(0)
        if len(self.page_top_positions) != count:
            self._rebuild_page_positions()

        view_top = self.scroll.verticalScrollBar().value()
        top = view_top - buffer_px
        bottom = view_top + self.scroll.viewport().height() + buffer_px
        start = max(0, bisect_right(self.page_top_positions, top) - 1)
        while start < count and self.page_labels[start].geometry().bottom() < top:
            start += 1
        end = max(start, bisect_right(self.page_top_positions, bottom))
        return range(start, min(count, end))

    def _render_page_high_quality(self, page_index: int):
        if self.doc is None or not (0 <= page_index < len(self.doc)):
            return

        page = self.doc[page_index]
        label = self.page_labels[page_index]
        logical_w, logical_h = self._logical_page_size(page_index)

        # Windows 顯示縮放（125% / 150%）也納入實體像素計算，避免 Qt 再放大
        # 一張低解析度 pixmap。另用 2x 超取樣降低文字與斜線鋸齒。
        try:
            dpr = max(1.0, float(self.scroll.viewport().devicePixelRatioF()))
        except Exception:
            dpr = 1.0

        # 一般閱讀倍率使用完整 2x 超取樣；倍率很高時本身已有足夠實體像素，
        # 適度降低超取樣可避免 300%~400% 時建立過大的中間影像。
        if self.zoom <= 2.0:
            oversample = RENDER_OVERSAMPLE
        elif self.zoom <= 3.0:
            oversample = 1.5
        else:
            oversample = 1.25
        render_scale = self.zoom * dpr * oversample
        matrix = fitz.Matrix(render_scale, render_scale)
        pix = page.get_pixmap(matrix=matrix, alpha=False, annots=True)
        fmt = QImage.Format_RGB888 if pix.n == 3 else QImage.Format_RGBA8888
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt).copy()
        qpix = QPixmap.fromImage(image)

        # 超取樣圖先縮到螢幕真正需要的實體像素，再設定 DPR。
        physical_w = max(1, int(round(logical_w * dpr)))
        physical_h = max(1, int(round(logical_h * dpr)))
        if qpix.width() != physical_w or qpix.height() != physical_h:
            qpix = qpix.scaled(
                physical_w,
                physical_h,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )
        qpix.setDevicePixelRatio(dpr)

        label.setPixmap(qpix)
        label.setFixedSize(logical_w, logical_h)
        label.set_display_scale(self.zoom)
        self.rendered_pages.add(page_index)

    def render_visible_pages(self):
        """Render only nearby pages and release distant rendered pixmaps."""
        if self.doc is None or not self.page_labels:
            return

        try:
            visible = set(self._nearby_page_indices())
            if not visible:
                visible = {0}

            for page_index in sorted(visible):
                if page_index not in self.rendered_pages:
                    self._render_page_high_quality(page_index)

            # Iterate only pages that actually own a pixmap. This keeps scroll
            # work proportional to the small render cache, not total PDF pages.
            near = set(self._nearby_page_indices(VISIBLE_PAGE_BUFFER * 3))
            for page_index in tuple(self.rendered_pages - near):
                label = self.page_labels[page_index]
                if label.pixmap() is not None:
                    label.clear()
                    label.setText(f"第 {page_index + 1} 頁")
                self.rendered_pages.discard(page_index)
        except Exception as e:
            self._set_status(f"預覽渲染失敗：{e}")

    def pan_view(self, dx: int, dy: int):
        hbar = self.scroll.horizontalScrollBar()
        vbar = self.scroll.verticalScrollBar()
        hbar.setValue(hbar.value() - dx)
        vbar.setValue(vbar.value() - dy)

    def change_zoom(self, delta: float):
        if self.doc is None:
            return
        new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, self.zoom + delta))
        if abs(new_zoom - self.zoom) < 0.001:
            return

        # 快速 Ctrl+滾輪時只更新頁面尺寸；高解析度 rasterize 延後到滾動停止。
        # 因此不會再每個 wheel event 都把所有頁面重新做一次縮圖。
        hbar = self.scroll.horizontalScrollBar()
        vbar = self.scroll.verticalScrollBar()
        h_ratio = hbar.value() / max(1, hbar.maximum())
        v_ratio = vbar.value() / max(1, vbar.maximum())

        self.zoom = new_zoom
        self.rendered_pages.clear()
        self._ensure_page_labels()
        self._update_controls()

        # 幾何尺寸變更後維持原本閱讀位置的相對比例。
        hbar.setValue(int(h_ratio * hbar.maximum()))
        vbar.setValue(int(v_ratio * vbar.maximum()))
        self._update_current_page_label()
        self.schedule_visible_render(ZOOM_RENDER_DEBOUNCE_MS)
        self._set_status(
            f"縮放：{int(round(self.zoom * 100))}%｜停止縮放後更新高解析度頁面"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, "_render_timer"):
            self._update_current_page_label()
            self.schedule_visible_render(SCROLL_RENDER_DEBOUNCE_MS)

    # ---------- 標記設定 ----------
    def choose_color(self):
        """相容舊呼叫：修改目前選中的色塊。"""
        self.choose_palette_color(self.active_color_index)

    def _fitz_rgb(self) -> Tuple[float, float, float]:
        return (
            self.current_color.red() / 255.0,
            self.current_color.green() / 255.0,
            self.current_color.blue() / 255.0,
        )

    def _keyword(self) -> Optional[str]:
        keyword = self.search_edit.text().strip()
        if not keyword:
            self._set_status("請先輸入搜尋關鍵字")
            self.search_edit.setFocus()
            return None
        return keyword

    # ---------- Undo / Redo（各最多 10 次） ----------
    @staticmethod
    def _delete_history_entry_file(entry: dict):
        if entry.get("kind") == "snapshot":
            try:
                Path(entry.get("path", "")).unlink(missing_ok=True)
            except Exception:
                pass

    def _clear_redo_stack(self):
        for entry in getattr(self, "redo_stack", []):
            self._delete_history_entry_file(entry)
        if hasattr(self, "redo_stack"):
            self.redo_stack.clear()
        self._remove_history_temp_dir_if_unused()
        if hasattr(self, "redo_action"):
            self._update_controls()

    def _clear_undo_stack(self):
        for entry in getattr(self, "undo_stack", []):
            self._delete_history_entry_file(entry)
        if hasattr(self, "undo_stack"):
            self.undo_stack.clear()
        # 開檔、正式儲存或歷史失效時，Undo / Redo 都必須回到同一基準。
        self._clear_redo_stack()
        self._remove_history_temp_dir_if_unused()
        self._update_controls() if hasattr(self, "undo_action") else None

    def _history_has_snapshot_entries(self) -> bool:
        for stack_name in ("undo_stack", "redo_stack"):
            for entry in getattr(self, stack_name, []):
                if entry.get("kind") == "snapshot":
                    return True
        return False

    def _remove_history_temp_dir_if_unused(self):
        if getattr(self, "undo_temp_dir", None) is None or self._history_has_snapshot_entries():
            return
        try:
            shutil.rmtree(self.undo_temp_dir, ignore_errors=True)
        finally:
            self.undo_temp_dir = None

    def _trim_history_stack(self, stack: list[dict]):
        while len(stack) > UNDO_LIMIT:
            old = stack.pop(0)
            self._delete_history_entry_file(old)
        self._remove_history_temp_dir_if_unused()

    def _push_undo_entry(self, entry: dict, *, clear_redo: bool = True):
        self.undo_stack.append(entry)
        self._trim_history_stack(self.undo_stack)
        # 只要使用者在 Undo 之後做了新的編輯，舊 Redo 分支就不再有效。
        if clear_redo and not self._history_replaying:
            self._clear_redo_stack()
        self._update_controls()

    def _push_redo_entry(self, entry: dict):
        self.redo_stack.append(entry)
        self._trim_history_stack(self.redo_stack)
        self._update_controls()

    def _snapshot_entry(self, action_name: str, prefix: str = "history") -> dict:
        """把目前 PDF 狀態存成磁碟快照並回傳 history entry。"""
        if self.doc is None:
            raise RuntimeError("目前沒有可建立歷史快照的 PDF")
        if self.undo_temp_dir is None:
            self.undo_temp_dir = Path(tempfile.mkdtemp(prefix="PdectUndo_"))
        snap = self.undo_temp_dir / f"{prefix}_{uuid.uuid4().hex}.pdf"
        self.doc.save(str(snap), garbage=0, clean=False, deflate=False, use_objstms=0)
        return {"kind":"snapshot", "path":str(snap), "name":action_name}

    def _capture_undo_state(self, action_name: str):
        """破壞性操作使用磁碟 PDF 快照，避免 10 份完整 PDF 全塞進 RAM。"""
        if self.doc is None:
            return
        self._push_undo_entry(self._snapshot_entry(action_name, "undo"))

    def _set_added_annotations_undo(
        self, action_name: str, refs: list[tuple[int, int]],
        content_refs: Optional[list[tuple[int, int]]] = None,
    ):
        """新增標記專用輕量 Undo；圖說另記錄其頁面內容串流。"""
        if refs or content_refs:
            self._push_undo_entry({
                "kind":"add", "refs":list(refs),
                "content_refs":list(content_refs or []), "name":action_name,
            })

    def _load_history_snapshot(self, entry: dict):
        path = Path(entry.get("path", ""))
        data = path.read_bytes()
        old_doc = self.doc
        self.doc = fitz.open(stream=data, filetype="pdf")
        if old_doc is not None:
            old_doc.close()
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass
        self.dirty = True
        self._clear_selection(update_view=False)
        self._refresh_bookmark_combo()
        self.render_all_pages(preserve_scroll=True)

    def undo_last_action(self):
        if not self.undo_stack:
            self._set_status("目前沒有可回復的動作")
            return

        entry = self.undo_stack.pop()
        redo_entry = None
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._history_replaying = True
        try:
            action_name = entry.get("name", "動作")
            # Undo 前先保存「目前狀態」，供 Ctrl+Y 完整做回去。
            redo_entry = self._snapshot_entry(action_name, "redo")

            if entry.get("kind") == "add":
                touched_pages = set()
                streams_by_page = {}
                for page_index, xref in entry.get("content_refs", []):
                    streams_by_page.setdefault(int(page_index), []).append(int(xref))
                for page_index, stream_xrefs in streams_by_page.items():
                    try:
                        page = self.doc[page_index]
                        self._remove_page_content_streams(page, stream_xrefs)
                        touched_pages.add(page_index)
                    except Exception:
                        pass
                for page_index, xref in reversed(entry.get("refs", [])):
                    try:
                        page = self.doc[page_index]
                        annot = page.load_annot(xref)
                        if annot is not None:
                            page.delete_annot(annot)
                            touched_pages.add(page_index)
                    except Exception:
                        pass
                self.dirty = True
                self._clear_selection(update_view=False)
                self._refresh_annotation_pages(touched_pages)
            else:
                self._load_history_snapshot(entry)

            self._push_redo_entry(redo_entry)
            redo_entry = None
            self._set_status(
                f"已回復：{action_name}｜可復原 {len(self.undo_stack)} 次｜可重做 {len(self.redo_stack)} 次"
            )
        except Exception as e:
            # 失敗時把 entry 放回，並清掉未使用的 redo 快照。
            self.undo_stack.append(entry)
            if redo_entry is not None:
                self._delete_history_entry_file(redo_entry)
            self._set_status(f"回復失敗：{e}")
            QMessageBox.critical(self, "回復失敗", f"無法回復上一次動作：\n{e}")
        finally:
            self._history_replaying = False
            QApplication.restoreOverrideCursor()
            self._update_controls()

    def redo_last_action(self):
        if not self.redo_stack:
            self._set_status("目前沒有可重做的動作")
            return

        entry = self.redo_stack.pop()
        undo_entry = None
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._history_replaying = True
        try:
            action_name = entry.get("name", "動作")
            # Redo 前保存目前（Undo 後）狀態，讓 Ctrl+Z 可以再次復原 Redo。
            undo_entry = self._snapshot_entry(action_name, "undo_redo")
            self._load_history_snapshot(entry)
            self._push_undo_entry(undo_entry, clear_redo=False)
            undo_entry = None
            self._set_status(
                f"已重做：{action_name}｜可復原 {len(self.undo_stack)} 次｜可重做 {len(self.redo_stack)} 次"
            )
        except Exception as e:
            self.redo_stack.append(entry)
            if undo_entry is not None:
                self._delete_history_entry_file(undo_entry)
            self._set_status(f"重做失敗：{e}")
            QMessageBox.critical(self, "重做失敗", f"無法回復後一次動作：\n{e}")
        finally:
            self._history_replaying = False
            QApplication.restoreOverrideCursor()
            self._update_controls()

    # ---------- 搜尋與標記 ----------
    @staticmethod
    def _rects_overlap(a: fitz.Rect, b: fitz.Rect, margin: float = 0.8) -> bool:
        """判斷兩區域是否重疊；加入微小容差，避免細線剛好壓在文字邊界時漏判。"""
        aa = fitz.Rect(a.x0 - margin, a.y0 - margin, a.x1 + margin, a.y1 + margin)
        bb = fitz.Rect(b.x0 - margin, b.y0 - margin, b.x1 + margin, b.y1 + margin)
        return not (aa.x1 < bb.x0 or aa.x0 > bb.x1 or aa.y1 < bb.y0 or aa.y0 > bb.y1)

    @staticmethod
    def _annotation_counts_as_existing_mark(annot) -> bool:
        """只把可能蓋在文字上的醒目 / 線條類註記視為既有標記。"""
        try:
            type_name = str(annot.type[1]).strip().lower()
        except Exception:
            type_name = ""

        # PyMuPDF 常見文字標記：Highlight / Underline / StrikeOut / Squiggly
        # 以及可能覆蓋文字的 Square / Line / Ink / PolyLine / Polygon / Redact。
        mark_types = {
            "highlight",
            "underline",
            "strikeout",
            "squiggly",
            "square",
            "line",
            "ink",
            "polyline",
            "polygon",
            "redact",
        }
        return type_name in mark_types

    def _build_existing_mark_index(self, page):
        """
        每頁只掃一次 Annotation，並依 72pt 網格建立空間索引。
        舊版是每一個搜尋命中都重新掃完整 annotation chain；大量頁面 / 大量標記時會非常慢。
        """
        grid: dict[tuple[int, int], list[fitz.Rect]] = {}
        annot = page.first_annot
        while annot:
            try:
                if self._annotation_counts_as_existing_mark(annot):
                    r = fitz.Rect(annot.rect)
                    try:
                        border = annot.border or {}
                        width = float(border.get("width", 0) or 0)
                    except Exception:
                        width = 0.0
                    expand = max(0.8, width / 2.0)
                    r = fitz.Rect(r.x0 - expand, r.y0 - expand, r.x1 + expand, r.y1 + expand)

                    x0 = int(r.x0 // EXISTING_MARK_GRID)
                    x1 = int(r.x1 // EXISTING_MARK_GRID)
                    y0 = int(r.y0 // EXISTING_MARK_GRID)
                    y1 = int(r.y1 // EXISTING_MARK_GRID)
                    for gx in range(x0, x1 + 1):
                        for gy in range(y0, y1 + 1):
                            grid.setdefault((gx, gy), []).append(r)
            except Exception:
                pass
            annot = annot.next
        return grid

    def _quad_has_existing_mark_indexed(self, quad, grid) -> bool:
        hit = fitz.Rect(quad.rect)
        margin = 0.8
        expanded = fitz.Rect(hit.x0 - margin, hit.y0 - margin, hit.x1 + margin, hit.y1 + margin)
        x0 = int(expanded.x0 // EXISTING_MARK_GRID)
        x1 = int(expanded.x1 // EXISTING_MARK_GRID)
        y0 = int(expanded.y0 // EXISTING_MARK_GRID)
        y1 = int(expanded.y1 // EXISTING_MARK_GRID)

        seen = set()
        for gx in range(x0, x1 + 1):
            for gy in range(y0, y1 + 1):
                for r in grid.get((gx, gy), ()):
                    # 同一 rect 可能存在多個相鄰網格，避免重複比較。
                    key = (r.x0, r.y0, r.x1, r.y1)
                    if key in seen:
                        continue
                    seen.add(key)
                    if self._rects_overlap(hit, r):
                        return True
        return False

    def _find_all_quads(self, keyword: str):
        matches = []
        skipped = 0
        start_page_index = max(0, min(len(self.doc) - 1, self.start_page_spin.value() - 1))
        skip_existing = self.skip_existing_check.isChecked()

        for page_index in range(start_page_index, len(self.doc)):
            page = self.doc[page_index]
            quads = page.search_for(keyword, quads=True)
            if skip_existing and quads:
                mark_index = self._build_existing_mark_index(page)
                if mark_index:
                    filtered = []
                    for quad in quads:
                        if self._quad_has_existing_mark_indexed(quad, mark_index):
                            skipped += 1
                        else:
                            filtered.append(quad)
                    quads = filtered
            if quads:
                matches.append((page_index, quads))
        return matches, skipped

    def mark_highlight(self):
        if self.doc is None:
            return
        keyword = self._keyword()
        if keyword is None:
            return

        start_page = self.start_page_spin.value()
        self._set_status(f"正在搜尋並建立螢光筆標記：第 {start_page} 頁起｜「{keyword}」…")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            matches, skipped = self._find_all_quads(keyword)
            count = sum(len(quads) for _, quads in matches)
            start_page = self.start_page_spin.value()
            if not count:
                if skipped:
                    self._set_status(
                        f"第 {start_page} 頁起找到的「{keyword}」都已位於既有標記區域，共略過 {skipped} 處"
                    )
                else:
                    self._set_status(f"從第 {start_page} 頁起找不到關鍵字：「{keyword}」")
                return

            color = self._fitz_rgb()
            opacity = self.opacity_spin.value() / 100.0
            added_refs: list[tuple[int, int]] = []
            touched_pages = set()

            for page_index, quads in matches:
                page = self.doc[page_index]
                touched_pages.add(page_index)
                for quad in quads:
                    annot = page.add_highlight_annot(quad)
                    annot.set_colors(stroke=color)
                    annot.set_opacity(opacity)
                    annot.update()
                    added_refs.append((page_index, annot.xref))

            self._set_added_annotations_undo(f"螢光筆標記「{keyword}」", added_refs)
            self.dirty = True
            self._clear_selection(update_view=False)
            self._refresh_annotation_pages(touched_pages)
            self._set_status(
                f"螢光筆完成：第 {start_page} 頁起「{keyword}」共標記 {count} 處"
                f"｜透明度 {self.opacity_spin.value()}%"
                + (f"｜略過既有標記 {skipped} 處" if skipped else "")
            )
        except Exception as e:
            self._set_status(f"螢光筆失敗：{e}")
            QMessageBox.critical(self, "螢光筆失敗", f"搜尋或標記時發生錯誤：\n{e}")
        finally:
            QApplication.restoreOverrideCursor()
            self._update_controls()

    def mark_strikeout(self):
        if self.doc is None:
            return
        keyword = self._keyword()
        if keyword is None:
            return

        start_page = self.start_page_spin.value()
        self._set_status(f"正在搜尋並建立刪除線：第 {start_page} 頁起｜「{keyword}」…")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            matches, skipped = self._find_all_quads(keyword)
            count = sum(len(quads) for _, quads in matches)
            start_page = self.start_page_spin.value()
            if not count:
                if skipped:
                    self._set_status(
                        f"第 {start_page} 頁起找到的「{keyword}」都已位於既有標記區域，共略過 {skipped} 處"
                    )
                else:
                    self._set_status(f"從第 {start_page} 頁起找不到關鍵字：「{keyword}」")
                return

            color = self._fitz_rgb()
            width = float(self.strike_width_spin.value())
            added_refs: list[tuple[int, int]] = []
            touched_pages = set()

            # 使用 Line Annotation 沿文字中線繪製，確保「刪除線寬度」可精確控制。
            # quads=True 可同時處理旋轉文字。
            for page_index, quads in matches:
                page = self.doc[page_index]
                touched_pages.add(page_index)
                for quad in quads:
                    left_mid = fitz.Point(
                        (quad.ul.x + quad.ll.x) / 2.0,
                        (quad.ul.y + quad.ll.y) / 2.0,
                    )
                    right_mid = fitz.Point(
                        (quad.ur.x + quad.lr.x) / 2.0,
                        (quad.ur.y + quad.lr.y) / 2.0,
                    )
                    annot = page.add_line_annot(left_mid, right_mid)
                    annot.set_colors(stroke=color)
                    annot.set_border(width=width)
                    annot.set_opacity(1.0)  # 依需求固定 100%
                    annot.update()
                    added_refs.append((page_index, annot.xref))

            self._set_added_annotations_undo(f"刪除線標記「{keyword}」", added_refs)
            self.dirty = True
            self._clear_selection(update_view=False)
            self._refresh_annotation_pages(touched_pages)
            self._set_status(
                f"刪除線完成：第 {start_page} 頁起「{keyword}」共標記 {count} 處"
                f"｜寬度 {width:g} pt｜不透明度 100%"
                + (f"｜略過既有標記 {skipped} 處" if skipped else "")
            )
        except Exception as e:
            self._set_status(f"刪除線失敗：{e}")
            QMessageBox.critical(self, "刪除線失敗", f"搜尋或標記時發生錯誤：\n{e}")
        finally:
            QApplication.restoreOverrideCursor()
            self._update_controls()

    # ---------- 手繪線 ----------
    def add_manual_line(self, page_index: int, x0: float, y0: float, x1: float, y1: float, mode: str):
        if self.doc is None or not (0 <= page_index < len(self.doc)):
            return
        if mode not in ("highlight", "strike", "strike_diag"):
            return

        page = self.doc[page_index]
        rect = page.rect

        if mode in ("highlight", "strike"):
            left = max(rect.x0, min(rect.x1, min(x0, x1)))
            right = max(rect.x0, min(rect.x1, max(x0, x1)))
            yy = max(rect.y0, min(rect.y1, y0))
            p0 = fitz.Point(left, yy)
            p1 = fitz.Point(right, yy)
        else:
            # strike_diag：強制左上 -> 右下；角度不限。
            left = max(rect.x0, min(rect.x1, min(x0, x1)))
            right = max(rect.x0, min(rect.x1, max(x0, x1)))
            top = max(rect.y0, min(rect.y1, min(y0, y1)))
            bottom = max(rect.y0, min(rect.y1, max(y0, y1)))
            p0 = fitz.Point(left, top)
            p1 = fitz.Point(right, bottom)

        dx = float(p1.x - p0.x)
        dy = float(p1.y - p0.y)
        if (dx * dx + dy * dy) ** 0.5 < 1.0:
            return

        try:
            color = self._fitz_rgb()
            annot = page.add_line_annot(p0, p1)
            annot.set_colors(stroke=color)

            if mode == "highlight":
                annot.set_border(width=HAND_HIGHLIGHT_WIDTH)
                annot.set_opacity(self.opacity_spin.value() / 100.0)
                action_name = f"手繪螢光線（第 {page_index + 1} 頁）"
            elif mode == "strike":
                width = float(self.strike_width_spin.value())
                annot.set_border(width=width)
                annot.set_opacity(1.0)
                action_name = f"手繪刪除線（第 {page_index + 1} 頁）"
            else:
                width = float(self.strike_width_spin.value())
                annot.set_border(width=width)
                annot.set_opacity(1.0)
                action_name = f"斜線刪除線（第 {page_index + 1} 頁）"

            annot.update()
            self._set_added_annotations_undo(action_name, [(page_index, annot.xref)])
            self.dirty = True
            self._clear_selection(update_view=False)
            self._refresh_annotation_pages([page_index])

            if mode == "highlight":
                self._set_status(
                    f"已新增手繪螢光線：第 {page_index + 1} 頁｜水平｜透明度 {self.opacity_spin.value()}%"
                )
            elif mode == "strike":
                self._set_status(
                    f"已新增手繪刪除線：第 {page_index + 1} 頁｜水平｜寬度 {self.strike_width_spin.value():g} pt｜不透明度 100%"
                )
            else:
                self._set_status(
                    f"已新增斜線刪除線：第 {page_index + 1} 頁｜左上→右下｜寬度 {self.strike_width_spin.value():g} pt｜不透明度 100%"
                )
        except Exception as e:
            self._set_status(f"手繪失敗：{e}")
            QMessageBox.critical(self, "手繪失敗", f"無法建立手繪線：\n{e}")
        finally:
            self._update_controls()

    def _bounded_page_rect(self, page_index: int, x0: float, y0: float, x1: float, y1: float):
        page_rect = self.doc[page_index].rect
        rect = fitz.Rect(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)) & page_rect
        if rect.is_empty or rect.width < 0.5 or rect.height < 0.5:
            return None
        return rect

    @staticmethod
    def _join_selected_words(words) -> str:
        if not words:
            return ""
        lines: list[str] = []
        current_key = None
        current_words: list[str] = []
        for word in words:
            text = str(word[4]).strip() if len(word) >= 5 else ""
            if not text:
                continue
            key = (int(word[5]), int(word[6])) if len(word) >= 7 else (0, round(float(word[1]) / 4.0))
            if current_key is not None and key != current_key:
                lines.append(" ".join(current_words))
                current_words = []
            current_key = key
            current_words.append(text)
        if current_words:
            lines.append(" ".join(current_words))
        return "\n".join(line for line in lines if line.strip()).strip()

    def select_text_in_rect(self, page_index: int, x0: float, y0: float, x1: float, y1: float):
        if self.doc is None or not (0 <= page_index < len(self.doc)):
            return
        rect = self._bounded_page_rect(page_index, x0, y0, x1, y1)
        if rect is None:
            self._set_status("選擇文字：框選範圍太小")
            return
        try:
            page = self.doc[page_index]
            try:
                text = self._join_selected_words(page.get_text("words", clip=rect, sort=True))
            except TypeError:
                text = self._join_selected_words(page.get_text("words", clip=rect))
            if not text:
                try:
                    text = page.get_text("text", clip=rect).strip()
                except Exception:
                    text = ""
            if not text:
                self._set_status(f"選擇文字：第 {page_index + 1} 頁框選範圍內沒有可複製文字")
                return
            QApplication.clipboard().setText(text)
            preview = text.replace("\n", " ")
            if len(preview) > 42:
                preview = preview[:42] + "..."
            self._set_status(f"已複製文字：第 {page_index + 1} 頁｜{preview}")
        except Exception as e:
            self._set_status(f"選擇文字失敗：{e}")
            QMessageBox.critical(self, "選擇文字失敗", f"無法複製框選文字：\n{e}")

    def add_square_annotation(self, page_index: int, x0: float, y0: float, x1: float, y1: float):
        if self.doc is None or not (0 <= page_index < len(self.doc)):
            return
        rect = self._bounded_page_rect(page_index, x0, y0, x1, y1)
        if rect is None or rect.width < 2.0 or rect.height < 2.0:
            self._set_status("方框：框選範圍太小，未建立註記")
            return
        try:
            page = self.doc[page_index]
            color = self._fitz_rgb()
            width = float(self.strike_width_spin.value())
            annot = page.add_rect_annot(rect)
            try:
                annot.set_colors(stroke=color, fill=None)
            except TypeError:
                annot.set_colors(stroke=color)
            annot.set_border(width=width)
            annot.set_opacity(1.0)
            annot.update()
            self._set_added_annotations_undo(f"新增方框（第 {page_index + 1} 頁）", [(page_index, annot.xref)])
            self.dirty = True
            self._clear_selection(update_view=False)
            self._refresh_annotation_pages([page_index])
            self._set_status(
                f"已新增方框：第 {page_index + 1} 頁｜框線 {self.current_color.name().upper()}｜寬度 {width:g} pt｜內部透明"
            )
        except Exception as e:
            self._set_status(f"新增方框失敗：{e}")
            QMessageBox.critical(self, "新增方框失敗", f"無法建立方框註記：\n{e}")
        finally:
            self._update_controls()

    # ---------- 圖說文字 / 方框 / 可延伸箭頭 ----------
    @staticmethod
    def _callout_attach_point(box: fitz.Rect, arrow: fitz.Point) -> fitz.Point:
        """把 callout 起點吸附到距箭頭最近的方框邊緣。"""
        cx = max(box.x0, min(box.x1, arrow.x)); cy = max(box.y0, min(box.y1, arrow.y))
        candidates = [
            (abs(arrow.x-box.x0), fitz.Point(box.x0, cy)),
            (abs(arrow.x-box.x1), fitz.Point(box.x1, cy)),
            (abs(arrow.y-box.y0), fitz.Point(cx, box.y0)),
            (abs(arrow.y-box.y1), fitz.Point(cx, box.y1)),
        ]
        return min(candidates, key=lambda t:t[0])[1]

    @staticmethod
    def _callout_font_path() -> Path:
        """Locate the real DFKai-SB font file used for PDF embedding."""
        env_path = os.environ.get(PDECT_KAIU_FONT_ENV, "").strip().strip('"')
        windir = Path(os.environ.get("WINDIR", r"C:\Windows"))
        candidates = []
        if env_path:
            candidates.append(Path(env_path).expanduser())
        candidates.extend([windir / "Fonts" / "kaiu.ttf", Path(r"C:\Windows\Fonts\kaiu.ttf")])
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        tried = "\n".join(f"- {candidate}" for candidate in candidates)
        raise FileNotFoundError(
            "找不到圖說需要的標楷體字型檔 kaiu.ttf。\n\n"
            f"已檢查：\n{tried}\n\n"
            f"Windows 請確認 C:\\Windows\\Fonts\\kaiu.ttf 存在；其他平台可設定 {PDECT_KAIU_FONT_ENV} "
            "指向合法的本機 kaiu.ttf。請不要把字型檔加入 repo 或交付包。"
        )

    @staticmethod
    def _callout_meta_subject(
        box, arrow, fontsize, shade, group_id, part,
        streams=None, render_fontsize=None, font_resource=None,
    ):
        payload = {
            "box":[box.x0,box.y0,box.x1,box.y1], "arrow":[arrow.x,arrow.y],
            "fs":float(fontsize), "shade":int(shade), "group":str(group_id), "part":str(part)
        }
        if streams:
            payload["streams"] = [int(xref) for xref in streams]
        if render_fontsize is not None:
            payload["rfs"] = float(render_fontsize)
        if font_resource:
            payload["font"] = str(font_resource)
        return CALLOUT_SUBJECT_PREFIX + json.dumps(payload, ensure_ascii=False, separators=(",",":"))

    @staticmethod
    def _parse_callout_meta(annot):
        try:
            subj = annot.info.get("subject", "")
            if not subj.startswith(CALLOUT_SUBJECT_PREFIX): return None
            data = json.loads(subj[len(CALLOUT_SUBJECT_PREFIX):])
            box = fitz.Rect(*data["box"]); arrow = fitz.Point(*data["arrow"])
            fs = float(data.get("fs", CALLOUT_DEFAULT_FONT_SIZE)); shade = int(data.get("shade", 1))
            streams = []
            for value in data.get("streams", []):
                try:
                    xref = int(value)
                    if xref > 0 and xref not in streams:
                        streams.append(xref)
                except (TypeError, ValueError):
                    pass
            return {
                "box":box, "arrow":arrow, "fs":fs,
                "rfs":float(data.get("rfs", fs)),
                "shade":max(0,min(len(CALLOUT_FILL_SHADES)-1,shade)),
                "group":str(data.get("group", "")), "part":str(data.get("part", "")),
                "streams":streams, "font":str(data.get("font", "")),
            }
        except Exception:
            return None

    @staticmethod
    def _callout_text(annot):
        try:
            txt = annot.info.get("content", "")
            if txt: return txt
            return annot.get_text().strip()
        except Exception:
            return ""

    def _callout_group_parts(self, page, group_id: str):
        parts=[]; a=page.first_annot
        while a:
            try:
                m=self._parse_callout_meta(a)
                if m is not None and m.get("group")==group_id:
                    parts.append((a,m))
            except Exception:
                pass
            a=a.next
        return parts

    def _remove_page_content_streams(self, page, stream_xrefs) -> list[int]:
        """Detach only Pdect-owned content streams from a page /Contents array."""
        remove = {int(xref) for xref in stream_xrefs if int(xref) > 0}
        existing = [int(xref) for xref in page.get_contents()]
        kept = [xref for xref in existing if xref not in remove]
        removed = [xref for xref in existing if xref in remove]
        if not removed:
            return []
        value = "[" + " ".join(f"{xref} 0 R" for xref in kept) + "]" if kept else "null"
        self.doc.xref_set_key(page.xref, "Contents", value)
        return removed

    def _callout_stream_xrefs(self, page, meta) -> list[int]:
        """Resolve owned streams after save-time xref renumbering via a stable marker."""
        page_streams = [int(xref) for xref in page.get_contents()]
        found=[]
        group_id = str(meta.get("group", ""))
        marker = (f"% PdectCallout-{group_id}\n").encode("ascii") if group_id else b""
        if marker:
            for xref in page_streams:
                try:
                    if self.doc.xref_stream(xref).startswith(marker):
                        found.append(xref)
                except Exception:
                    pass
        else:
            found = [int(xref) for xref in meta.get("streams", []) if int(xref) in page_streams]
        return found

    def _delete_callout_parts(self, page, parts) -> list[int]:
        """Delete a Pdect callout's annotations and its owned vector content."""
        streams=[]; xrefs=[]
        for annot, meta in parts:
            xrefs.append(annot.xref)
            for stream_xref in self._callout_stream_xrefs(page, meta):
                if stream_xref not in streams:
                    streams.append(stream_xref)
        removed = self._remove_page_content_streams(page, streams)
        for xref in xrefs:
            try:
                annot = page.load_annot(xref)
                if annot is not None:
                    page.delete_annot(annot)
            except Exception:
                pass
        return removed

    @staticmethod
    def _callout_text_rect(box: fitz.Rect) -> fitz.Rect:
        """圖說文字距方框左、上各 2 px。"""
        b = fitz.Rect(box)
        margin = CALLOUT_TEXT_MARGIN_PT
        x0 = min(b.x1, b.x0 + margin)
        y0 = min(b.y1, b.y0 + margin)
        return fitz.Rect(x0, y0, b.x1, b.y1)

    def _insert_callout_content(self, page, box, text, fontsize, shade, group_id):
        """Insert lossless vector background and DFKai-SB text as owned streams."""
        font_path = self._callout_font_path()
        resource = self.callout_font_resource
        page.insert_font(fontname=resource, fontfile=str(font_path), set_simple=False)

        text_rect = self._callout_text_rect(box)
        requested = max(CALLOUT_MIN_FONT_SIZE, min(CALLOUT_MAX_FONT_SIZE, float(fontsize)))
        minimum = max(CALLOUT_MIN_FONT_SIZE, requested * CALLOUT_MIN_RENDER_SCALE)
        render_size = requested
        shape = None
        spare_height = -1.0
        while render_size + 1e-6 >= minimum:
            candidate = page.new_shape()
            spare_height = candidate.insert_textbox(
                text_rect, text, fontsize=render_size,
                fontname=resource, fontfile=str(font_path),
                color=(0,0,0), lineheight=1.0,
            )
            if spare_height >= 0:
                shape = candidate
                break
            render_size -= 0.5
        if shape is None:
            raise ValueError("圖說文字無法放入方框，請放大方框或縮小字體")

        before = set(page.get_contents())
        try:
            page.draw_rect(box, color=None, fill=CALLOUT_FILL_SHADES[shade], width=0, overlay=True)
            shape.commit(overlay=True)
            streams = [xref for xref in page.get_contents() if xref not in before]
            if not streams:
                raise RuntimeError("圖說文字內容串流建立失敗")
            marker = f"% PdectCallout-{group_id}\n".encode("ascii")
            for xref in streams:
                data = self.doc.xref_stream(xref)
                if not data.startswith(marker):
                    self.doc.update_stream(xref, marker + data)
        except Exception:
            created = [xref for xref in page.get_contents() if xref not in before]
            self._remove_page_content_streams(page, created)
            raise
        self._callout_font_needs_subset = True
        return streams, render_size

    def _create_callout_group(self, page, box: fitz.Rect, arrow: fitz.Point, text: str, fontsize: float, shade: int, group_id: str|None=None):
        """以向量內容 + Rect / Line annotations 建立可編輯且不破字的圖說。"""
        shade=max(0,min(len(CALLOUT_FILL_SHADES)-1,int(shade)))
        fontsize=max(CALLOUT_MIN_FONT_SIZE,min(CALLOUT_MAX_FONT_SIZE,float(fontsize)))
        box=fitz.Rect(box); arrow=fitz.Point(arrow); group_id=group_id or uuid.uuid4().hex
        attach=self._callout_attach_point(box,arrow)
        streams, render_size = self._insert_callout_content(page, box, text, fontsize, shade, group_id)
        refs=[]
        try:
            # 紅框保留為 Annotation；底色與文字位於其下方的向量內容層。
            recta=page.add_rect_annot(box)
            recta.set_border(width=CALLOUT_BORDER_WIDTH)
            recta.set_colors(stroke=(1,0,0), fill=None)
            recta.set_opacity(1.0); recta.update()
            recta.set_info(
                content=text,
                subject=self._callout_meta_subject(
                    box,arrow,fontsize,shade,group_id,"box",streams,render_size,self.callout_font_resource
                ),
                title=f"{APP_TITLE} 圖說",
            )
            refs.append((page.number, recta.xref))

            # 紅色可延伸實心箭頭。
            linea=page.add_line_annot(attach,arrow)
            linea.set_border(width=CALLOUT_BORDER_WIDTH)
            linea.set_colors(stroke=(1,0,0), fill=(1,0,0))
            linea.set_line_ends(fitz.PDF_ANNOT_LE_NONE, fitz.PDF_ANNOT_LE_CLOSED_ARROW)
            linea.set_opacity(1.0); linea.update()
            linea.set_info(
                content=text,
                subject=self._callout_meta_subject(
                    box,arrow,fontsize,shade,group_id,"arrow",streams,render_size,self.callout_font_resource
                ),
                title=f"{APP_TITLE} 圖說",
            )
            refs.append((page.number, linea.xref))
            return recta, refs, group_id, [(page.number, xref) for xref in streams]
        except Exception:
            self._remove_page_content_streams(page, streams)
            for _page_index, xref in reversed(refs):
                try:
                    annot = page.load_annot(xref)
                    if annot is not None:
                        page.delete_annot(annot)
                except Exception:
                    pass
            raise
    def add_callout(self, page_index: int, x0: float, y0: float, x1: float, y1: float):
        if self.doc is None or not (0 <= page_index < len(self.doc)): return
        text, ok = QInputDialog.getMultiLineText(self, "新增圖說", "圖說文字：", "")
        if not ok or not text.strip():
            self._set_status("已取消新增圖說"); return
        page = self.doc[page_index]; pr = page.rect
        box = fitz.Rect(max(pr.x0,min(x0,x1)), max(pr.y0,min(y0,y1)), min(pr.x1,max(x0,x1)), min(pr.y1,max(y0,y1)))
        if box.width < 20 or box.height < 14: return
        arrow_x = max(pr.x0+4, box.x0-70)
        arrow = fitz.Point(arrow_x, box.y0 + box.height/2)
        try:
            annot, refs, _group, content_refs = self._create_callout_group(page, box, arrow, text.strip(), CALLOUT_DEFAULT_FONT_SIZE, 1)
            self._set_added_annotations_undo(f"新增圖說（第 {page_index+1} 頁）", refs, content_refs)
            self.dirty=True; self._refresh_annotation_pages([page_index])
            self._select_annotation_object(page_index, annot)
            self.set_manual_draw_mode(None)
            self._set_status(f"圖說已新增：第 {page_index+1} 頁｜標楷體設定 {CALLOUT_DEFAULT_FONT_SIZE:g} pt｜紅框｜淺米黃色底色")
        except Exception as e:
            self._set_status(f"新增圖說失敗：{e}"); QMessageBox.critical(self,"圖說失敗",f"無法建立圖說：\n{e}")

    def _replace_selected_callout(self, *, box=None, arrow=None, fontsize=None, shade=None, new_text=None, action_name="修改圖說"):
        if self.doc is None or self.selected_page_index is None or self.selected_annot_xref is None: return
        page_index=self.selected_page_index; page=self.doc[page_index]
        try: annot=page.load_annot(self.selected_annot_xref)
        except Exception: annot=None
        if annot is None: return
        meta=self._parse_callout_meta(annot)
        if meta is None:
            self._set_status("此註記不是 Pdect 圖說，無法使用圖說調整控制"); return
        group_id=meta.get("group", "")
        if group_id:
            self.selected_callout_group_id = group_id
        parts=self._callout_group_parts(page, group_id) if group_id else [(annot,meta)]
        current_text=""
        for pa, pm in parts:
            current_text=self._callout_text(pa) or current_text
        text = current_text if new_text is None else str(new_text)
        nbox=fitz.Rect(box if box is not None else meta["box"])
        nar=fitz.Point(arrow if arrow is not None else meta["arrow"])
        nfs=float(fontsize if fontsize is not None else meta["fs"])
        nsh=int(shade if shade is not None else meta["shade"])
        try:
            self._capture_undo_state(action_name)
            self._delete_callout_parts(page, parts)
            newa, _refs, _gid, _content_refs = self._create_callout_group(
                page,nbox,nar,text,nfs,nsh,group_id=group_id or None
            )
            self.dirty=True; self._refresh_annotation_pages([page_index]); self._select_annotation_object(page_index,newa)
            self._set_status(f"{action_name}完成｜字體 {nfs:g} pt｜底色階 {nsh+1}/{len(CALLOUT_FILL_SHADES)}｜Undo {len(self.undo_stack)}/{UNDO_LIMIT}")
        except Exception as e:
            self._set_status(f"{action_name}失敗：{e}"); QMessageBox.critical(self,"圖說修改失敗",f"{e}")
        finally: self._update_controls()

    def _selected_callout_bundle(self):
        """回傳目前選取圖說；xref 失效時以穩定 group ID 自動重新綁定。"""
        if self.doc is None or self.selected_page_index is None:
            return None
        try:
            page_index = self.selected_page_index
            if not (0 <= page_index < len(self.doc)):
                return None
            page = self.doc[page_index]
            annot = None
            meta = None

            # 先走最快的 xref；圖說重建後舊 xref 可能已不存在或已指向別的物件。
            if self.selected_annot_xref is not None:
                try:
                    candidate = page.load_annot(self.selected_annot_xref)
                except Exception:
                    candidate = None
                if candidate is not None:
                    candidate_meta = self._parse_callout_meta(candidate)
                    if candidate_meta is not None:
                        expected_group = self.selected_callout_group_id
                        candidate_group = candidate_meta.get("group", "")
                        if not expected_group or candidate_group == expected_group:
                            annot = candidate
                            meta = candidate_meta

            # xref 不可靠時，以 group ID 掃描目前頁面重新找到圖說。
            group_id = self.selected_callout_group_id
            if (annot is None or meta is None) and group_id:
                a = page.first_annot
                guard = 0
                while a is not None and guard < 100000:
                    m = self._parse_callout_meta(a)
                    if m is not None and m.get("group", "") == group_id:
                        annot = a
                        meta = m
                        self.selected_annot_xref = a.xref
                        break
                    a = a.next
                    guard += 1

            if annot is None or meta is None:
                return None

            group_id = meta.get("group", "")
            if group_id:
                self.selected_callout_group_id = group_id
                parts = self._callout_group_parts(page, group_id)
            else:
                parts = [(annot, meta)]

            text = ""
            for pa, _pm in parts:
                text = self._callout_text(pa) or text
            return page_index, page, annot, meta, parts, text
        except Exception:
            return None

    def copy_selected_callout(self):
        bundle = self._selected_callout_bundle()
        if bundle is None:
            self._set_status("請先選取要複製的圖說")
            return
        page_index, page, _annot, meta, _parts, text = bundle
        pr = page.rect
        box = fitz.Rect(meta["box"])
        arrow = fitz.Point(meta["arrow"])

        # 預設往右下錯開 18 pt；靠近頁緣時自動改往左 / 上，避免複製後跑出頁面。
        step = 18.0
        dx = step if max(box.x1, arrow.x) + step <= pr.x1 else (-step if min(box.x0, arrow.x) - step >= pr.x0 else 0.0)
        dy = step if max(box.y1, arrow.y) + step <= pr.y1 else (-step if min(box.y0, arrow.y) - step >= pr.y0 else 0.0)
        new_box = fitz.Rect(box.x0 + dx, box.y0 + dy, box.x1 + dx, box.y1 + dy)
        new_arrow = fitz.Point(arrow.x + dx, arrow.y + dy)

        try:
            newa, refs, _gid, content_refs = self._create_callout_group(
                page, new_box, new_arrow, text, meta["fs"], meta["shade"]
            )
            self._set_added_annotations_undo(
                f"複製圖說（第 {page_index + 1} 頁）", refs, content_refs
            )
            self.dirty = True
            self._refresh_annotation_pages([page_index])
            self._select_annotation_object(page_index, newa)
            self._set_status(
                f"圖說已複製：第 {page_index + 1} 頁｜位置錯開 ({dx:g}, {dy:g}) pt｜可 Ctrl+Z 回復"
            )
        except Exception as e:
            self._set_status(f"複製圖說失敗：{e}")
            QMessageBox.critical(self, "複製圖說失敗", f"無法複製圖說：\n{e}")
        finally:
            self._update_controls()

    def edit_selected_callout_text(self):
        bundle = self._selected_callout_bundle()
        if bundle is None:
            self._set_status("請先選取要修改文字的圖說")
            return
        page_index, _page, _annot, _meta, _parts, old_text = bundle
        new_text, ok = QInputDialog.getMultiLineText(
            self, "修改圖說內容", "圖說文字：", old_text
        )
        if not ok:
            self._set_status("已取消修改圖說內容")
            return
        if new_text == old_text:
            self._set_status("圖說內容沒有變更")
            return
        self._replace_selected_callout(
            new_text=new_text, action_name=f"修改第 {page_index + 1} 頁圖說文字"
        )

    def _callout_annotation_at(self, page_index: int, pdf_x: float, pdf_y: float):
        """只尋找 Pdect 圖說；供雙擊文字編輯使用，避免被其他註記搶先選取。"""
        if self.doc is None or not (0 <= page_index < len(self.doc)):
            return None
        page = self.doc[page_index]
        point = fitz.Point(pdf_x, pdf_y)
        annot = page.first_annot
        guard = 0
        while annot is not None and guard < 100000:
            try:
                meta = self._parse_callout_meta(annot)
                if meta is not None:
                    box = fitz.Rect(meta["box"])
                    # 文字框是最主要的雙擊區；箭頭則使用 annotation 自身 rect。
                    box_hit = fitz.Rect(box.x0 - 4, box.y0 - 4, box.x1 + 4, box.y1 + 4)
                    ar = annot.rect
                    annot_hit = fitz.Rect(ar.x0 - 6, ar.y0 - 6, ar.x1 + 6, ar.y1 + 6)
                    if point in box_hit or point in annot_hit:
                        return annot
            except Exception:
                pass
            annot = annot.next
            guard += 1
        return None

    def edit_callout_at(self, page_index: int, pdf_x: float, pdf_y: float):
        """在頁面上雙擊圖說：以 group ID 重新綁定後開啟內容編輯。"""
        selected = self._callout_annotation_at(page_index, pdf_x, pdf_y)
        if selected is None:
            return
        self._select_annotation_object(page_index, selected)
        if self._selected_callout_bundle() is not None:
            self.edit_selected_callout_text()

    def show_callout_context_menu(self, page_index: int, pdf_x: float, pdf_y: float, global_pos):
        """圖說右鍵選單：複製 / 刪除。非圖說位置不顯示選單。"""
        self.select_annotation_at(page_index, pdf_x, pdf_y)
        if self._selected_callout_bundle() is None:
            return
        menu = QMenu(self)
        copy_action = menu.addAction("複製圖說")
        delete_action = menu.addAction("刪除圖說")
        chosen = menu.exec(global_pos)
        if chosen == copy_action:
            self.copy_selected_callout()
        elif chosen == delete_action:
            self.delete_selected_annotation()

    def adjust_selected_callout(self, page_index: int, action: str):
        if page_index != self.selected_page_index or self.doc is None or self.selected_annot_xref is None: return
        try: annot=self.doc[page_index].load_annot(self.selected_annot_xref)
        except Exception: annot=None
        if annot is None: return
        meta=self._parse_callout_meta(annot)
        if meta is None: return
        if action=="font_plus": self._replace_selected_callout(fontsize=min(CALLOUT_MAX_FONT_SIZE,meta["fs"]+1), action_name="圖說字體放大")
        elif action=="font_minus": self._replace_selected_callout(fontsize=max(CALLOUT_MIN_FONT_SIZE,meta["fs"]-1), action_name="圖說字體縮小")
        elif action=="shade_lighter": self._replace_selected_callout(shade=max(0,meta["shade"]-1), action_name="圖說底色變淺")
        elif action=="shade_darker": self._replace_selected_callout(shade=min(len(CALLOUT_FILL_SHADES)-1,meta["shade"]+1), action_name="圖說底色變深")

    def resize_selected_callout(self, page_index:int, x0:float,y0:float,x1:float,y1:float):
        if page_index != self.selected_page_index or self.doc is None: return
        pr=self.doc[page_index].rect
        box=fitz.Rect(max(pr.x0,x0),max(pr.y0,y0),min(pr.x1,x1),min(pr.y1,y1))
        # 取消原本 20x14 pt 的最小尺寸限制，只需保持有效矩形。
        if box.width <= 0.5 or box.height <= 0.5: return
        self._replace_selected_callout(box=box, action_name="調整圖說方框大小")

    def move_selected_callout(self, page_index:int, x0:float,y0:float,x1:float,y1:float, ax:float, ay:float):
        if page_index != self.selected_page_index or self.doc is None: return
        pr=self.doc[page_index].rect
        box=fitz.Rect(max(pr.x0,x0),max(pr.y0,y0),min(pr.x1,x1),min(pr.y1,y1))
        if box.width <= 0.5 or box.height <= 0.5: return
        arrow=fitz.Point(max(pr.x0,min(pr.x1,ax)), max(pr.y0,min(pr.y1,ay)))
        self._replace_selected_callout(box=box, arrow=arrow, action_name="移動圖說位置")

    def move_selected_callout_arrow(self, page_index:int, x:float,y:float):
        if page_index != self.selected_page_index or self.doc is None: return
        pr=self.doc[page_index].rect
        arrow=fitz.Point(max(pr.x0,min(pr.x1,x)), max(pr.y0,min(pr.y1,y)))
        self._replace_selected_callout(arrow=arrow, action_name="延伸圖說箭頭")

    def _select_annotation_object(self, page_index:int, selected):
        self._clear_selection(update_view=True)
        self.selected_page_index=page_index; self.selected_annot_xref=selected.xref
        r=selected.rect; self.selected_annot_rect=(r.x0,r.y0,r.x1,r.y1)
        meta=self._parse_callout_meta(selected)
        label=self.page_labels[page_index] if 0 <= page_index < len(self.page_labels) else None
        if meta is not None:
            self.selected_callout_group_id = meta.get("group", "") or None
            if label:
                label.set_selected_pdf_rect(None)
                label.set_callout_overlay((meta["box"].x0,meta["box"].y0,meta["box"].x1,meta["box"].y1),(meta["arrow"].x,meta["arrow"].y))
            self.selection_label.setText(f"已選取：第 {page_index+1} 頁 / 圖說（拖移/縮放/箭頭；雙擊改文字；右鍵複製或刪除）")
            self._set_status("已選取圖說：拖框移動；右下角改大小；拖圓點改箭頭；雙擊改文字；右鍵可複製/刪除；Del 可刪除")
        else:
            self.selected_callout_group_id = None
            if label: label.set_selected_pdf_rect(self.selected_annot_rect); label.set_callout_overlay(None,None)
            try: type_name=selected.type[1]
            except Exception: type_name="Annotation"
            self.selection_label.setText(f"已選取：第 {page_index+1} 頁 / {type_name}（Del 刪除）")
            self._set_status("已選取註記，可按 Delete 鍵刪除")
        self._update_controls()

    # ---------- 快速窗選清除標記 ----------
    @staticmethod
    def _rects_intersect(a, b) -> bool:
        try:
            return not (a.x1 < b.x0 or a.x0 > b.x1 or a.y1 < b.y0 or a.y0 > b.y1)
        except Exception:
            return False

    def clear_marks_in_rect(self, page_index: int, x0: float, y0: float, x1: float, y1: float):
        """刪除單一頁面框選範圍內相交的 PDF 註記；一次操作只建立一筆 Undo。"""
        if self.doc is None or not (0 <= page_index < len(self.doc)):
            return

        page = self.doc[page_index]
        page_rect = fitz.Rect(page.rect)
        clear_rect = fitz.Rect(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        clear_rect = clear_rect & page_rect
        if clear_rect.is_empty or clear_rect.width < 0.5 or clear_rect.height < 0.5:
            self._set_status("快速清除：框選範圍太小，未刪除任何標記")
            return

        plain_xrefs: list[int] = []
        callout_groups: set[str] = set()
        annot = page.first_annot
        while annot:
            try:
                meta = self._parse_callout_meta(annot)
                if meta is not None and meta.get("group"):
                    br = fitz.Rect(meta["box"])
                    ar = meta["arrow"]
                    hit_rect = fitz.Rect(
                        min(br.x0, ar.x), min(br.y0, ar.y),
                        max(br.x1, ar.x), max(br.y1, ar.y),
                    )
                    if self._rects_intersect(clear_rect, hit_rect):
                        callout_groups.add(str(meta["group"]))
                else:
                    hit_rect = fitz.Rect(annot.rect)
                    # 線條 / Ink 等註記的 rect 可能極薄，稍微擴張以符合肉眼框選。
                    try:
                        type_name = str(annot.type[1]).lower()
                    except Exception:
                        type_name = ""
                    if any(k in type_name for k in ("line", "ink", "strike", "highlight", "underline", "squiggly")):
                        hit_rect = fitz.Rect(hit_rect.x0-2, hit_rect.y0-2, hit_rect.x1+2, hit_rect.y1+2)
                    if self._rects_intersect(clear_rect, hit_rect):
                        plain_xrefs.append(int(annot.xref))
            except Exception:
                pass
            annot = annot.next

        # 去除可能重複的 xref；圖說群組會由群組刪除函式整組處理。
        plain_xrefs = list(dict.fromkeys(plain_xrefs))
        logical_count = len(plain_xrefs) + len(callout_groups)
        if logical_count == 0:
            self._set_status(f"快速清除：第 {page_index+1} 頁框選範圍內沒有標記")
            return

        try:
            self._capture_undo_state(f"快速清除第 {page_index+1} 頁 {logical_count} 個標記")

            deleted_groups = 0
            for group in sorted(callout_groups):
                try:
                    parts = self._callout_group_parts(page, group)
                    if parts:
                        self._delete_callout_parts(page, parts)
                        deleted_groups += 1
                except Exception:
                    pass

            deleted_plain = 0
            for xref in plain_xrefs:
                try:
                    target = page.load_annot(xref)
                    if target is not None:
                        # 若這個 xref 已隨圖說群組刪除，load_annot 會失敗或回 None。
                        page.delete_annot(target)
                        deleted_plain += 1
                except Exception:
                    pass

            deleted_total = deleted_groups + deleted_plain
            if deleted_total <= 0:
                # 沒有真的刪到東西時，移除剛建立的 Undo 快照。
                if self.undo_stack:
                    entry = self.undo_stack.pop()
                    if entry.get("kind") == "snapshot":
                        try:
                            Path(entry.get("path", "")).unlink(missing_ok=True)
                        except Exception:
                            pass
                self._update_controls()
                self._set_status("快速清除：沒有可刪除的標記")
                return

            self.dirty = True
            self._clear_selection(update_view=False)
            self._refresh_annotation_pages([page_index])
            self._set_status(
                f"快速清除完成：第 {page_index+1} 頁已刪除 {deleted_total} 個標記｜可按 Ctrl+Z 回復"
            )
        except Exception as e:
            self._set_status(f"快速清除失敗：{e}")
            QMessageBox.critical(self, "快速清除失敗", f"無法刪除框選範圍內的標記：\n{e}")
        finally:
            self._update_controls()

    # ---------- 點選 / 刪除註記 ----------
    def select_annotation_at(self, page_index: int, pdf_x: float, pdf_y: float):
        if self.doc is None or not (0 <= page_index < len(self.doc)): return
        page=self.doc[page_index]; point=fitz.Point(pdf_x,pdf_y); selected=None
        annot=page.first_annot
        while annot:
            try:
                meta=self._parse_callout_meta(annot)
                if meta is not None:
                    # 圖說以文字框 + 箭頭聯集區域作選取。
                    br=fitz.Rect(meta["box"]); ar=meta["arrow"]
                    rr=fitz.Rect(min(br.x0,ar.x)-6,min(br.y0,ar.y)-6,max(br.x1,ar.x)+6,max(br.y1,ar.y)+6)
                    if point in rr: selected=annot; break
                else:
                    r=annot.rect; hit=fitz.Rect(r.x0-5,r.y0-5,r.x1+5,r.y1+5)
                    if point in hit: selected=annot; break
            except Exception: pass
            annot=annot.next
        if selected is None:
            self._clear_selection(update_view=True); self._set_status("此位置沒有可刪除的註記"); return
        self._select_annotation_object(page_index, selected)

    def delete_selected_annotation(self):
        if (
            self.doc is None
            or self.selected_page_index is None
            or self.selected_annot_xref is None
        ):
            return

        try:
            page_index = self.selected_page_index
            page = self.doc[page_index]
            target = None
            annot = page.first_annot
            while annot:
                if annot.xref == self.selected_annot_xref:
                    target = annot
                    break
                annot = annot.next

            if target is None:
                self._clear_selection(update_view=True)
                return

            meta = self._parse_callout_meta(target)
            self._capture_undo_state(f"刪除第 {page_index + 1} 頁註記")
            if meta is not None and meta.get("group"):
                parts = self._callout_group_parts(page, meta["group"])
                self._delete_callout_parts(page, parts)
            else:
                page.delete_annot(target)
            self.dirty = True
            self._clear_selection(update_view=False)
            self._refresh_annotation_pages([page_index])
            self._set_status("註記已刪除；可按 Ctrl+Z 回復")
        except Exception as e:
            self._set_status(f"刪除失敗：{e}")
            QMessageBox.critical(self, "刪除失敗", f"無法刪除註記：\n{e}")

    def _clear_selection(self, update_view: bool = True):
        old_page = self.selected_page_index
        self.selected_page_index = None
        self.selected_annot_xref = None
        self.selected_callout_group_id = None
        self.selected_annot_rect = None
        self.selection_label.setText("未選取註記")

        if old_page is not None and 0 <= old_page < len(self.page_labels):
            self.page_labels[old_page].set_callout_overlay(None, None)
            if update_view:
                self.page_labels[old_page].set_selected_pdf_rect(None)


    # ---------- 儲存 ----------
    def _edit_series_info(self, path: Path):
        """辨識 foo_edit.pdf / foo_edit_01.pdf / foo_edit_002.pdf 為同一修改系列。"""
        match = re.match(r"^(?P<root>.+_edit)(?:_(?P<version>\d+))?$", path.stem, re.IGNORECASE)
        if not match:
            return None
        root = match.group("root")
        version_text = match.group("version")
        version = int(version_text) if version_text is not None else 0
        return root, version

    def _next_edit_version_path(self, current_path: Path) -> Path:
        """掃描同資料夾同系列版本，回傳下一個不重複的 _## 檔名。"""
        info = self._edit_series_info(current_path)
        if info is None:
            root = f"{current_path.stem}_edit"
        else:
            root, _ = info

        version_re = re.compile(rf"^{re.escape(root)}_(\d+)\.pdf$", re.IGNORECASE)
        max_version = 0
        try:
            entries = current_path.parent.iterdir()
        except Exception:
            entries = []

        for candidate in entries:
            if not candidate.is_file():
                continue
            m = version_re.match(candidate.name)
            if m:
                try:
                    max_version = max(max_version, int(m.group(1)))
                except ValueError:
                    pass

        # 至少兩位數：01~99；100 之後自然擴成三位數。
        version = max_version + 1
        while True:
            candidate = current_path.with_name(f"{root}_{version:02d}.pdf")
            if not candidate.exists():
                return candidate
            version += 1

    def _choose_save_output(self) -> Optional[Path]:
        """依目前檔名決定輸出位置；_edit 系列會先詢問覆蓋或建立新版本。"""
        if self.pdf_path is None:
            return None

        info = self._edit_series_info(self.pdf_path)
        if info is None:
            return self.pdf_path.with_name(f"{self.pdf_path.stem}_edit.pdf")

        root, current_version = info
        next_path = self._next_edit_version_path(self.pdf_path)
        current_label = "主修改檔" if current_version == 0 else f"第 {current_version:02d} 版"

        box = QMessageBox(self)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle("儲存修改檔")
        box.setText(f"目前檔名已屬於 _edit 修改系列：\n{self.pdf_path.name}")
        box.setInformativeText(
            f"目前識別為：{current_label}\n\n"
            "要覆蓋目前這個檔案，還是另存下一個修改版本？\n"
            f"下一個未使用版本：{next_path.name}"
        )
        overwrite_button = box.addButton("覆蓋原檔", QMessageBox.ButtonRole.AcceptRole)
        version_button = box.addButton("另存新版本", QMessageBox.ButtonRole.ActionRole)
        cancel_button = box.addButton("取消", QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(version_button)
        box.exec()

        clicked = box.clickedButton()
        if clicked is overwrite_button:
            self._set_status(f"儲存方式：覆蓋 {self.pdf_path.name}")
            return self.pdf_path
        if clicked is version_button:
            self._set_status(f"儲存方式：建立新版本 {next_path.name}")
            return next_path

        self._set_status("已取消儲存")
        return None

    def _migrate_legacy_pdect_callouts(self) -> int:
        """Replace V0.2.x FreeText callouts with embedded vector DFKai-SB text."""
        if self.doc is None:
            return 0
        targets=[]
        for page_index in range(len(self.doc)):
            page=self.doc[page_index]
            groups={}
            annot=page.first_annot
            while annot:
                try:
                    meta=self._parse_callout_meta(annot)
                    group_id=meta.get("group", "") if meta else ""
                    if group_id:
                        groups.setdefault(group_id, []).append((annot.xref, meta, self._callout_text(annot)))
                except Exception:
                    pass
                annot=annot.next
            for group_id, rows in groups.items():
                if not any(meta.get("part") == "text" for _xref, meta, _text in rows):
                    continue
                base=rows[0][1]
                text=""
                for _xref, _meta, value in rows:
                    text=value or text
                targets.append((
                    page_index, group_id, [xref for xref,_meta,_text in rows],
                    text, fitz.Rect(base["box"]), fitz.Point(base["arrow"]),
                    float(base["fs"]), int(base["shade"]),
                ))

        converted=0
        for page_index, _old_group, old_xrefs, text, box, arrow, fs, shade in targets:
            page=self.doc[page_index]
            try:
                # 先成功建立新版群組才刪除舊群組，失敗時原圖說仍完整保留。
                self._create_callout_group(page, box, arrow, text, fs, shade)
                old_parts=[]
                for xref in old_xrefs:
                    try:
                        annot=page.load_annot(xref)
                        meta=self._parse_callout_meta(annot) if annot is not None else None
                        if annot is not None and meta is not None:
                            old_parts.append((annot,meta))
                    except Exception:
                        pass
                self._delete_callout_parts(page, old_parts)
                converted += 1
            except Exception:
                continue
        return converted
    def save_pdf(self):
        if self.doc is None or self.pdf_path is None:
            self._set_status("目前沒有可儲存的 PDF")
            return

        out = self._choose_save_output()
        if out is None:
            return

        source_path_before = Path(self.pdf_path)
        try:
            source_size_bytes_before = source_path_before.stat().st_size
        except Exception:
            source_size_bytes_before = 0
        temp_out = out.with_name(f".{out.stem}_{uuid.uuid4().hex[:10]}.saving.pdf")
        old_scroll = self.scroll.verticalScrollBar().value() if hasattr(self, "scroll") else 0

        save_mode = "快速無損壓縮"

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.save_action.setEnabled(False)
        try:
            # 先清除 GUI 端持有的 Annotation wrapper，避免存檔期間還有舊 Annot 參照。
            self._clear_selection(update_view=False)
            gc.collect()

            # 舊版 Pdect FreeText 圖說改建為嵌入標楷體的向量內容。
            converted = self._migrate_legacy_pdect_callouts()
            if converted:
                self.dirty = True
                # 圖說文字 annotation 的 xref 已更換，舊的輕量 Undo xref 不再可靠。
                self._clear_undo_stack()
                self._set_status(f"正在儲存：先轉換 {converted} 個舊版圖說文字為穩定格式…")
                gc.collect()

            if temp_out.exists():
                temp_out.unlink()

            font_mode = ""
            if self._callout_font_needs_subset:
                self._set_status(f"正在儲存：{out.name}｜子集化標楷體字型…")
                try:
                    self.doc.subset_fonts()
                    font_mode = "｜標楷體已嵌入並子集化"
                except Exception:
                    # 子集化失敗仍保留完整嵌入字型，正確顯示優先於容量。
                    font_mode = "｜標楷體完整嵌入（子集化未完成）"
                gc.collect()

            self._set_status(f"正在儲存：{out.name}｜步驟 1/4：寫入安全暫存檔…")

            # Fast lossless compact save: remove unreachable objects, compact
            # the xref table, Flate-compress uncompressed streams, images and
            # fonts, and place eligible objects in object streams. garbage=2
            # intentionally avoids the expensive duplicate-object scan of
            # garbage=3 on PDFs with tens of thousands of xrefs. Existing
            # JPEG/JPEG2000 samples are not rasterized or recompressed.
            try:
                self.doc.save(
                    str(temp_out),
                    garbage=2,
                    clean=False,
                    deflate=True,
                    deflate_images=True,
                    deflate_fonts=True,
                    use_objstms=1,
                    compression_effort=0,
                )
            except Exception:
                # Keep a compatibility path for unusual or partly repaired PDFs.
                # A failed compact attempt never touches the destination file.
                temp_out.unlink(missing_ok=True)
                save_mode = "相容模式"
                self.doc.save(
                    str(temp_out),
                    garbage=1,
                    clean=False,
                    deflate=True,
                    deflate_images=False,
                    deflate_fonts=False,
                    use_objstms=0,
                )

            if not temp_out.exists() or temp_out.stat().st_size <= 0:
                raise RuntimeError("暫存 PDF 沒有成功建立")

            self._set_status(f"正在儲存：{out.name}｜步驟 2/4：驗證 PDF 完整性…")
            check_doc = None
            try:
                check_doc = fitz.open(str(temp_out))
                if len(check_doc) != len(self.doc):
                    raise RuntimeError(
                        f"頁數驗證失敗：暫存檔 {len(check_doc)} 頁，工作檔 {len(self.doc)} 頁"
                    )
                # 不只讀 rect，也實際載入首末頁內容與 annotation 鏈，
                # 提前抓出部分「可以 open 但物件結構損壞」的情況。
                if len(check_doc) > 0:
                    for idx in {0, len(check_doc)-1}:
                        pg = check_doc[idx]
                        _ = pg.rect
                        _ = pg.get_text("text")
                        aa = pg.first_annot
                        guard = 0
                        while aa is not None and guard < 100000:
                            _ = aa.rect
                            aa = aa.next
                            guard += 1
            finally:
                if check_doc is not None:
                    check_doc.close()

            self._set_status(f"正在儲存：{out.name}｜步驟 3/4：關閉工作檔並更新正式檔案…")

            # Windows 對「正在開啟中的 PDF」做 replace 很容易失敗。
            # V0.0.15 改成驗證成功後，一律先關閉目前 Document，再更新正式檔。
            old_doc = self.doc
            self.doc = None
            try:
                if old_doc is not None:
                    old_doc.close()
            finally:
                old_doc = None
            gc.collect()

            try:
                os.replace(str(temp_out), str(out))
            except Exception as replace_error:
                # 某些 NAS / 雲端同步 / 防毒環境對 os.replace 支援不完整。
                # 退回一般複製覆蓋；暫存檔已驗證，所以仍比直接寫正式檔安全。
                try:
                    shutil.copy2(str(temp_out), str(out))
                    temp_out.unlink(missing_ok=True)
                except Exception:
                    raise replace_error

            self._set_status(f"正在儲存：{out.name}｜步驟 4/4：重新開啟工作檔…")
            self.doc = fitz.open(str(out))

            self.pdf_path = out
            self.dirty = False
            self.callout_font_resource = CALLOUT_FONT_RESOURCE_PREFIX + uuid.uuid4().hex[:8]
            self._callout_font_needs_subset = False
            self._refresh_bookmark_combo()

            # 儲存後物件 xref 可能因 PDF 重寫而改變，因此舊 Undo xref 不再可靠。
            # 清除歷史後重新以剛存好的檔案作為工作基準。
            self._clear_undo_stack()
            self._clear_selection(update_view=False)
            self.start_page_spin.setRange(1, max(1, len(self.doc)))
            self.rendered_pages.clear()
            self.schedule_visible_render(0)
            try:
                self.scroll.verticalScrollBar().setValue(old_scroll)
            except Exception:
                pass
            self._update_controls()

            size_mb = out.stat().st_size / (1024 * 1024)
            src_mb = source_size_bytes_before / (1024 * 1024) if source_size_bytes_before > 0 else 0.0
            ratio = (size_mb / src_mb) if src_mb > 0 else 0.0
            version_info = self._edit_series_info(out)
            version_text = ""
            if version_info is not None:
                _, saved_version = version_info
                version_text = "｜修改主檔" if saved_version == 0 else f"｜修改版本 {saved_version:02d}"

            self._set_status(
                f"存檔成功：{out.name}{version_text}｜{len(self.doc)} 頁｜{size_mb:.1f} MB"
                + (f"｜前一檔 {src_mb:.1f} MB｜{ratio:.2f}×" if src_mb else "")
                + f"｜{save_mode}{font_mode}"
                + (f"｜已修復舊圖說 {converted} 個" if converted else "")
            )

        except Exception as e:
            # 若正式更新前已經關閉工作 doc，盡可能恢復來源；若正式檔已存在則
            # 優先開啟 out，避免使用者看到空白工作區。
            if self.doc is None:
                for candidate in (out, source_path_before):
                    try:
                        if candidate.exists():
                            self.doc = fitz.open(str(candidate))
                            self.pdf_path = candidate

                            break
                    except Exception:
                        self.doc = None
            self._set_status(f"存檔失敗：{e}｜暫存檔未直接覆寫原工作檔")
            QMessageBox.critical(
                self,
                "存檔失敗",
                f"無法儲存 PDF：\n{e}\n\n"
                f"{APP_VERSION} 會先嘗試快速無損壓縮並自動退回相容模式；若仍失敗，請確認檔案不是唯讀、"
                "沒有被其他 PDF 程式鎖定，且所在資料夾可以寫入。",
            )
        finally:
            try:
                if temp_out.exists():
                    temp_out.unlink()
            except Exception:
                pass
            QApplication.restoreOverrideCursor()
            self._update_controls()

    # ---------- 關閉 ----------
    def closeEvent(self, event):
        self._save_current_view_state()
        if self.dirty:
            reply = QMessageBox.question(
                self,
                "尚未存檔",
                "目前有尚未儲存的修改，確定要離開嗎？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return

        try:
            self._clear_undo_stack()
            if self.undo_temp_dir is not None:
                shutil.rmtree(self.undo_temp_dir, ignore_errors=True)
        except Exception:
            pass
        if self.doc is not None:
            try:
                self.doc.close()
            except Exception:
                pass
        event.accept()


def dependency_error_message() -> str:
    missing = []
    if QApplication is None:
        missing.append("PySide6")
    if not load_pdf_engine():
        missing.append("PyMuPDF")
    if not missing:
        return ""
    return (
        "缺少必要套件：" + ", ".join(missing) + "\n\n"
        "請開啟命令提示字元執行：\n"
        "pip install PySide6 PyMuPDF"
    )


def main():
    msg = dependency_error_message()
    if msg:
        print(msg)
        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(f"{APP_TITLE} {APP_VERSION}", msg)
            root.destroy()
        except Exception:
            pass
        return 1

    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setApplicationVersion(APP_VERSION)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
