# -*- coding: utf-8 -*-
"""
Pdect V0.3.5 recovery / quick-save extension.

Designed to be imported by the small compatibility launcher before pdect_app.main().
It patches the existing Pdect QMainWindow class without replacing pdect_app.py.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

EXT_VERSION = "V0.3.5"
AUTOSAVE_INTERVAL_MS = 60_000
AUTOSAVE_INTERVAL_SECONDS = 60

try:
    import fitz  # type: ignore
except Exception:
    fitz = None

try:
    from PySide6.QtCore import QTimer, Qt, QPointF
    from PySide6.QtGui import QAction, QColor, QIcon, QKeySequence, QPainter, QPen, QPixmap, QPolygonF, QBrush
    from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolBar
except Exception:  # pragma: no cover - Pdect itself requires PySide6
    QTimer = None
    QMainWindow = object
    QApplication = None
    QMessageBox = None
    QToolBar = None


_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="PdectAutosave")
_RECOVERY_SCAN_STARTED = False
_PATCHED_CLASSES: set[type] = set()


def _recovery_root() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    if local:
        root = Path(local) / "Pdect" / "autosave"
    else:
        root = Path.home() / ".pdect" / "autosave"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _norm_path(path: Path | str) -> str:
    try:
        return str(Path(path).resolve(strict=False)).casefold()
    except Exception:
        return str(path).casefold()


def _record_key(path: Path | str) -> str:
    return hashlib.sha256(_norm_path(path).encode("utf-8", "surrogatepass")).hexdigest()[:24]


def _record_dir(path: Path | str) -> Path:
    return _recovery_root() / _record_key(path)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp_{os.getpid()}_{time.time_ns()}")
    try:
        with tmp.open("wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    _atomic_write_bytes(path, data)


def _remove_record_dir(folder: Path) -> None:
    try:
        shutil.rmtree(folder, ignore_errors=True)
    except Exception:
        pass


def _clear_record_for_path(path: Optional[Path | str]) -> None:
    if not path:
        return
    _remove_record_dir(_record_dir(path))


def _validate_pdf(path: Path, expected_pages: Optional[int] = None) -> None:
    if fitz is None:
        if not path.exists() or path.stat().st_size <= 0:
            raise RuntimeError("暫存 PDF 檔案不存在或大小為 0")
        return
    doc = fitz.open(str(path))
    try:
        if expected_pages is not None and len(doc) != int(expected_pages):
            raise RuntimeError(f"頁數驗證失敗：{len(doc)} != {expected_pages}")
    finally:
        doc.close()


def _edit_series(path: Path) -> tuple[str, int]:
    stem = path.stem
    m = re.match(r"^(?P<base>.+)_edit(?:_(?P<num>\d+))?$", stem, re.IGNORECASE)
    if m:
        return m.group("base"), int(m.group("num") or 0)
    return stem, -1


def _next_version_path(formal_path: Path) -> Path:
    base, _ = _edit_series(formal_path)
    max_no = 0
    pattern = re.compile(rf"^{re.escape(base)}_edit(?:_(\d+))?\.pdf$", re.IGNORECASE)
    try:
        for p in formal_path.parent.glob("*.pdf"):
            m = pattern.match(p.name)
            if not m:
                continue
            no = int(m.group(1) or 0)
            max_no = max(max_no, no)
    except Exception:
        pass
    n = max_no + 1
    while True:
        candidate = formal_path.parent / f"{base}_edit_{n:02d}.pdf"
        if not candidate.exists():
            return candidate
        n += 1


def _restore_snapshot(snapshot: Path, target: Path, expected_pages: Optional[int]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.stem}_restore_", suffix=".pdf", dir=str(target.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        shutil.copy2(snapshot, tmp)
        _validate_pdf(tmp, expected_pages)
        os.replace(tmp, target)
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def _status(window: Any, text: str, timeout_ms: int = 6000) -> None:
    try:
        setter = getattr(window, "_set_status", None)
        if callable(setter):
            setter(text)
            return
    except Exception:
        pass
    try:
        sb = window.statusBar()
        sb.showMessage(text, timeout_ms)
    except Exception:
        pass


def _quick_save_icon() -> "QIcon":
    pix = QPixmap(28, 28)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing, True)

    # floppy disk body
    p.setPen(QPen(QColor("#2E5B8A"), 1.5))
    p.setBrush(QBrush(QColor("#DCEBFA")))
    p.drawRoundedRect(4, 3, 19, 21, 2, 2)
    p.setBrush(QBrush(QColor("#FFFFFF")))
    p.drawRect(8, 5, 10, 6)
    p.setBrush(QBrush(QColor("#B8D4EF")))
    p.drawRect(8, 16, 11, 6)

    # lightning bolt = quick
    p.setPen(QPen(QColor("#9C6A00"), 1.0))
    p.setBrush(QBrush(QColor("#FFC928")))
    bolt = QPolygonF([
        QPointF(18, 10), QPointF(13, 17), QPointF(17, 17),
        QPointF(14, 24), QPointF(23, 14), QPointF(19, 14),
    ])
    p.drawPolygon(bolt)
    p.end()
    return QIcon(pix)


def _doc_bytes(doc: Any) -> bytes:
    # Keep autosave conservative and quick: no cleanup / recompression.
    attempts = [
        dict(garbage=0, clean=False, deflate=False, use_objstms=0),
        dict(garbage=0, deflate=False),
        {},
    ]
    last: Optional[Exception] = None
    for kwargs in attempts:
        try:
            return bytes(doc.tobytes(**kwargs))
        except Exception as e:
            last = e
    raise RuntimeError(f"建立背景暫存失敗：{last}")


def _write_autosave_worker(
    source_path_text: str,
    pdf_bytes: bytes,
    page_count: int,
    app_version: str,
) -> tuple[bool, str, str]:
    source = Path(source_path_text)
    folder = _record_dir(source)
    folder.mkdir(parents=True, exist_ok=True)
    snapshot = folder / "autosave.pdf"
    meta_path = folder / "meta.json"
    try:
        _atomic_write_bytes(snapshot, pdf_bytes)
        _validate_pdf(snapshot, page_count)
        snapshot_sha = hashlib.sha256(pdf_bytes).hexdigest()

        formal_exists = source.exists()
        formal_sha = None
        formal_size = None
        formal_mtime_ns = None
        if formal_exists:
            try:
                stat = source.stat()
                formal_size = stat.st_size
                formal_mtime_ns = stat.st_mtime_ns
                formal_sha = _sha256_file(source)
            except Exception:
                pass

        now_ns = time.time_ns()
        payload = {
            "schema": 1,
            "app_version": app_version,
            "source_path": str(source),
            "formal_path": str(source),
            "snapshot_path": str(snapshot),
            "page_count": int(page_count),
            "autosave_time_ns": now_ns,
            "autosave_time": datetime.now().isoformat(timespec="seconds"),
            "snapshot_sha256": snapshot_sha,
            "snapshot_size": len(pdf_bytes),
            "formal_exists": formal_exists,
            "formal_sha256_at_autosave": formal_sha,
            "formal_size_at_autosave": formal_size,
            "formal_mtime_ns_at_autosave": formal_mtime_ns,
        }
        _atomic_write_json(meta_path, payload)
        return True, datetime.now().strftime("%H:%M:%S"), str(folder)
    except Exception as e:
        return False, str(e), str(folder)


class RecoveryController:
    def __init__(self, window: Any, app_module: Any):
        self.window = window
        self.app_module = app_module
        self._autosave_busy = False
        self._last_seen_path: Optional[Path] = None
        self._install_quick_save_action()

        self.timer = QTimer(window)
        self.timer.setInterval(AUTOSAVE_INTERVAL_MS)
        self.timer.timeout.connect(self.autosave_tick)
        self.timer.start()

        _status(window, "背景預存已啟用：每 1 分鐘一次；正式儲存後會清除暫存")
        global _RECOVERY_SCAN_STARTED
        if not _RECOVERY_SCAN_STARTED:
            _RECOVERY_SCAN_STARTED = True
            QTimer.singleShot(650, self.scan_recovery_records)

    def _current_doc(self) -> Any:
        doc = getattr(self.window, "doc", None)
        if doc is None:
            doc = getattr(self.window, "document", None)
        return doc

    def _current_path(self) -> Optional[Path]:
        for name in ("pdf_path", "current_pdf_path", "file_path", "current_path"):
            value = getattr(self.window, name, None)
            if value:
                try:
                    return Path(value)
                except Exception:
                    continue
        doc = self._current_doc()
        try:
            if doc is not None and getattr(doc, "name", None):
                return Path(doc.name)
        except Exception:
            pass
        return None

    def _install_quick_save_action(self) -> None:
        try:
            toolbar = self.window.findChild(QToolBar)
        except Exception:
            toolbar = None
        if toolbar is None:
            return

        action = QAction(_quick_save_icon(), "快速儲存", self.window)
        action.setToolTip("快速儲存目前 PDF（Ctrl+Alt+S）")
        action.setShortcut(QKeySequence("Ctrl+Alt+S"))
        action.triggered.connect(self.quick_save)
        self.quick_save_action = action

        actions = toolbar.actions()
        insert_before = None
        for idx, a in enumerate(actions):
            text = (a.text() or "").replace("&", "")
            if text in ("存檔", "儲存", "保存") or "存檔" in text or "儲存" in text:
                if idx + 1 < len(actions):
                    insert_before = actions[idx + 1]
                break
        if insert_before is not None:
            toolbar.insertAction(insert_before, action)
        else:
            toolbar.addAction(action)

    def autosave_tick(self) -> None:
        if self._autosave_busy:
            return
        doc = self._current_doc()
        path = self._current_path()
        if doc is None or path is None:
            return
        try:
            if getattr(doc, "is_closed", False):
                return
            page_count = len(doc)
        except Exception:
            return

        self._last_seen_path = path
        try:
            dirty = bool(getattr(doc, "is_dirty"))
        except Exception:
            dirty = True

        if not dirty:
            # A formal save generally reopens / cleans the document. Remove stale recovery.
            _clear_record_for_path(path)
            return

        self._autosave_busy = True
        try:
            pdf_bytes = _doc_bytes(doc)
        except Exception as e:
            self._autosave_busy = False
            _status(self.window, f"背景預存失敗：{e}")
            return

        version = str(getattr(self.app_module, "APP_VERSION", EXT_VERSION))
        future = _EXECUTOR.submit(_write_autosave_worker, str(path), pdf_bytes, page_count, version)
        future.add_done_callback(lambda fut: QTimer.singleShot(0, lambda: self._autosave_finished(fut)))

    def _autosave_finished(self, future: concurrent.futures.Future) -> None:
        self._autosave_busy = False
        try:
            ok, message, _folder = future.result()
        except Exception as e:
            ok, message = False, str(e)
        if ok:
            _status(self.window, f"背景預存完成：{message}（每 1 分鐘）", 3500)
        else:
            _status(self.window, f"背景預存失敗：{message}", 7000)

    def clear_autosave(self, *paths: Optional[Path | str]) -> None:
        for p in paths:
            _clear_record_for_path(p)

    def on_formal_save_maybe(self, before_path: Optional[Path]) -> None:
        after_path = self._current_path()
        doc = self._current_doc()
        clean = False
        try:
            clean = doc is not None and not bool(getattr(doc, "is_dirty"))
        except Exception:
            pass
        changed_path = bool(before_path and after_path and _norm_path(before_path) != _norm_path(after_path))
        if clean or changed_path:
            self.clear_autosave(before_path, after_path)

    def quick_save(self) -> None:
        doc = self._current_doc()
        path = self._current_path()
        if doc is None or path is None:
            _status(self.window, "快速儲存：目前沒有開啟 PDF")
            return

        base, series_no = _edit_series(path)
        is_edit_series = series_no >= 0
        if is_edit_series:
            try:
                can = getattr(doc, "can_save_incrementally", None)
                can_incr = bool(can()) if callable(can) else False
                doc_name = Path(getattr(doc, "name", "")) if getattr(doc, "name", "") else None
                same_file = doc_name is not None and _norm_path(doc_name) == _norm_path(path)
                if can_incr and same_file:
                    doc.saveIncr()
                    self.clear_autosave(path)
                    _status(self.window, f"快速儲存完成：{path.name}")
                    return
            except Exception as e:
                _status(self.window, f"增量快速儲存不可用，改用一般儲存：{e}", 4500)

        # Original file should keep Pdect's existing _edit / version rules.
        for name in ("save_pdf", "save_file", "save_document", "save_current"):
            method = getattr(self.window, name, None)
            if callable(method):
                try:
                    method()
                    return
                except Exception as e:
                    _status(self.window, f"快速儲存失敗：{e}")
                    return
        _status(self.window, "快速儲存失敗：找不到 Pdect 的正式儲存功能")

    def scan_recovery_records(self) -> None:
        root = _recovery_root()
        try:
            folders = [p for p in root.iterdir() if p.is_dir()]
        except Exception:
            return
        for folder in sorted(folders):
            meta_path = folder / "meta.json"
            snapshot = folder / "autosave.pdf"
            if not meta_path.exists() or not snapshot.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                self._handle_recovery_record(folder, snapshot, meta)
            except Exception:
                continue

    def _handle_recovery_record(self, folder: Path, snapshot: Path, meta: dict[str, Any]) -> None:
        formal_text = meta.get("formal_path") or meta.get("source_path")
        if not formal_text:
            return
        formal = Path(formal_text)
        expected_pages = meta.get("page_count")
        try:
            _validate_pdf(snapshot, expected_pages)
        except Exception:
            _remove_record_dir(folder)
            return

        try:
            snap_hash = meta.get("snapshot_sha256") or _sha256_file(snapshot)
        except Exception:
            snap_hash = None
        formal_hash = None
        if formal.exists():
            try:
                formal_hash = _sha256_file(formal)
            except Exception:
                pass
        if snap_hash and formal_hash and snap_hash == formal_hash:
            _remove_record_dir(folder)
            return

        autosave_time = str(meta.get("autosave_time") or "未知")
        formal_time = "不存在"
        if formal.exists():
            try:
                formal_time = datetime.fromtimestamp(formal.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                formal_time = "未知"

        box = QMessageBox(self.window)
        box.setWindowTitle(f"P找碴 {EXT_VERSION}｜發現未同步暫存")
        box.setIcon(QMessageBox.Warning)
        box.setText(f"發現背景暫存與正式 PDF 不同步：\n\n{formal.name}")
        box.setInformativeText(
            f"背景暫存：{autosave_time}\n正式檔案：{formal_time}\n\n"
            "請選擇要把暫存內容回存正式檔、另存為新的版本序號，或先略過。"
        )
        restore_btn = box.addButton("回存正式檔", QMessageBox.AcceptRole)
        version_btn = box.addButton("另存新版本", QMessageBox.ActionRole)
        skip_btn = box.addButton("略過", QMessageBox.RejectRole)
        box.setDefaultButton(version_btn)
        box.exec()
        clicked = box.clickedButton()

        if clicked is restore_btn:
            try:
                self._close_if_current(formal)
                _restore_snapshot(snapshot, formal, expected_pages)
                _remove_record_dir(folder)
                _status(self.window, f"暫存已回存正式檔：{formal.name}")
                self._reload_if_possible(formal)
            except Exception as e:
                QMessageBox.critical(self.window, "回存失敗", str(e))
        elif clicked is version_btn:
            target = _next_version_path(formal)
            try:
                _restore_snapshot(snapshot, target, expected_pages)
                _remove_record_dir(folder)
                _status(self.window, f"暫存已另存新版本：{target.name}")
                self._reload_if_possible(target)
            except Exception as e:
                QMessageBox.critical(self.window, "另存新版本失敗", str(e))
        elif clicked is skip_btn:
            _status(self.window, f"已略過暫存復原：{formal.name}；下次啟動仍會再次檢查", 5000)

    def _close_if_current(self, target: Path) -> None:
        current = self._current_path()
        if current is None or _norm_path(current) != _norm_path(target):
            return
        doc = self._current_doc()
        try:
            if doc is not None and not getattr(doc, "is_closed", False):
                doc.close()
        except Exception:
            pass
        for name in ("doc", "document"):
            if hasattr(self.window, name):
                try:
                    setattr(self.window, name, None)
                except Exception:
                    pass

    def _reload_if_possible(self, target: Path) -> None:
        for name in ("open_pdf_path", "load_pdf_path", "open_path"):
            method = getattr(self.window, name, None)
            if callable(method):
                try:
                    QTimer.singleShot(0, lambda m=method, p=target: m(p))
                    return
                except Exception:
                    pass


def _patch_save_methods(cls: type) -> None:
    for name in ("save_pdf", "save_file", "save_document", "save_current"):
        original = getattr(cls, name, None)
        if not callable(original) or getattr(original, "_pdect_recovery_wrapped", False):
            continue

        def make_wrapper(orig, method_name):
            def wrapped(self, *args, **kwargs):
                ctrl: Optional[RecoveryController] = getattr(self, "_pdect_recovery_controller", None)
                before = ctrl._current_path() if ctrl else None
                result = orig(self, *args, **kwargs)
                if ctrl is not None:
                    QTimer.singleShot(350, lambda c=ctrl, b=before: c.on_formal_save_maybe(b))
                return result
            wrapped.__name__ = getattr(orig, "__name__", method_name)
            wrapped.__doc__ = getattr(orig, "__doc__", None)
            wrapped._pdect_recovery_wrapped = True
            return wrapped

        setattr(cls, name, make_wrapper(original, name))


def _patch_window_class(cls: type, app_module: Any) -> None:
    if cls in _PATCHED_CLASSES:
        return
    _PATCHED_CLASSES.add(cls)
    _patch_save_methods(cls)

    original_init = cls.__init__
    if getattr(original_init, "_pdect_recovery_wrapped", False):
        return

    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        try:
            title = self.windowTitle()
            title = re.sub(r"V\d+(?:\.\d+){2,3}[A-Za-z]?", EXT_VERSION, title)
            self.setWindowTitle(title)
        except Exception:
            pass
        try:
            self._pdect_recovery_controller = RecoveryController(self, app_module)
        except Exception as e:
            _status(self, f"快速儲存 / 背景預存初始化失敗：{e}")

    patched_init.__name__ = getattr(original_init, "__name__", "__init__")
    patched_init.__doc__ = getattr(original_init, "__doc__", None)
    patched_init._pdect_recovery_wrapped = True
    cls.__init__ = patched_init


def install(app_module: Any) -> int:
    """Patch Pdect window class(es). Returns number of patched classes."""
    if QTimer is None:
        return 0
    try:
        if hasattr(app_module, "APP_VERSION"):
            app_module.APP_VERSION = EXT_VERSION
    except Exception:
        pass

    patched = 0
    for _name, obj in list(vars(app_module).items()):
        if not isinstance(obj, type):
            continue
        try:
            if issubclass(obj, QMainWindow) and obj is not QMainWindow:
                _patch_window_class(obj, app_module)
                patched += 1
        except Exception:
            continue
    return patched
