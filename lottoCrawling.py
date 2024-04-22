from sqlalchemy import create_engine
from functools import cache
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

@cache
def get_lottoNumber(count): # lotto 추첨 회차를 인수로 받음
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={count}"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find('p', {'class': 'desc'}).text  # 로또 추첨일 정보
    lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")
    # 로또 당첨 번호 6개 반환
    lottoNumber = soup.find('div', {'class': 'num win'}).find('p').text.strip().split('\n')
    # str 을 int 변환
    lottoNumberList = []
    for num in lottoNumber:
        lottoNumberList.append(int(num))
    # 로또 당첨 보너스 번호 1개 반환 >> str 을 int 변환
    bonusNumber = int(soup.find('div', {'class': 'num bonus'}).find('p').text.strip())

    lottoDic = {'lottoDate': lottoDate, 'lottoNumber': lottoNumberList, 'bonusNumber': bonusNumber}

    return lottoDic

def get_recent_lottocount(): # 최신 로또 회차 크롤링 함수
    url = "https://www.dhlottery.co.kr/common.do?method=main"   # 동핵 복권 메인 화면
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    recent_count = soup.find('strong', {"id": "lottoDrwNo"}).text.strip()
    recent_count = int(recent_count)
    return recent_count + 1

lottoDf_list = []

for count in range(1, get_recent_lottocount()):
    lottoResult = get_lottoNumber(count)

    lottoDf_list.append({
        'count': count,                              # lotto 추첨 회차
        'lottoDate': lottoResult['lottoDate'],       # lotto 추첨일
        'lottoNum1': lottoResult['lottoNumber'][0],  # 1번째 당첨 번호
        'lottoNum2': lottoResult['lottoNumber'][1],  # 2번째 당첨 번호
        'lottoNum3': lottoResult['lottoNumber'][2],  # 3번째 당첨 번호
        'lottoNum4': lottoResult['lottoNumber'][3],  # 4번째 당첨 번호
        'lottoNum5': lottoResult['lottoNumber'][4],  # 5번째 당첨 번호
        'lottoNum6': lottoResult['lottoNumber'][5],  # 6번째 당첨 번호
        'bonusNum': lottoResult['bonusNumber']       # bonus 번호
    })
    print(f"{count} 회차 처리중......")

lottoDf = pd.DataFrame(data = lottoDf_list, columns = ['count', 'lottoDate',
            'lottoNum1', 'lottoNum2','lottoNum3','lottoNum4','lottoNum5','lottoNum6','bonusNum'])

# print(lottoDf)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
engine.connect()

lottoDf.to_sql(name="lotto_tbl", con=engine, if_exists='append', index=False)