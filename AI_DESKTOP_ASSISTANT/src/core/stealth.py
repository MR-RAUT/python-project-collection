
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from src.core.windows_api import set_window_no_capture, is_desktop_share_active


class StealthManager(QObject):
    stealth_required = pyqtSignal(bool)  # True = enter, False = exit

    def __init__(self, windows: dict, interval=800):
        super().__init__()
        self.windows = windows
        self.interval = interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.guard)

        self._last_state = None

    def start(self):
        self.apply_protection()
        self.timer.start(self.interval)

    # ---------- CORE LOOP ----------
    def guard(self):
        self.apply_protection()

        tb = self.windows.get("toolbar")
        if tb and getattr(tb, "hard_hidden", False):
            return  # 🔥 DO NOTHING if hard hidden

        active = is_desktop_share_active()

        if active != self._last_state:
            self.stealth_required.emit(active)
            self._last_state = active


    # ---------- PROTECTION ----------
    def apply_protection(self):
        for win in self.windows.values():
            try:
                set_window_no_capture(int(win.winId()))
            except:
                pass
