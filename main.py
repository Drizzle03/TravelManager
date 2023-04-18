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
UIbtn3_class = uic.loadUiType("foodui.ui")[0]

#시도군구 default 값
sido = '서울특별시'
gungu = '서대문구'

# Main Window
class MyWindow(QMainWindow, QWidget, UI_class) :
    def __init__(self) :
        super().__init__()
        self.setWindowTitle('Travel Manager - Main')
        self.setupUi(self)

        self.btn1.clicked.connect(self.button1Function) #관광지맵
        self.btnget.clicked.connect(self.getinfoFunction)
        self.btn3.clicked.connect(self.button3Function)
        self.btn4.clicked.connect(self.button4Function) #숙소 후보

    def button1Function(self):
        self.hide()
        self.myApp = btn1Window()
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    def getinfoFunction(self):
        global sido, gungu
        sido = self.sido_info.text()
        gungu = self.gungu_info.text()

    def button3Function(self):
        self.hide()
        self.myApp = btn3Window()
        self.myApp.show()
        self.myApp.closed.connect(self.show)

    def button4Function(self):
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

class btn3Window(QWidget, UIbtn3_class):
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Travel Manager - Food')
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        sido_input = sido
        #윤서 코드 삽입
        food_list = {}
        food_list['서울특별시'] = '남산 돈까스, 마포 돼지갈비, 신당동 떡볶이, 신림동 순대, 장충동 족발, 종로 닭한마리, 종로 생선구이, 종로 육회, 왕십리 양념 돼지 곱창'
        food_list['인천광역시'] = '강화 사자발약쑥전, 강화 인삼 삼계탕, 대청도 참홍어, 무의도 낙지해물칼국수, 신포동 닭강정, 중구 개항장 짜장면'
        food_list['강원도'] = '양양 송이버섯전골, 양양 메밀홍합장칼국수, 고성 생태맑은탕, 양구 시래기요리, 인제 황태찜,  정선 콧등치기국수, 화천 산천어영양돌솥밥, 철원 돼지갈비'
        food_list['충청도'] = '강경 젓갈정식, 괴산 메기매운탕, 단양 쏘가리매운탕, 보은 약초산채정식, 서산 어리굴젓, 영동 어죽, 진천 도리뱅뱅이, 태안 게국지'
        food_list['경상도'] = '마산 아귀찜, 부산 돼지국밥, 통영 충무김밥, 포항 과메기, 포항 물회, 청도 미나리삼겹살, 청도 추어탕, 청송 닭불고기, 안동 간고등어정식, 안동 찜닭, 달성 현풍곰탕, 대구 찜갈비, 동래 해물파전'
        food_list['전라도'] = '전주비빔밥, 나주곰탕, 풍천장어, 영광굴비정식, 담양대통밥, 광양불고기, 흑산도 홍어, 목포 세발낙지, 벌교꼬막, 여수 갓김치, 순천짱뚱어탕'
        food_list['제주도'] = '흑돼지구이, 오분자기, 서귀포 옥돔구이, 자리돔물회, 갈치국'

        if sido_input == '충청남도' or sido_input == '충청북도':
            sido_input = '충청도'
        if sido_input == '경상남도' or sido_input == '경상북도':
            sido_input = '경상도'
        if sido_input == '전라남도' or sido_input == '전라북도':
            sido_input = '전라도'
        if not sido_input in ['서울특별시','인천광역시','강원도','충청도','경상도','전라도','제주도']:
            result = 'DB에 등록되지 않은 지역이에요! \n 대신에 여기서 찾아보는 건 어떨까요? \nhttps://www.siksinhot.com/search?keywords=%ED%8C%94%EB%8F%84%EC%8B%9C%EC%9E%A5'
            self.print.setText(result)
        else:
            result = food_list[sido_input]
            self.print.setText(result)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

class btn4Window(QWidget):
    global gungu
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Travel Manager - Hotels')
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
