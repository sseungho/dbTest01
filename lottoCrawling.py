import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

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

    return