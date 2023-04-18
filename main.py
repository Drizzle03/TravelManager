import sys 
import pandas as pd
import sys
import io
import folium as g
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic 

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

        self.btn1.clicked.connect(self.button1Function) #관광지맵
        self.btnget.clicked.connect(self.button2Function)
        self.btn4.clicked.connect(self.button_btn4Funtion) #숙소 후보

    def button1Function(self):
        self.hide()
        self.myApp = btn1Window()
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    def button2Function(self):
        global sido, gungu
        sido = self.sido_info.text()
        gungu = self.gungu_info.text()

    def button_btn4Funtion(self):
        self.hide()
        self.myApp = btn4Window()
        self.myApp.show()
        self.myApp.closed.connect(self.show)


# Map Window
class btn1Window(QWidget):
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Travel Manger - Map')
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        colums_to_keep = ['POI_NM','CL_NM','CTPRVN_NM','SIGNGU_NM','LC_LO','LC_LA','RDNMADR_NM']
        df = pd.read_csv('data1.csv', encoding='utf-8', usecols = colums_to_keep)

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
            LAT = ft_df.loc[a,"LC_LA"] #위도
            LONG = ft_df.loc[a,"LC_LO"] #경도
            POI_NM = ft_df.loc[a,"POI_NM"]#관광지 종류
            CL_NM = ft_df.loc[a,"CL_NM"]#관광지 이름
            CTPRVN_NM = ft_df.loc[a,"CTPRVN_NM"] #시도명
            SIGNGU_NM = ft_df.loc[a,"SIGNGU_NM"] #시군구명
            RDNMADR_NM = ft_df.loc[a,"RDNMADR_NM"] #도로명주소명
            popup = g.Popup(f'<b>{POI_NM}</b><br>종류 : {CL_NM}<br><br> 주소 : {CTPRVN_NM} {SIGNGU_NM} {RDNMADR_NM}',max_width=650)
            
            tooltip = POI_NM
            g.Marker([LAT, LONG], popup = popup, tooltip =tooltip).add_to(map)   

        # save map data to data object
        data = io.BytesIO()
        map.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)


class btn4Window(QWidget):
    global gungu
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Travel Manger - Hotels')
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        colums_to_keep = ['소재지전체주소',	'사업장명','위생업태명','위도','경도','시도','구']
        df = pd.read_csv('hotel.csv', encoding='utf-8', usecols = colums_to_keep)

        CTRVN_NM = sido #시도명
        SIGNGU_NM = gungu #시군구명

        ft_df = df[(df['시도'] == CTRVN_NM) & (df['구'] == SIGNGU_NM)]

        first_row = ft_df.iloc[0]
        map = g.Map(
            location = [first_row['위도'],first_row['경도']],
            zoom_start =13,
            attr ='VworldBase'
        )

        for a in ft_df.index:
            LAT  = ft_df.loc[a,"위도"]
            LONG = ft_df.loc[a,"경도"]
            HT_NM = ft_df.loc[a,"사업장명"]
            HT_TYPE = ft_df.loc[a,"위생업태명"] #숙박업 종류
            ADDRESS = ft_df.loc[a,"소재지전체주소"] #도로명주소명
            popup = g.Popup(f'<b>{HT_NM}</b><br>종류 : {HT_TYPE}<br>주소 :{ADDRESS}',max_width=700)
            
            tooltip = HT_NM
            g.Marker([LAT, LONG], popup = popup, tooltip =tooltip).add_to(map)   

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
