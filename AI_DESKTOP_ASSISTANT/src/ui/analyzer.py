# ==========================================================
# SCREEN ANALYZER OVERLAY (CLEAN & STABLE)
# ==========================================================

from pathlib import Path
from threading import Thread

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

from src.core.screen_analyzer_engine import ScreenAnalyzerEngine
from src.services.ai import ask_ai
from src.core.window_snap import WindowSnapManager


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
ICON_PATH = BASE_DIR / "assets" / "icons" / "Ai_i.PNG"

# ==========================================================
# SCREEN ANALYZER
# ==========================================================

class ScreenAnalyzer(QWidget):
    ai_ready = pyqtSignal(str)

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

        # callbacks (wired in main.py)
        self.on_close = None   # restore toolbar
        self.on_hide = None    # global hide (bubble)

        self.engine = ScreenAnalyzerEngine()
        self.ai_ready.connect(self._on_ai_result)

        self._drag_pos = None
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._setup_dimensions()
        self._build_ui()

    # ------------------------------------------------------
    # SETUP
    # ------------------------------------------------------

    def _setup_dimensions(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * self.WIDTH_RATIO), self.HEIGHT)
        self.move((screen.width() - self.width()) // 2, 8)

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
        layout.addWidget(self._build_input())

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

        self.analyze_btn = self._btn("Analyze Screen", 168)
        self.analyze_btn.clicked.connect(self.analyze_screen)

        exit_btn = self._btn("Exit", 60, red=True)
        exit_btn.clicked.connect(self.close_overlay)

        row.addWidget(icon)
        row.addWidget(title)
        row.addStretch()
        row.addWidget(hide_btn)
        row.addWidget(self.analyze_btn)
        row.addWidget(exit_btn)

        return row

    def _build_input(self):
        self.input_field = QLineEdit()
        self.input_field.installEventFilter(self)
        self.input_field.setObjectName("overlayInput")
        self.input_field.setPlaceholderText(
            "Click Analyze to read the screen"
        )
        self.input_field.setFixedHeight(36)
        return self.input_field

    def _btn(self, text, width, red=False):
        btn = QPushButton(text)
        btn.setFixedSize(width, 34)
        btn.setObjectName("redBtn" if red else "blackBtn")
        btn.setStyleSheet("text-align: center;")
        return btn

    # ------------------------------------------------------
    # ANALYSIS LOGIC
    # ------------------------------------------------------

    def analyze_screen(self):
        self.analyze_btn.setEnabled(False)
        self.input_field.setText("🔍 Reading screen...")
        Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            screen_text = self.engine.capture_text()

            if not screen_text.strip():
                result = "❌ No readable text found on screen."
            else:
                prompt = self.engine.build_prompt(screen_text)
                result = ask_ai(prompt)

        except Exception as e:
            result = f"Analyzer error: {e}"

        self.ai_ready.emit(result)

    # ------------------------------------------------------
    # RESULT HANDLING
    # ------------------------------------------------------

    def _on_ai_result(self, text):
        self.analyze_btn.setEnabled(True)

        if hasattr(self, "answer_window"):
            self.answer_window.set_response("Screen Analysis", text)
            self._sync_answer_window()
            self.answer_window.show()
            self.answer_window.raise_()
        else:
            self.input_field.setText(text)

    # ------------------------------------------------------
    # ANSWER FOLLOW
    # ------------------------------------------------------

    def _sync_answer_window(self):
        if hasattr(self, "answer_window"):
            self.answer_window.move(
                self.x(),
                self.y() + self.height() + self.ANSWER_GAP
            )

    def moveEvent(self, event):
        super().moveEvent(event)
        self._sync_answer_window()

    # ------------------------------------------------------
    # CLOSE / HIDE
    # ------------------------------------------------------

    def close_overlay(self):
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

    def closeEvent(self, event):
        event.ignore()
        self.close_overlay()

    # ------------------------------------------------------
    # DRAG
    # ------------------------------------------------------

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.activateWindow()
            self.setFocus()
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()


    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            self._sync_answer_window()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()
        self.raise_()
        self.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.input_field and event.type() == event.KeyPress:
            if event.modifiers() == Qt.ControlModifier and event.key() in (
                Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right
            ):
                self.keyPressEvent(event)
                return True
        return super().eventFilter(obj, event)

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
        self._sync_answer_window()