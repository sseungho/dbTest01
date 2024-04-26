import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from naverSearchApi import *

import webbrowser

form_class = uic.loadUiType("ui/naver_api_search.ui")[0] # 외부에서 ui 불러오기 (내부에서 불러올 경우 "[1]")

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("네이버 뉴스 제공")
        self.setWindowIcon(QIcon("img/news.png"))
        self.statusBar().showMessage("NAVER News Search App v1.0")

        self.searchBtn.clicked.connect(self.searchBtn_clicked)
        self.result_table.doubleClicked.connect(self.link_doubleClicked)
        # 테이블의 항목이 더블 클릭되면 함수 호출

    def searchBtn_clicked(self):
        keyword = self.input_keyword.text() # 사용자가 입력한 키워드 가져오기

        if keyword == "":
            QMessageBox.warning(self, "입력오류", "검색어를 넣어라!")
        else:
            naverApi = NaverApi()   #  import된 naverSearchApi 내의 NaverApi 클래스로 객체 선언
            searchResult = naverApi.getNaverSearch("news", keyword, 1, 50)
            # print(searchResult)
            newsResult = searchResult['items']
            self.outputTable(newsResult)
    def outputTable(self, newsResult):      # 뉴스 검색 결과 테이블 위젯에 출력 함수
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.result_table.setColumnCount(3) # 출력되는 table 을 3열로 설정
        self.result_table.setRowCount(len(newsResult)) # 출력되는 table 을 행의 개수 설정
        # newsResult 내의 원소 개수 만큼 row 개수를 설정

        # table의 첫 행(열 이름) 설정
        self.result_table.setHorizontalHeaderLabels(["기사제목","기사링크","게시시간"])
        self.result_table.setColumnWidth(0, 300)
        self.result_table.setColumnWidth(1, 200)
        self.result_table.setColumnWidth(2, 121)

        # 테이블 출력 결과 수정 금지
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # print(newsResult)

        for i, news in enumerate(newsResult):   # i -> 0~9 까지 index 뽑아옮
            newsTitle = news['title']   # 뉴스 제목
            newsTitle = newsTitle.replace("&quot","").replace(";","").replace("</b>","").replace("<b>","")
            newsLink = news['originallink']   # 뉴스 오리지널 소스
            newsDate = news['pubDate']   # 뉴스 게시일
            newsDate = newsDate[:25]

            self.result_table.setItem(i, 0, QTableWidgetItem(newsTitle))
            self.result_table.setItem(i, 1, QTableWidgetItem(newsLink))
            self.result_table.setItem(i, 2, QTableWidgetItem(newsDate))

    def link_doubleClicked(self):    # link 더블클릭 호출 됨
        selectedRow = self.result_table.currentRow()  # 현재 더블클릭하여 선택되어 있는 행의 index 반환
        selectedLink = self.result_table.item(selectedRow, 1).text()  # 현재 더블클릭한 셀의 text 반환
        webbrowser.open(selectedLink)

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())




