import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic   
import pandas as pd
import sys
import io
import folium as g
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

#UI파일 연결 코드
UI_class = uic.loadUiType("mainui.ui")[0]

#시도군구 default 값
sido = '서울특별시'
gungu = '서대문구'

# Main Window
class MyWindow(QMainWindow, QWidget, UI_class) :
    def __init__(self) :
        super().__init__()
        self.setWindowTitle('Travel Manger - Main')
        self.setupUi(self)

        self.btn_1.clicked.connect(self.button1Function) #관광지맵
        self.btn_get.clicked.connect(self.button2Function)

    def button1Function(self):
        self.hide()
        self.myApp = MapWindow()
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    def button2Function(self):
        global sido, gungu
        sido = self.sido_info.text()
        gungu = self.gungu_info.text()


# Map Window
class MapWindow(QWidget):
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Travel Manger - Map')
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        colums_to_keep = ['POI_NM','CL_NM','CTPRVN_NM','SIGNGU_NM','LC_LO','LC_LA','RDNMADR_NM', ]
        df = pd.read_csv('data.csv', encoding='utf-8', usecols = colums_to_keep)

        CTRVN_NM = sido #시도명
        SIGNGU_NM = gungu #시군구명

        ft_df = df[(df['CTPRVN_NM'] == CTRVN_NM) & (df['SIGNGU_NM'] == SIGNGU_NM)]

        first_row = ft_df.iloc[0]
        map = g.Map(
            location = [first_row['LC_LA'],first_row['LC_LO']],
            zoom_start =13,
            attr ='VworldBase'
        )

        for a in ft_df.index:
            LC_LA = ft_df.loc[a,"LC_LA"]
            LC_LO = ft_df.loc[a,"LC_LO"]
            POI_NM = ft_df.loc[a,"POI_NM"]
            CL_NM = ft_df.loc[a,"CL_NM"]
            CTPRVN_NM = ft_df.loc[a,"CTPRVN_NM"] #시도명
            SIGNGU_NM = ft_df.loc[a,"SIGNGU_NM"] #시군구명
            RDNMADR_NM = ft_df.loc[a,"RDNMADR_NM"] #도로명주소명
            popup = g.Popup(f'<b>{POI_NM}</b><br>종류 : {CL_NM}<br><br> 주소 : {CTPRVN_NM} {SIGNGU_NM} {RDNMADR_NM}',max_width=650)
            
            tooltip = POI_NM
            g.Marker([LC_LA, LC_LO], popup = popup, tooltip =tooltip).add_to(map)   

        # save map data to data object
        data = io.BytesIO()
        map.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

app = QApplication(sys.argv) 

Window = MyWindow() 

Window.show()

app.exec_()