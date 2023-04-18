from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

UIbtn2_class = uic.loadUiType("./UI/photospotui.ui")[0]
class Photospotscreen(QWidget, UIbtn2_class):
    closed = pyqtSignal()
    def __init__(self, result):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Travel Manager - Food')
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)
        self.result = result[1:]
        result = ', '.join(result)
        self.print.setText(result)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)