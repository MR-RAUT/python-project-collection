from PyQt5.QtWidgets import QApplication

class WindowSnapManager:
    GRID = [
        ["top_left", "top_center", "top_right"],
        ["mid_left", "mid_center", "mid_right"],
        ["bot_left", "bot_center", "bot_right"]
    ]

    POS = {
        "top_left": (0, 0),
        "top_center": (0.5, 0),
        "top_right": (1, 0),

        "mid_left": (0, 0.5),
        "mid_center": (0.5, 0.5),
        "mid_right": (1, 0.5),

        "bot_left": (0, 1),
        "bot_center": (0.5, 1),
        "bot_right": (1, 1),
    }

    @staticmethod
    def snap(widget, key):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = widget.width(), widget.height()

        x_ratio, y_ratio = WindowSnapManager.POS[key]
        x = int(screen.x() + (screen.width() - w) * x_ratio)
        y = int(screen.y() + (screen.height() - h) * y_ratio)

        widget.move(x, y)

    @staticmethod
    def detect(widget):
        screen = QApplication.primaryScreen().availableGeometry()
        geo = widget.geometry()

        cx = geo.x() + geo.width() / 2
        cy = geo.y() + geo.height() / 2

        col = 0 if cx < screen.width() * 0.33 else \
              2 if cx > screen.width() * 0.66 else 1

        row = 0 if cy < screen.height() * 0.33 else \
              2 if cy > screen.height() * 0.66 else 1

        return row, col
