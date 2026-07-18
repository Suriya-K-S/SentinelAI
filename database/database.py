"""
SentinelAI Dashboard
Main Window (PySide6)
"""

import sys
try:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import (
        QApplication,
        QLabel,
        QMainWindow,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
        QHBoxLayout,
    )
except ImportError:
    print("PySide6 is not installed.")
    raise

from database.database import database



class _QTimerFallback:
    def __init__(self, *args, **kwargs):
        pass

    def timeout(self, *args, **kwargs):
        return self

    def connect(self, *args, **kwargs):
        pass

    def start(self, *args, **kwargs):
        pass



QTimer = _QTimerFallback
try:
    from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    class _SignalFallback:
        def connect(self, *args, **kwargs):
            pass

    class QApplication:
        def __init__(self, argv=None):
            self._argv = argv

        def exec(self):
            return 0

    class QLabel:
        def __init__(self, text=""):
            self._text = text

        def setText(self, text):
            self._text = text

    class QMainWindow:
        def __init__(self):
            pass

        def setWindowTitle(self, title):
            self._title = title

        def resize(self, w, h):
            self._size = (w, h)

        def setCentralWidget(self, w):
            self._central = w

        def show(self):
            pass

    class QPushButton:
        def __init__(self, text=""):
            self.text = text
            self.clicked = _SignalFallback()

        def setText(self, text):
            self.text = text

    class QTableWidget:
        def __init__(self, rows=0, cols=0):
            self._rows = rows
            self._cols = cols
            self._items = {}

        def setHorizontalHeaderLabels(self, labels):
            self._headers = labels

        def horizontalHeader(self):
            class _H:
                def setStretchLastSection(self, val):
                    pass

            return _H()

        def setRowCount(self, r):
            self._rows = r

        def setItem(self, r, c, item):
            self._items[(r, c)] = item

    class QTableWidgetItem:
        def __init__(self, val=""):
            self.val = val

        def setBackground(self, bg):
            self._bg = bg

    class QVBoxLayout:
        def __init__(self, parent=None):
            self.parent = parent

        def addWidget(self, w):
            pass

        def addLayout(self, l):
            pass

    class QHBoxLayout(QVBoxLayout):
        def addStretch(self):
            pass

    class QWidget:
        def __init__(self):
            pass


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SentinelAI Dashboard")
        self.resize(1000, 650)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.status = QLabel("SentinelAI Status: Running")
        layout.addWidget(self.status)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Module", "Severity", "Description"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        row = QHBoxLayout()
        btn = QPushButton("Refresh")
        btn.clicked.connect(self.refresh_events)
        row.addWidget(btn)
        row.addWidget(QPushButton("Export"))
        row.addWidget(QPushButton("Settings"))
        row.addStretch()
        layout.addLayout(row)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_events)
        self.timer.start(2000)

        self.refresh_events()

    def refresh_events(self):
        data = [
            ("13:10", "USB", "WARNING", "Unknown USB inserted"),
            ("13:15", "NETWORK", "INFO", "Internet Connected"),
            ("13:18", "LOGIN", "INFO", "User Logged In")
        ]
        self.table.setRowCount(len(data))
        for r, vals in enumerate(data):
            for c, val in enumerate(vals):
                item = QTableWidgetItem(val)
                if c == 2 and val == "WARNING":
                    item.setBackground(Qt.yellow)
                self.table.setItem(r, c, item)

def main():
    app = QApplication(sys.argv)
    w = DashboardWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
