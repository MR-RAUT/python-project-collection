from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QHBoxLayout, QStackedLayout, QApplication
)
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
)
from PyQt5.QtGui import QPixmap

import os
import time
from pathlib import Path
from enum import Enum
from typing import Optional

if os.name == "nt":
    import win32gui
    import win32con

from src.services.chatgpt import (
    auto_open_chatgpt,
    find_chatgpt_window,
    move_window_below_toolbar,
    make_window_transparent
)
from src.core.windows_api import set_window_no_capture
from src.core.window_snap import WindowSnapManager


# ==========================================================
# UI STATE
# ==========================================================

class UIState(Enum):
    FULL = 1
    BUBBLE = 2


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
ICON_PATH = BASE_DIR / "assets" / "icons" / "Ai_i.PNG"


# ==========================================================
# CLICKABLE LABEL
# ==========================================================

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


# ==========================================================
# ASSISTANT TOOLBAR
# ==========================================================

class AssistantToolbar(QWidget):

    TOOLBAR_HEIGHT = 56
    COLLAPSED_WIDTH = 56   # 🔥 MUST MATCH HEIGHT


    def __init__(self, windows: dict):
        super().__init__(
            flags=Qt.FramelessWindowHint |
                  Qt.WindowStaysOnTopHint |
                  Qt.Tool
        )
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_KeyboardFocusChange)


        self.windows = windows
        self.ui_state = UIState.FULL
        self.hard_hidden = False
        self._drag_pos = None
        self._anim = None

        self.setAttribute(Qt.WA_TranslucentBackground)

        self._setup_dimensions()
        self._build_widgets()
        self._build_layout()
        self._connect_signals()

    # ------------------------------------------------------
    # SETUP
    # ------------------------------------------------------

    def _setup_dimensions(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.normal_width = int(screen.width() * 0.48)
        self.setFixedHeight(self.TOOLBAR_HEIGHT)
        self.resize(self.normal_width, self.TOOLBAR_HEIGHT)
        self._center_top()

    def _load_icon(self, size: int) -> Optional[QPixmap]:
        if ICON_PATH.exists():
            return QPixmap(str(ICON_PATH)).scaled(
                size, size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        return None

    def _btn(self, text, width, red=False):
        btn = QPushButton(text)
        btn.setFixedSize(width, 34)
        btn.setObjectName("redBtn" if red else "blackBtn")
        btn.setStyleSheet("text-align: center;")
        return btn


    # ==========================================================
    # UI BUILD
    # ==========================================================

    def _build_widgets(self):
        # ---- Icons ----
        self.icon_label = ClickableLabel()
        self.bubble_icon = ClickableLabel()

        if icon := self._load_icon(34):
            self.icon_label.setPixmap(icon)

        # 🔥 Bubble icon (perfect circle base)
        self.bubble_icon.setFixedSize(44, 44)
        self.bubble_icon.setAlignment(Qt.AlignCenter)
        self.bubble_icon.setObjectName("bubbleIcon")

        if icon := self._load_icon(20):
            self.bubble_icon.setPixmap(icon)

        # ---- Title ----
        self.title = QLabel("NovaDhi AI")
        self.title.setStyleSheet(
            "color:white;font-size:18px;font-weight:bold;"
        )

        # ---- Buttons ----
        self.ai_btn = self._btn("AI Help ✨", 115)
        self.analyze_btn = self._btn("Analyze Screen 🖥️", 180)
        self.chat_btn = self._btn("Chat", 65)
        self.hide_btn = self._btn("Hide", 65)
        self.exit_btn = self._btn("Exit", 60, red=True)


    def _build_layout(self):
        self.container = QWidget(self)
        self.container.setObjectName("toolbarContainer")
        self.container.setFixedSize(
            self.normal_width - 12,
            self.TOOLBAR_HEIGHT - 12
        )
        self.container.move(6, 6)

        self.stacked = QStackedLayout(self.container)
        self.stacked.setContentsMargins(0, 0, 0, 0)

        self._build_full_page()
        self._build_bubble_page()

        self.stacked.setCurrentIndex(0)


    def _build_full_page(self):
        root = QHBoxLayout()
        root.setContentsMargins(10, 6, 10, 6)
        root.setSpacing(12)

        # ---- Left (Icon + Title) ----
        left = QHBoxLayout()
        left.setSpacing(8)
        left.addWidget(self.icon_label)
        left.addWidget(self.title)

        # ---- Center (Main Buttons) ----
        center = QHBoxLayout()
        center.setSpacing(12)
        for btn in (self.ai_btn, self.analyze_btn, self.chat_btn):
            center.addWidget(btn)

        # ---- Right (Hide / Exit) ----
        right = QHBoxLayout()
        right.setSpacing(10)
        right.addWidget(self.hide_btn)
        right.addWidget(self.exit_btn)

        root.addLayout(left)
        root.addStretch()
        root.addLayout(center)
        root.addStretch()
        root.addLayout(right)

        page = QWidget()
        page.setLayout(root)
        self.stacked.addWidget(page)


    def _build_bubble_page(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch()
        layout.addWidget(self.bubble_icon)
        layout.addStretch()

        page = QWidget()
        page.setLayout(layout)
        self.stacked.addWidget(page)


    def _connect_signals(self):
        self.icon_label.clicked.connect(self.toggle)
        self.bubble_icon.clicked.connect(self.toggle)

        self.hide_btn.clicked.connect(self.icon_hide)
        self.exit_btn.clicked.connect(QApplication.quit)

        self.ai_btn.clicked.connect(self.show_answer)
        self.chat_btn.clicked.connect(lambda: self._show_popup("chat"))
        self.analyze_btn.clicked.connect(lambda: self._show_popup("analyzer"))

    # ------------------------------------------------------
    # TOGGLE / HIDE / RESTORE
    # ------------------------------------------------------

    def toggle(self):
        if self.ui_state == UIState.FULL:
            self.icon_hide()
        else:
            self.icon_restore()

    def icon_hide(self):
        self.hard_hidden = False
        self.ui_state = UIState.BUBBLE

        for key, win in self.windows.items():
            if key != "toolbar":
                try:
                    win.hide()
                except:
                    pass

        self.setVisible(True)
        self.collapse()

    def icon_restore(self):
        self.setVisible(True)
        self.raise_()
        self.ui_state = UIState.FULL
        self.expand()

    # ------------------------------------------------------
    # HARD HIDE (HOTKEY / STEALTH)
    # ------------------------------------------------------

    def hotkey_toggle(self):
        self.hard_restore() if self.hard_hidden else self.hard_hide()

    def hard_hide(self):
        self.hard_hidden = True
        self.setVisible(False)

        for win in self.windows.values():
            try:
                win.hide()
            except:
                pass

    def hard_restore(self):
        self.hard_hidden = False
        self.setVisible(True)
        self.raise_()

        if self.ui_state == UIState.FULL:
            self.expand()
        else:
            self.collapse()

    # ------------------------------------------------------
    # POPUPS
    # ------------------------------------------------------

    def _show_popup(self, key):
        for k in ("chat", "analyzer"):
            if win := self.windows.get(k):
                win.hide()

        win = self.windows.get(key)
        if not win:
            return

        screen = QApplication.primaryScreen().availableGeometry()
        win.move(
            (screen.width() - win.width()) // 2,
            int(screen.height() * 0.01)
        )

        win.on_close = self.restore_toolbar_from_popup
        win.show()
        win.raise_()
        win.activateWindow()

        self.setVisible(False)

        if os.name == "nt":
            set_window_no_capture(int(win.winId()))

    def restore_toolbar_from_popup(self):
        self.hard_hidden = False
        self.setVisible(True)
        self.raise_()

        if self.ui_state == UIState.FULL:
            self.expand()
        else:
            self.collapse()

    # ------------------------------------------------------
    # CHATGPT WINDOW
    # ------------------------------------------------------

    def show_answer(self):
        hwnd = find_chatgpt_window() or (
            auto_open_chatgpt() and time.sleep(3) or find_chatgpt_window()
        )
        if not hwnd:
            return

        make_window_transparent(hwnd, 30)
        move_window_below_toolbar(hwnd, self)

        if os.name == "nt":
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except:
                pass

    # ------------------------------------------------------
    # ANIMATION
    # ------------------------------------------------------

    def collapse(self):
        for w in (
            self.title, self.ai_btn,
            self.analyze_btn, self.chat_btn,
            self.hide_btn, self.exit_btn
        ):
            w.hide()

        self._animate(self.width(), self.COLLAPSED_WIDTH)
        self.container.setFixedWidth(self.COLLAPSED_WIDTH - 12)
        self.stacked.setCurrentIndex(1)

    def expand(self):
        self._animate(self.width(), self.normal_width)
        self.container.setFixedWidth(self.normal_width - 12)
        self.stacked.setCurrentIndex(0)

        for w in (
            self.title, self.ai_btn,
            self.analyze_btn, self.chat_btn,
            self.hide_btn, self.exit_btn
        ):
            w.show()

        self._center_top()

    def _animate(self, start, end):
        if self._anim:
            self._anim.stop()

        rect = self.geometry()
        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(260)
        self._anim.setStartValue(QRect(rect.x(), rect.y(), start, rect.height()))
        self._anim.setEndValue(QRect(rect.x(), rect.y(), end, rect.height()))
        self._anim.setEasingCurve(QEasingCurve.InOutCubic)
        self._anim.start()

    # ------------------------------------------------------
    # DRAG
    # ------------------------------------------------------

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.activateWindow()
            self.setFocus()
            self._drag_pos = e.globalPos() - self.frameGeometry().topLeft()


    def mouseMoveEvent(self, e):
        if self._drag_pos:
            self.move(e.globalPos() - self._drag_pos)

            if hwnd := find_chatgpt_window():
                move_window_below_toolbar(hwnd, self)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None

    def _center_top(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            (screen.width() - self.normal_width) // 2,
            10
        )
        
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()
        self.raise_()
        self.setFocus()


    def keyPressEvent(self, event):
        if event.modifiers() != Qt.ControlModifier:
            return super().keyPressEvent(event)

        row, col = WindowSnapManager.detect(self)

        if event.key() == Qt.Key_Up:
            row = max(0, row - 1)

        elif event.key() == Qt.Key_Down:
            row = min(2, row + 1)

        elif event.key() == Qt.Key_Left:
            col = max(0, col - 1)

        elif event.key() == Qt.Key_Right:
            col = min(2, col + 1)

        else:
            return super().keyPressEvent(event)

        target = WindowSnapManager.GRID[row][col]
        WindowSnapManager.snap(self, target)
        
    def icon_restore(self):
        self.setVisible(True)
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.ui_state = UIState.FULL
        self.expand()

    def hard_restore(self):
        self.hard_hidden = False
        self.setVisible(True)
        self.raise_()
        self.activateWindow()
        self.setFocus()

