import pymysql  # mysql 과 연동 시켜주는 라이브러리

# 파이썬 과 mysql 서버 사이에 connection 생성
# 1) 계정: root(관리자)
# 2) 비밀번호: 12345
# 3) 데이터베이스가 설치된 컴퓨터의 IP 주소
#   - 본인 컴퓨터라면 localhost, 다른 컴퓨터라면 그 컴퓨터의 IP 주소
#   - 192.168.0.100 (교수용 컴퓨터 IP)
#   데이터베이스 schema 이름(ex. shopdb)

dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='shop_db')
# 파이썬과 mysql 간 connection 생성

sql = "SELECT * FROM membertbl" # DB에 실행할 SQL 문 생성

cur = dbConn.cursor()

cur.execute(sql) #연결된 DB의 스키마에 지정된 SQL 문이 실행

records = cur.fetchall()    # sql 문에서 실행된 SELECT 문의 결과를 records에 받음 (tuple 로 반환)

print(records)
print(records[0])   # 특정 레코드(1행)
print(records[0][1])    # 특정 레코드의 특정 값 ('한주연')

for member in records:
    print(member[1])

# DB 사용이 종료된 후에는 반드시 닫아 줄것! (close: cur 먼저 닫고 dbConn을 닫아야 함)
cur.close()
dbConn.close()


