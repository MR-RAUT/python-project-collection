# ==========================================================
# GLOBAL HOTKEY MANAGER (QT-SAFE & RELIABLE)
# ==========================================================

import keyboard
from PyQt5.QtCore import QObject, pyqtSignal


class GlobalHotkeyManager(QObject):
    toggle_requested = pyqtSignal()

    def __init__(self, toolbar):
        super().__init__()
        self.toolbar = toolbar
        self._registered = False

        self.toggle_requested.connect(self.toolbar.hotkey_toggle)

    def start(self):
        if self._registered:
            return

        keyboard.add_hotkey(
            "ctrl+alt+space",
            self._on_hotkey,
            suppress=False
        )
        self._registered = True

    def stop(self):
        if self._registered:
            keyboard.clear_all_hotkeys()
            self._registered = False

    def _on_hotkey(self):
        self.toggle_requested.emit()

