import ctypes
from ctypes import wintypes

import win32gui
import win32con
import win32process
import win32api
import psutil


# ==========================================================
# BASIC WINDOW HELPERS
# ==========================================================

def move_window(hwnd, x, y, width, height):
    """Move and resize a window safely."""
    try:
        win32gui.MoveWindow(hwnd, x, y, width, height, True)
    except:
        pass


def make_window_transparent(hwnd, opacity=200):
    """
    opacity: 0 (invisible) → 255 (opaque)
    """
    try:
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            style | win32con.WS_EX_LAYERED
        )
        win32gui.SetLayeredWindowAttributes(
            hwnd, 0, opacity, win32con.LWA_ALPHA
        )
    except:
        pass


# ==========================================================
# NO-CAPTURE / STEALTH PROTECTION
# ==========================================================

user32 = ctypes.windll.user32
WDA_MONITOR = 1


def set_window_no_capture(hwnd):
    """Prevent window from being captured or screen-shared."""
    try:
        ex = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            ex | win32con.WS_EX_LAYERED | 0x00200000
        )
        user32.SetWindowDisplayAffinity(
            wintypes.HWND(hwnd),
            wintypes.DWORD(WDA_MONITOR)
        )
    except:
        pass


# ==========================================================
# MEETING / SCREEN SHARE DETECTION
# ==========================================================

MEETING_APPS = {
    "zoom.exe", "teams.exe", "msedge.exe",
    "chrome.exe", "firefox.exe"
}

KEYWORDS = ("share", "meet", "meeting", "zoom", "teams")


def is_desktop_share_active():
    """Detect if a meeting or screen-share app is active."""
    active = False

    def enum(hwnd, _):
        nonlocal active
        if active or not win32gui.IsWindowVisible(hwnd):
            return
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            name = proc.name().lower()
            title = win32gui.GetWindowText(hwnd).lower()

            if name in MEETING_APPS and any(k in title for k in KEYWORDS):
                active = True
        except:
            pass

    win32gui.EnumWindows(enum, None)
    return active


# ==========================================================
# PUBLIC API (OPTIONAL BUT RECOMMENDED)
# ==========================================================

__all__ = [
    "move_window",
    "make_window_transparent",
    "set_window_no_capture",
    "is_desktop_share_active",
]
