from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSignal
import os
import pandas as pd
import folium as g
import io

class Touristmap(QWidget):
    closed = pyqtSignal()

    def __init__(self, sido, gungu):
        super().__init__()
        layout = QVBoxLayout()

        self.setWindowTitle('Travel Manger - Map')
        self.window_width, self.window_height = (1280, 720)
        self.setMinimumSize(self.window_width, self.window_height)
        self.setLayout(layout)

        self.sido = sido
        self.gungu = gungu

        colums_to_keep = ['POI_NM', 'CL_NM', 'CTPRVN_NM', 'SIGNGU_NM', 'LC_LO', 'LC_LA', 'RDNMADR_NM']
        df = pd.read_csv(f'{os.getcwd()}/DB/tour_spot.csv', encoding='utf-8', usecols=colums_to_keep)

        CTRVN_NM = sido  # 시도명
        SIGNGU_NM = gungu  # 시군구명

        ft_df = df[(df['CTPRVN_NM'] == CTRVN_NM) & (df['SIGNGU_NM'] == SIGNGU_NM)]

        first_row = ft_df.iloc[0]
        map = g.Map(
            location=[first_row['LC_LA'], first_row['LC_LO']],
            zoom_start=13,
            attr='VworldBase'
        )

        for a in ft_df.index:
            LAT = ft_df.loc[a, "LC_LA"]  # 위도
            LONG = ft_df.loc[a, "LC_LO"]  # 경도
            POI_NM = ft_df.loc[a, "POI_NM"]  # 관광지 종류
            CL_NM = ft_df.loc[a, "CL_NM"]  # 관광지 이름
            CTPRVN_NM = ft_df.loc[a, "CTPRVN_NM"]  # 시도명
            SIGNGU_NM = ft_df.loc[a, "SIGNGU_NM"]  # 시군구명
            RDNMADR_NM = ft_df.loc[a, "RDNMADR_NM"]  # 도로명주소명
            popup = g.Popup(f'<b>{POI_NM}</b><br>종류 : {CL_NM}<br><br> 주소 : {CTPRVN_NM} {SIGNGU_NM} {RDNMADR_NM}',
                            max_width=650)

            tooltip = POI_NM
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
