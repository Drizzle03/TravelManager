import pandas as pd
import sys
import io
import folium as g
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)
        colums_to_keep = ['POI_NM','CL_NM','CTPRVN_NM','SIGNGU_NM','LC_LO','LC_LA','RDNMADR_NM', ]
        df = pd.read_csv('data.csv', encoding='utf-8', usecols = colums_to_keep)

        CTRVN_NM = '서울특별시' #시도명
        SIGNGU_NM = '서대문구' #시군구명

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')