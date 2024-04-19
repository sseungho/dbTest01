import pymysql

dbConn = pymysql.connect(user='root', password='12345', host='localhost', db='shop_db')

while True:

    print('---------------- 회원 관리 프로그램 -------------------')
    print('1 : 회원 가입')
    print('2 : 회원 비번 수정')
    print('3 : 회원 탈퇴')
    print('4 : 전체 회원 목록 조회')
    print('5 : 프로그램 종료')

    print('----------------------------------------------------')
    menuNum = input('메뉴 중 한가지를 선택하세요 (1,2,3,4,5) : ')

    if menuNum == '1':
        print('회원 정보를 입력하세요 (ID, 이름, 사는 곳')
        memberID = input('회원 ID 입력하세요 : ')
        memberName = input('회원 이름을 입력하세요 : ')
        address = input('회원 주소를 입력하세요 : ')

        sql = f"INSERT INTO membertbl VALUES ('{memberID}', '{memberName}', '{address}')"  # DB에 실행할 SQL 문 생성
        cur = dbConn.cursor()
        result = cur.execute(sql)  # 연결된 DB의 스키마에 지정된 SQL 문이 실행
        if result == 1:
            print('회원 가입 성공')
        else:
            print('회원 가입 실패')
        cur.close()
        dbConn.commit()  # insert, delete, update 문을 사용하는 경우는 반드시 commit 할 것!

    elif menuNum == '2':
        memberID = input('회원 정보를 수정할 ID를 입력하세요 : ')
        memberName = input('수정할 회원 이름을 입력하세요 : ')
        address = input('수정할 회원 주소를 입력하세요 : ')

        sql = f"UPDATE membertbl SET memberName = '{memberName}', memberAddress = '{address}'  WHERE memberID = '{memberID}'"

        cur = dbConn.cursor()
        result = cur.execute(sql)  # 연결된 DB의 스키마에 지정된 SQL 문이 실행
        if result == 1:
            print('~~~~~~~~~~회원 정보 수정 성공')
        else:
            print('회원 정보 수정 실패~~~~~~~~~~')
        cur.close()
        dbConn.commit()  # insert, delete, update 문을 사용하는 경우는 반드시 commit 할 것!

    elif menuNum == "3":
        memberID = input('회원 탈퇴할 ID를 입력하세요 : ')

        sql = f"DELETE FROM membertbl WHERE memberID='{memberID}'"

        cur = dbConn.cursor()
        result = cur.execute(sql)  # 연결된 DB의 스키마에 지정된 SQL 문이 실행
        if result == 1:
            print('~~~~~~~~~~회원 탈퇴 완료')
        else:
            print('회원 탈퇴 실패~~~~~~~~~~')
        cur.close()
        dbConn.commit()  # insert, delete, update 문을 사용하는 경우는 반드시 commit 할 것!


    elif menuNum == '5':
        print('프로그램 종료 한다, say goodbye!')
        dbConn.close()
        break
    else:
        print('회원 정보를 다시 입력하세요!')

# DB 사용이 종료된 후에는 반드시 닫아 줄것! (close: cur 먼저 닫고 dbConn을 닫아야 함)



