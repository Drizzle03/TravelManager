from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

UIbtn3_class = uic.loadUiType("./UI/foodui.ui")[0]
class Touristfood(QWidget, UIbtn3_class):
    closed = pyqtSignal()
    def __init__(self, sido):
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