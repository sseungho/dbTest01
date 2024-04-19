import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/member.ui")[0] # UI 불러오기

class MainWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("회원 관리 프로그램")

        self.join_btn.clicked.connect(self.member_join)
        self.joinreset_btn.clicked.connect(self.join_reset)
        self.idcheck_btn.clicked.connect(self.idcheck)

    def member_join(self):     # 회원가입 이벤트 처리 함수
        memberid = self.joinid_edit.text() # 유저가 입력한 회원 아이디 텍스트 가져오기
        memberpw = self.joinpw_edit.text() # 유저가 입력한 회원 비밀번호 텍스트 가져오기
        membername = self.joinname_edit.text() # 유저가 입력한 회원 이름 텍스트 가져오기
        memberemail = self.joinemail_edit.text() # 유저가 입력한 회원 이메일 텍스트 가져오기
        memberage = self.joinage_edit.text() # 유저가 입력한 회원 나이 텍스트 가져오기

        if memberid == "" or memberpw == "" or membername == "" or memberemail == "" or memberage == "":
            QMessageBox.warning(self, '입력 오류', '입력되지 않은 항목이 있습니다.\n다시 입력 하세요.')
        elif len(memberid) < 4 or len(memberid) > 15:
            QMessageBox.warning(self, 'ID 길이 오류', 'ID는 4자 이상 14자 이하! \n다시 입력 하세요.')
        elif len(memberpw) < 4 or len(memberpw) > 15:
            QMessageBox.warning(self, '비번 길이 오류', '비번은 4자 이상 14자 이하! \n다시 입력 하세요.')
        elif self.idcheck() == 0: # 가입 불가
            self.joinid_edit.clear()
            pass
        else:
            dbConn = pymysql.connect(user="root", password="12345", host="localhost",  db="shop_db")

            sql = f"INSERT INTO appmember VALUES ('{memberid}','{memberpw}','{membername}','{memberemail}','{memberage}')"

            cur = dbConn.cursor()
            result = cur.execute(sql)  # 회원가입하는 sql 명령이 성공하면 1이 반환
            if result == 1:
                QMessageBox.warning(self, '회원가입성공', '축하합니다. \n회원가입이 성공하였습니다.')
                self.join_reset()   # 회원 가입 성공 후에 입력화면 초기화
            else:
                QMessageBox.warning(self, '회원가입 실패', '회원가입이 실패 하였습니다.')

            cur.close()
            dbConn.commit()
            dbConn.close()
    def join_reset(self):  # 회원 가입 정보 입력 화면 초기화
        self.joinid_edit.clear()
        self.joinpw_edit.clear()
        self.joinemail_edit.clear()
        self.joinname_edit.clear()
        self.joinage_edit.clear()

    def idcheck(self): # 기존 회원 가입 여부 체크 함수
        memberid = self.joinid_edit.text() # 유저가 입력한 회원 아이디 텍스트 가져오기

        if memberid == "":
            QMessageBox.warning(self, 'ID 입력 오류', 'ID는 필수 입력 사항입니다!')
        elif len(memberid) < 4 or len(memberid) > 15:
            QMessageBox.warning(self, 'ID 길이 오류', 'ID는 4자 이상 14자 이하! \n다시 입력 하세요.')
        else:
            dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shop_db")
            sql = f"SELECT count(*) FROM appmember WHERE memberID = '{memberid}'"
            cur = dbConn.cursor()
            cur.execute(sql)
            result = cur.fetchall()

            if result[0][0] == 1:
                QMessageBox.warning(self, '회원 가입 불가 ', '이미 가입된 ID! \n다시 입력 하세요.')
                return 0
            else:
                QMessageBox.warning(self, '회원 가입 성공 ', '계속해서 진행 하세요.')
                return 1
app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


