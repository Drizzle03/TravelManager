# TravelManager(2023/04/15 ~ 2023/04/18)
Python 컴퓨팅적 사고 교양 팀플 1 / 여행지 관리 프로그램 기능 추가하기

<h3>I. 목표 기능</h1>
  1. 관광 예정 지역 관광명소 추천 및 지도 시각화, 관광지 정보 제공
  <br>2. 관광지 포토스팟 추천
  <br>3. 관광 예정 지역 대표 음식 추천
  <br>4. 여행 예정 관광지 및 숙소 후보들 입력시 지도 시각화
  
 <br><h3>II. 구현 방법</h3>
  <b>1.관광지 추천 및 정보 제공</b>
    <br>- Pandas 기반 관광명소 CSV 파일 가공 후 방문 예정 지역 관광지 정보 DataFrame 추출
    <br>- Folium 라이브러리 기반 지도 시각화 및 마커 정보 제공
    <br>- PyQt5 이용 GUI 제작 및 Folium 생성 html 파일 출력
  
  <b>2. 관광지 포토스팟</b>
    <br>- Selenium, beautifulsoup 이용 인스타그램 크롤링
    <br>- 관광지명을 담은 해시태그 검색 -> 게시물의 위치 태그 출력<br>
  
  <b>3. 관광 지역 대표 음식 추천</b>
    <br>- 관광지역 대표 음식 리스트 정리 후 출력 </b>
  
  <b>4. 여행 예정 관광지 및 숙소 후보 시각화 -> 숙소 위치 지정 시 도움을 주기 위함</b>
    <br>- 1번과 동일
    <br>- 시도 군구 주소 정보를 입력 받은 뒤, 위도, 경도 정보로 변환
    <br>- Folium 라이브러리에 전달 후 시각화<br>

  <br><h3>III. 시연영상</h3>
  <a href="https://youtu.be/rP_ANphXJEo" target="_blank">https://youtu.be/rP_ANphXJEo </a>
