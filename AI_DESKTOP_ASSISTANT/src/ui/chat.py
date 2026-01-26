# ==========================================================
# CHAT WINDOW (CLEAN & STABLE)
# ==========================================================

from pathlib import Path
from threading import Thread

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from src.services.ai import ask_ai
from src.services.speech import start_auto_listening, stop_auto_listening
from src.core.window_snap import WindowSnapManager


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
ICON_PATH = BASE_DIR / "assets" / "icons" / "Ai_i.PNG"


# ==========================================================
# CHAT WINDOW
# ==========================================================

class ChatWindow(QWidget):
    ai_ready = pyqtSignal(str, str)

    WIDTH_RATIO = 0.48
    HEIGHT = 100
    ANSWER_GAP = 10

    def __init__(self):
        super().__init__(
            flags=Qt.FramelessWindowHint |
                  Qt.WindowStaysOnTopHint |
                  Qt.Tool
        )
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_KeyboardFocusChange)

        self._busy = False
        self.is_listening = False
        self.dragging = False
        self._drag_pos = None

        # callbacks (wired in main.py)
        self.on_close = None   # restore toolbar
        self.on_hide = None    # global hide (bubble)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ai_ready.connect(self._handle_ai_response)

        self._setup_dimensions()
        self._build_ui()

    # ------------------------------------------------------
    # SETUP
    # ------------------------------------------------------

    def _setup_dimensions(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * self.WIDTH_RATIO), self.HEIGHT)
        self.move((screen.width() - self.width()) // 2, -10)
        self.setObjectName("shareOverlayRoot")

    def _load_icon(self, size=32):
        if ICON_PATH.exists():
            return QPixmap(str(ICON_PATH)).scaled(
                size, size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        return None

    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    def _build_ui(self):
        bg = QWidget(self)
        bg.setObjectName("toolbarContainer")
        bg.setGeometry(0, 0, self.width(), self.height())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 10)
        layout.setSpacing(2)

        layout.addLayout(self._build_top_bar())
        layout.addLayout(self._build_input_row())

    def _build_top_bar(self):
        row = QHBoxLayout()

        icon = QLabel()
        if pix := self._load_icon():
            icon.setPixmap(pix)

        title = QLabel("NovaDhi AI")
        title.setStyleSheet(
            "color:white;font-size:18px;font-weight:bold;"
        )

        hide_btn = self._btn("Hide", 65)
        hide_btn.clicked.connect(self.hide_request)

        self.stop_btn = self._btn("Stop Listening 🔴", 180)
        self.stop_btn.clicked.connect(self.toggle_listening)

        exit_btn = self._btn("Exit", 60, red=True)
        exit_btn.clicked.connect(self.close_overlay)

        row.addWidget(icon)
        row.addWidget(title)
        row.addStretch()
        row.addWidget(hide_btn)
        row.addWidget(self.stop_btn)
        row.addWidget(exit_btn)

        return row

    def _build_input_row(self):
        row = QHBoxLayout()

        self.text_input = QLineEdit()
        self.text_input.installEventFilter(self)
        self.text_input.setObjectName("overlayInput")
        self.text_input.setPlaceholderText("Say something or type here...")
        self.text_input.setFixedHeight(36)
        self.text_input.returnPressed.connect(self.send_text)

        send_btn = self._btn("Send", 70)
        send_btn.setFixedHeight(36)
        send_btn.clicked.connect(self.send_text)

        row.addWidget(self.text_input)
        row.addWidget(send_btn)

        return row

    def _btn(self, text, width, red=False):
        btn = QPushButton(text)
        btn.setFixedSize(width, 34)
        btn.setObjectName("redBtn" if red else "blackBtn")
        btn.setStyleSheet("text-align: center;")
        return btn

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def send_text(self):
        if self._busy:
            return

        text = self.text_input.text().strip()
        if not text:
            return

        self._busy = True
        self.text_input.clear()
        self._show_answer(text, "⏳ Thinking...")

        Thread(
            target=self._ai_worker,
            args=(text,),
            daemon=True
        ).start()

    def _ai_worker(self, text):
        reply = ask_ai(text)
        self.ai_ready.emit(text, reply)

    def toggle_listening(self):
        if self.is_listening:
            stop_auto_listening()
            self.stop_btn.setText("Start Listening 🟢")
            self.is_listening = False
            return

        start_auto_listening(self._thread_safe_callback)
        self.stop_btn.setText("Listening... 🔴")
        self.is_listening = True

    # ------------------------------------------------------
    # CLOSE / HIDE
    # ------------------------------------------------------

    def close_overlay(self):
        if self.is_listening:
            stop_auto_listening()
            self.is_listening = False
            self.stop_btn.setText("Start Listening 🟢")

        self.hide()

        if hasattr(self, "answer_window"):
            self.answer_window.hide()

        if self.on_close:
            self.on_close()   # restore toolbar

    def hide_request(self):
        self.hide()

        if hasattr(self, "answer_window"):
            self.answer_window.hide()

        if self.on_hide:
            self.on_hide()    # global hide (bubble)

    # ------------------------------------------------------
    # AI RESPONSE
    # ------------------------------------------------------

    def _thread_safe_callback(self, user_text, ai_reply):
        self.ai_ready.emit(user_text, ai_reply)

    def _handle_ai_response(self, user_text, ai_reply):
        self._busy = False
        self.text_input.setText(user_text)
        self._show_answer(user_text, ai_reply)

    def _show_answer(self, user_text, ai_reply):
        if not hasattr(self, "answer_window"):
            return

        self.answer_window.set_response(user_text, ai_reply)
        self._sync_answer_window()
        self.answer_window.show()
        self.answer_window.raise_()

    # ------------------------------------------------------
    # DRAG + ANSWER FOLLOW
    # ------------------------------------------------------

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.activateWindow()
            self.setFocus()
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            self.dragging = True


    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            self._sync_answer_window()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def _sync_answer_window(self):
        if hasattr(self, "answer_window"):
            self.answer_window.move(
                self.x(),
                self.y() + self.height() + self.ANSWER_GAP
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

        # keep answer window synced
        self._sync_answer_window()


    def eventFilter(self, obj, event):
        if obj == self.text_input and event.type() == event.KeyPress:
            if event.modifiers() == Qt.ControlModifier and event.key() in (
                Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right
            ):
                self.keyPressEvent(event)
                return True
        return super().eventFilter(obj, event)
