# ==========================================================
# ANSWER WINDOW (CLEAN & STABLE)
# ==========================================================

import re
import pyperclip
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextBrowser,
    QVBoxLayout, QHBoxLayout, QScrollArea, QApplication
)
from PyQt5.QtCore import Qt, QFile, QTextStream, QSize
from PyQt5.QtGui import QFont, QIcon


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

ARROW_ICON = ICONS_DIR / "arrow.PNG"
SCROLLBAR_QSS = ASSETS_DIR / "scrollbar.qss"


# ==========================================================
# UTILITIES
# ==========================================================

def load_scrollbar_style(widget):
    file = QFile(str(SCROLLBAR_QSS))
    if file.open(QFile.ReadOnly | QFile.Text):
        widget.setStyleSheet(QTextStream(file).readAll())
        file.close()


# ==========================================================
# ANSWER WINDOW
# ==========================================================

class AnswerWindow(QWidget):
    def __init__(self):
        super().__init__(
            flags=Qt.FramelessWindowHint |
                  Qt.WindowStaysOnTopHint |
                  Qt.Tool
        )
        
        self.setFocusPolicy(Qt.NoFocus)
        self.on_close = None   # wired by parent (Analyzer / Chat)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self._setup_dimensions()
        self._build_ui()

    # ------------------------------------------------------
    # SETUP
    # ------------------------------------------------------

    def _setup_dimensions(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.48), 600)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(screen.width(), screen.height())
        self.move(screen.left() + 20, screen.top() + 20)

    def _build_ui(self):
        self.bg = QWidget(self)
        self.bg.setObjectName("popupContainer")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 30)
        self.main_layout.setSpacing(6)

        self._build_header()
        self._build_question()
        self._build_answer_area()
        self._build_resize_handle()

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    def _build_header(self):
        row = QHBoxLayout()

        self.question_label = QLabel("💬 Question:")
        self.question_label.setStyleSheet(
            "color:white;font-size:18px;font-weight:bold;"
        )

        close_btn = QPushButton(" × ")
        close_btn.setObjectName("redBtn")
        close_btn.setFixedSize(40, 30)
        close_btn.clicked.connect(self._close_child)

        row.addWidget(self.question_label)
        row.addStretch()
        row.addWidget(close_btn)

        self.main_layout.addLayout(row)

    # ------------------------------------------------------
    # QUESTION
    # ------------------------------------------------------

    def _build_question(self):
        self.question_scroll = QScrollArea()
        self.question_scroll.setWidgetResizable(True)
        self.question_scroll.setFixedHeight(10)
        self.question_scroll.setFrameShape(QScrollArea.NoFrame)
        self.question_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.question_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.question_scroll.setStyleSheet("background: transparent;")
        self.question_scroll.viewport().setStyleSheet("background: transparent;")

        load_scrollbar_style(self.question_scroll)

        container = QWidget()
        container.setStyleSheet("background: transparent;")

        self.question_text = QLabel("")
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet(
            "color:white;font-size:16px;background:transparent;"
        )

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.question_text)

        self.question_scroll.setWidget(container)
        self.main_layout.addWidget(self.question_scroll)

        self.answer_label = QLabel("⭐ Answer:")
        self.answer_label.setStyleSheet(
            "color:yellow;font-size:18px;font-weight:bold;"
        )
        self.main_layout.addWidget(self.answer_label)

    # ------------------------------------------------------
    # ANSWER AREA
    # ------------------------------------------------------

    def _build_answer_area(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setObjectName("answerScrollArea")

        load_scrollbar_style(scroll)

        container = QWidget()
        container.setStyleSheet("background:transparent;")

        self.answer_layout = QVBoxLayout(container)
        self.answer_layout.setSpacing(10)
        self.answer_layout.setAlignment(Qt.AlignTop)

        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

    # ------------------------------------------------------
    # RESIZE HANDLE
    # ------------------------------------------------------

    def _build_resize_handle(self):
        self.resize_handle = QPushButton(self)
        self.resize_handle.setObjectName("resizeHandleButton")
        self.resize_handle.setIcon(QIcon(str(ARROW_ICON)))
        self.resize_handle.setIconSize(QSize(14, 14))
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)
        self.resize_handle.setFixedSize(24, 24)

        self.resize_handle.mousePressEvent = self._start_resize
        self.resize_handle.mouseMoveEvent = self._do_resize

    def _start_resize(self, event):
        self._drag_start_pos = event.globalPos()
        self._drag_start_size = self.size()

    def _do_resize(self, event):
        if event.buttons() & Qt.LeftButton:
            dx = event.globalPos().x() - self._drag_start_pos.x()
            dy = event.globalPos().y() - self._drag_start_pos.y()

            self.resize(
                max(self.minimumWidth(),
                    min(self._drag_start_size.width() + dx, self.maximumWidth())),
                max(self.minimumHeight(),
                    min(self._drag_start_size.height() + dy, self.maximumHeight()))
            )

    # ------------------------------------------------------
    # CONTENT RENDERING
    # ------------------------------------------------------

    def set_response(self, question: str, answer: str):
        self.question_text.setText(question)

        fm = self.question_text.fontMetrics()
        lines = question.count("\n") + 1
        self.question_scroll.setFixedHeight(
            min(40, max(40, lines * fm.height() + 10))
        )

        self._clear_answer()
        self._render_answer(answer)

    def _clear_answer(self):
        while self.answer_layout.count():
            item = self.answer_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _render_answer(self, text: str):
        code_blocks = re.findall(r"```(.*?)\n(.*?)```", text, re.DOTALL)
        text_parts = re.split(r"```.*?```", text, flags=re.DOTALL)

        for i, part in enumerate(text_parts):
            part = part.strip()
            if part:
                label = QLabel(part.replace("\n", "<br>"))
                label.setWordWrap(True)
                label.setStyleSheet(
                    "color:white;font-size:16px;background:transparent;"
                )
                self.answer_layout.addWidget(label)

            if i < len(code_blocks):
                lang, code = code_blocks[i]
                self._add_code_block(lang, code)

    def _add_code_block(self, lang: str, code: str):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QHBoxLayout()
        header.addWidget(QLabel(f"<b>{lang or 'code'}</b>"))
        header.addStretch()

        copy_btn = QPushButton("📋 Copy")
        copy_btn.setObjectName("copyCodeBtn")
        copy_btn.clicked.connect(lambda _, c=code: pyperclip.copy(c))
        header.addWidget(copy_btn)

        layout.addLayout(header)

        box = QTextBrowser()
        box.setObjectName("codeBlockBox")
        box.setFont(QFont("Consolas", 11))
        box.setText(code)
        box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        fm = box.fontMetrics()
        box.setFixedHeight(len(code.splitlines()) * fm.height() + 20)

        layout.addWidget(box)
        self.answer_layout.addWidget(wrapper)

    # ------------------------------------------------------
    # EVENTS
    # ------------------------------------------------------

    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.width(), self.height())
        self.resize_handle.move(
            self.width() - self.resize_handle.width() - 13,
            self.height() - self.resize_handle.height() - 10
        )
        super().resizeEvent(event)

    def _close_child(self):
        self.hide()
        if self.on_close:
            self.on_close()

    def closeEvent(self, event):
        event.ignore()
        self._close_child()
