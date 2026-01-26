import os
import time
import subprocess
import psutil
import win32gui
import win32process

from src.core.windows_api import move_window, make_window_transparent

# ---- ChatGPT Desktop Path ----
CHATGPT_EXACT_PATH = os.path.join(
    r"C:\Program Files\WindowsApps",
    r"OpenAI.ChatGPT-Desktop_1.2025.258.0_x64__2p2nqsd0c76g0\app\ChatGPT.exe"
)


# -------------------------------------------------
# Launch ChatGPT Desktop App
# -------------------------------------------------
def auto_open_chatgpt():
    if not os.path.exists(CHATGPT_EXACT_PATH):
        print("❌ ChatGPT.exe not found")
        return False

    try:
        subprocess.Popen([CHATGPT_EXACT_PATH], shell=True)
        time.sleep(3)
        return True
    except Exception as e:
        print("❌ Failed to launch ChatGPT:", e)
        return False


# -------------------------------------------------
# Find REAL ChatGPT Desktop Window
# -------------------------------------------------
def find_chatgpt_window():
    target_pid = None

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and "chatgpt" in proc.info['name'].lower():
                target_pid = proc.info['pid']
        except:
            pass

    if not target_pid:
        return None

    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == target_pid:
                result.append(hwnd)

    result = []
    win32gui.EnumWindows(enum_handler, result)
    return result[0] if result else None


# -------------------------------------------------
# Position ChatGPT below toolbar
# -------------------------------------------------
def move_window_below_toolbar(hwnd, toolbar, height=700):
    if not hwnd:
        return

    x = toolbar.x()
    y = toolbar.y() + toolbar.height() + 10
    width = toolbar.width()

    move_window(hwnd, x, y, width, height)
