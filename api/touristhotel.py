from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSignal
import os
import pandas as pd
import folium as g
import io

class Touristhotel(QWidget):
    global gungu
    closed = pyqtSignal()

    def __init__(self, sido, gungu):
        super().__init__()
        layout = QVBoxLayout()

        self.setWindowTitle('Travel Manager - Hotels')
        self.window_width, self.window_height = (1280, 720)
        self.setMinimumSize(self.window_width, self.window_height)
        self.setLayout(layout)

        self.sido = sido
        self.gungu = gungu

        colums_to_keep = ['소재지전체주소', '사업장명', '위생업태명', '위도', '경도', '시도', '구']
        df = pd.read_csv(f'{os.getcwd()}/DB/tour_hotel.csv', encoding='utf-8', usecols=colums_to_keep)

        CTRVN_NM = sido  # 시도명
        SIGNGU_NM = gungu  # 시군구명

        ft_df = df[(df['시도'] == CTRVN_NM) & (df['구'] == SIGNGU_NM)]

        first_row = ft_df.iloc[0]
        map = g.Map(
            location=[first_row['위도'], first_row['경도']],
            zoom_start=13,
            attr='VworldBase'
        )

        for a in ft_df.index:
            LAT = ft_df.loc[a, "위도"]
            LONG = ft_df.loc[a, "경도"]
            HT_NM = ft_df.loc[a, "사업장명"]
            HT_TYPE = ft_df.loc[a, "위생업태명"]  # 숙박업 종류
            ADDRESS = ft_df.loc[a, "소재지전체주소"]  # 도로명주소명
            popup = g.Popup(f'<b>{HT_NM}</b><br>종류 : {HT_TYPE}<br>주소 :{ADDRESS}', max_width=700)

            tooltip = HT_NM
            g.Marker([LAT, LONG], popup=popup, tooltip=tooltip).add_to(map)

            # save map data to data object
        data = io.BytesIO()
        map.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
