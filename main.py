from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
import sys

from api import Photospot, Touristmap, Touristfood, Touristhotel, Photospotscreen

#UI파일 연결 코드
UI_class = uic.loadUiType("UI/mainui.ui")[0]


# 시도군구 default 값
sido = '서울특별시'
gungu = '서대문구'

# Main Window
class MyWindow(QMainWindow, QWidget, UI_class):
    def __init__(self):
        super().__init__()
        self.myApp = None

        self.setWindowTitle('Travel Manager - Main')
        self.setupUi(self)
        self.btnget.clicked.connect(self.getinfoFunction)
        self.btn1.clicked.connect(self.button1Function)  
        self.btn2.clicked.connect(self.button2Function)
        self.btn3.clicked.connect(self.button3Function)
        self.btn4.clicked.connect(self.button_btn4Function) 

    #관광지 지도
    def button1Function(self):
        self.hide()
        self.myApp = Touristmap(sido, gungu)
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    #관광지 포토스팟
    def button2Function(self):
        app = Photospot()
        app.run(place=sido)
        self.hide()
        self.myApp = Photospotscreen(app.result)
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    #관광지 대표음식
    def button3Function(self):
        self.hide()
        self.myApp = Touristfood(sido)
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    #관광지 숙소
    def button_btn4Function(self):
        self.hide()
        self.myApp = Touristhotel(sido, gungu)
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    #입력 완료 버튼
    def getinfoFunction(self):
        global sido, gungu
        sido = self.sido_info.text()
        gungu = self.gungu_info.text()

app = QApplication(sys.argv)

Window = MyWindow()

Window.show()

app.exec_()