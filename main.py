import sys
from gui import ShapeApp
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
win = ShapeApp()
win.show()
sys.exit(app.exec())