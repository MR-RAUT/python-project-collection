import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication

from src.ui.toolbar import AssistantToolbar
from src.ui.chat import ChatWindow
from src.ui.analyzer import ScreenAnalyzer
from src.ui.answer import AnswerWindow
from src.core.stealth import StealthManager
from src.core.hotkeys import GlobalHotkeyManager


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"


# ==========================================================
# STYLES
# ==========================================================

def load_styles(app):
    style = ""

    for name in ("styles.qss", "scrollbar.qss"):
        path = ASSETS_DIR / name
        if path.exists():
            style += path.read_text() + "\n"

    app.setStyleSheet(style)


# ==========================================================
# APP ENTRY
# ==========================================================

def run_app():
    app = QApplication(sys.argv)
    load_styles(app)

    # ---------------- WINDOWS ----------------
    chat = ChatWindow()
    analyzer = ScreenAnalyzer()
    answer = AnswerWindow()

    # answer follows chat / analyzer
    chat.answer_window = answer
    analyzer.answer_window = answer

    # answer close hides only answer
    answer.on_close = answer.hide

    windows = {
        "chat": chat,
        "analyzer": analyzer
    }

    # ---------------- TOOLBAR ----------------
    toolbar = AssistantToolbar(windows)
    windows["toolbar"] = toolbar
    toolbar.show()

    # ---------------- HIDE (bubble mode) ----------------
    chat.on_hide = toolbar.icon_hide
    analyzer.on_hide = toolbar.icon_hide

    # ---------------- CLOSE (restore toolbar) ----------------
    chat.on_close = toolbar.restore_toolbar_from_popup
    analyzer.on_close = toolbar.restore_toolbar_from_popup

    # ---------------- HOTKEYS ----------------
    hotkeys = GlobalHotkeyManager(toolbar)
    hotkeys.start()

    # ---------------- STEALTH ----------------
    stealth = StealthManager(windows)
    stealth.stealth_required.connect(
        lambda active: (
            toolbar.hard_hide() if active else toolbar.hard_restore()
        )
    )
    stealth.start()

    sys.exit(app.exec_())
