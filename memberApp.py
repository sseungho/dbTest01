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
        self.memberreset_btn.clicked.connect(self.memberinfo_reset)
        self.idcheck_btn.clicked.connect(self.idcheck)
        self.membersearch_btn.clicked.connect(self.member_search)   # 회원 조회 버튼 클릭 시 회원 정보 출력 함수 실행
        self.membermodify_btn.clicked.connect(self.member_modify)   # 회원 정보 수정 함수 호출
        self.login_btn.clicked.connect(self.memberLogin)
        self.loginreset_btn.clicked.connect(self.logininfo_reset)
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

    def idcheck(self):  # 기존 회원 가입 여부 체크 함수
        memberid = self.joinid_edit.text()  # 유저가 입력한 회원 아이디 텍스트 가져오기

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
            cur.close()
            dbConn.close()

            if result[0][0] == 1:
                QMessageBox.warning(self, '회원 가입 불가 ', '이미 가입된 ID! \n다시 입력 하세요.')
                return 0
            else:
                QMessageBox.warning(self, '회원 가입 성공 ', '계속해서 진행 하세요.')
                return 1
    def membercheck(self): # 기존 회원 가입 여부 체크 함수
        memberid = self.memberid_edit.text() # 유저가 입력한 회원 아이디 텍스트 가져오기

        dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shop_db")
        sql = f"SELECT count(*) FROM appmember WHERE memberID = '{memberid}'"
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        cur.close()
        dbConn.close()

        if result[0][0] == 1:
            return 1
        else:
            QMessageBox.warning(self, '회원 조회 불가', 'ID 검색 안됨 다시 입력 하세요.')
            self.memberinfo_reset()
            return 0
    def member_search(self):    # 아이디로 회원 정보 조회
        memberid = self.memberid_edit.text() # 유저가 입력한 회원 아이디 텍스트 가져오기
        dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shop_db")
        sql = f"SELECT * FROM appmember WHERE memberID = '{memberid}'"
        if memberid == "":
            QMessageBox.warning(self, 'ID 입력 오류', 'ID는 필수 입력 사항입니다!')
        elif self.membercheck() == 0:
            pass
        else:
            cur = dbConn.cursor()
            cur.execute(sql)
            result = cur.fetchall()

            cur.close()
            dbConn.close()
            print(result)

            self.memberpw_edit.setText(result[0][1])
            self.membername_edit.setText(result[0][2])
            self.memberemail_edit.setText(result[0][3])
            self.memberage_edit.setText(str(result[0][4]))
    def memberinfo_reset(self):  # 회원 가입 정보 입력 화면 초기화
        self.memberid_edit.clear()
        self.memberpw_edit.clear()
        self.memberemail_edit.clear()
        self.membername_edit.clear()
        self.memberage_edit.clear()


    def member_modify(self):  # 회원 가입 정보 입력 화면 초기화
        memberid = self.memberid_edit.text()
        memberpw = self.memberpw_edit.text()
        memberemail = self.memberemail_edit.text()
        membername = self.membername_edit.text()
        memberage = self.memberage_edit.text()

        dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shop_db")

        sql = f"UPDATE appmember SET memberpw = '{memberpw}', membername = '{membername}', memberemail = '{memberemail}', memberage = '{memberage}' WHERE memberid = '{memberid}'"
        cur = dbConn.cursor()
        result = cur.execute(sql)

        if result == 1:     # 회원 정보 수정 성공
            QMessageBox.warning(self, '회원정보수정 성공', '회원 정보 수정 완료!')
        else:
            QMessageBox.warning(self, '실패', '회원정보 수정 실패!')

        cur.close()
        dbConn.commit()
        dbConn.close()

    def memberLogin(self):
        loginid = self.loginid_edit.text()    # 유저가 로그인 창에 입력한 아이디 가져오기
        loginpw = self.loginpw_edit.text()    # 패스워드 가져오기

        if loginid == "" or loginpw == "":  # 아이디, 비번 공란 확인
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비번 입력하세요.")
        else:
            dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shop_db")
            sql = f"SELECT count(*) FROM appmember WHERE memberid='{loginid}' AND memberpw='{loginpw}'"

            # 아이디와 비밀번호가 모두 일치하는 레코드 개수를 반환(1 또는 0 반환 tuple)

            cur = dbConn.cursor()
            cur.execute(sql)

            result = cur.fetchall()  # 1이면 로그인 성공, 아니면 실패
            print(result)

            if result[0][0] == 1:   # 로그인 성공
                QMessageBox.warning(self, "로그인 성공", f"{loginid}님 로그인 성공.")

            else:
                QMessageBox.warning(self, "로그인 실패", "아이디 또는 비번 입력하세요.")


    def logininfo_reset(self):  # 로그인 입력 화면 초기화
        self.loginid_edit.clear()
        self.loginpw_edit.clear()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())


