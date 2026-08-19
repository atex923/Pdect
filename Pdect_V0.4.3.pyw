# -*- coding: utf-8 -*-
"""Pdect V0.4.3 fail-safe launcher.

Keeps the original Codex-built pdect_app as the source of truth.
Quick-save / autosave extension is optional and must never prevent Pdect from starting.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import traceback
from pathlib import Path
from datetime import datetime

APP_VERSION = "V0.4.3"


def _base_dir() -> Path:
    # Nuitka / frozen executable first, normal script otherwise.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    try:
        return Path(__file__).resolve().parent
    except Exception:
        return Path.cwd()


def _log_error(title: str, exc_text: str) -> Path:
    base = _base_dir()
    log_path = base / "Pdect_startup_error.log"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(f"\n[{stamp}] {title}\n{exc_text}\n")
    except Exception:
        # Fallback to temp / user home if app folder is read-only.
        try:
            log_path = Path.home() / "Pdect_startup_error.log"
            with log_path.open("a", encoding="utf-8") as f:
                f.write(f"\n[{stamp}] {title}\n{exc_text}\n")
        except Exception:
            pass
    return log_path


def _show_error(title: str, message: str) -> None:
    # Prefer Qt if already available, but do not require it just to show startup errors.
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance()
        owns_app = app is None
        if owns_app:
            app = QApplication(sys.argv[:1])
        QMessageBox.critical(None, title, message)
        if owns_app:
            app.quit()
        return
    except Exception:
        pass
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
        return
    except Exception:
        pass
    # Last resort: on .py this is visible; on .pyw it still avoids a secondary crash.
    try:
        print(f"{title}: {message}", file=sys.stderr)
    except Exception:
        pass


def _candidate_dirs(base: Path) -> list[Path]:
    dirs: list[Path] = [base, base.parent]
    for name in ("app", "src", "Pdect", "pdect", "lib"):
        dirs.append(base / name)
        dirs.append(base.parent / name)
    # preserve order while removing duplicates
    seen = set()
    out = []
    for d in dirs:
        key = str(d.resolve(strict=False)).casefold()
        if key not in seen:
            seen.add(key)
            out.append(d)
    return out


def _locate_pdect_app() -> Path | None:
    base = _base_dir()
    for d in _candidate_dirs(base):
        p = d / "pdect_app.py"
        if p.is_file():
            return p
    # Shallow recursive fallback, deliberately bounded.
    for root in (base, base.parent):
        try:
            for p in root.glob("*/pdect_app.py"):
                if p.is_file():
                    return p
        except Exception:
            pass
    return None


def _load_module_from_path(name: str, path: Path):
    parent = str(path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"無法建立模組載入器：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _install_optional_extension(pdect_app) -> None:
    base = _base_dir()
    ext_path = None
    for d in _candidate_dirs(base):
        p = d / "pdect_recovery_ext.py"
        if p.is_file():
            ext_path = p
            break
    if ext_path is None:
        # Extension absent => simply run original Pdect.
        return
    try:
        ext = _load_module_from_path("pdect_recovery_ext", ext_path)
        install = getattr(ext, "install", None)
        if callable(install):
            install(pdect_app)
    except Exception:
        # Fail-open by design: extension problems must never block Pdect startup.
        _log_error("快速儲存 / 背景預存擴充載入失敗（已略過）", traceback.format_exc())


def main() -> int:
    app_path = _locate_pdect_app()
    if app_path is None:
        msg = (
            "找不到 Pdect 主程式模組：pdect_app.py\n\n"
            "你目前執行的是啟動器，實際程式內容在 pdect_app.py。\n"
            "請把 Pdect_V0.4.3.pyw、pdect_recovery_ext.py 和原本的 pdect_app.py\n"
            "放在同一個資料夾後再執行。\n\n"
            "程式不會再直接閃退。"
        )
        log = _log_error("找不到 pdect_app.py", msg)
        _show_error(f"P找碴 {APP_VERSION}", f"{msg}\n\n錯誤紀錄：{log}")
        return 2

    try:
        pdect_app = _load_module_from_path("pdect_app", app_path)
    except Exception:
        details = traceback.format_exc()
        log = _log_error("pdect_app.py 載入失敗", details)
        _show_error(
            f"P找碴 {APP_VERSION}",
            "Pdect 主程式載入失敗。\n\n"
            f"主程式：{app_path}\n"
            f"錯誤紀錄：{log}\n\n"
            "請把這個 log 提供給我，我可以直接定位錯誤。",
        )
        return 3

    # Optional feature extension. Any exception is swallowed and logged.
    _install_optional_extension(pdect_app)

    original_main = getattr(pdect_app, "main", None)
    if not callable(original_main):
        msg = f"pdect_app.py 中找不到 main()：{app_path}"
        log = _log_error("main() 不存在", msg)
        _show_error(f"P找碴 {APP_VERSION}", f"{msg}\n\n錯誤紀錄：{log}")
        return 4

    try:
        result = original_main()
        return int(result or 0)
    except SystemExit as e:
        code = e.code
        return int(code) if isinstance(code, int) else 0
    except Exception:
        details = traceback.format_exc()
        log = _log_error("Pdect 執行期間未處理例外", details)
        _show_error(
            f"P找碴 {APP_VERSION}",
            "Pdect 執行時發生錯誤，已留下紀錄，不再無訊息閃退。\n\n"
            f"錯誤紀錄：{log}",
        )
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
