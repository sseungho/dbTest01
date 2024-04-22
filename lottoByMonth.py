import pymysql
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from collections import Counter


dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='lottodb')

sql = "SELECT * FROM lotto_tbl"
cur = dbConn.cursor()
cur.execute(sql)
dbResult = cur.fetchall()

lotto_df = pd.DataFrame(dbResult, columns=['회차', '추첨일', '당첨번호1'
                        , '당첨번호2', '당첨번호3', '당첨번호4', '당첨번호5', '당첨번호6', '보너스번호'])

lotto_df['추첨일'] = pd.to_datetime(lotto_df['추첨일'])   # 추첨일을 pandas 날짜 형식으로 변환

# 추첨일에서 월 month 만 추출하여 새로운 필드로 데이터 프레임 추가

lotto_df['추첨월'] = lotto_df['추첨일'].dt.month

# lotto_month_01 = lotto_df[lotto_df['추첨월']==1]   # 1월에 출현 했던 당첨 번호 데이터
#
# # print(lotto_month_01)
#
# month01_lottolist = list(lotto_month_01['당첨번호1'])+list(lotto_month_01['당첨번호2'])+list(lotto_month_01['당첨번호3'])+list(lotto_month_01['당첨번호4'])+list(lotto_month_01['당첨번호5'])+list(lotto_month_01['당첨번호6'])+list(lotto_month_01['보너스번호'])
# print(Counter(month01_lottolist))
#
# data = pd.Series(Counter(month01_lottolist))
# data.plot(figsize=(20,35), kind='barh', grid=True, title='1월 로또 번호 빈도수')

for month in range(1, 13):
    lotto_month_df = lotto_df[lotto_df['추첨월']==month]   # month 월에 출현 했던 당첨 번호 데이터
    month_lottolist = list(lotto_month_df['당첨번호1'])+list(lotto_month_df['당첨번호2'])+list(lotto_month_df['당첨번호3'])+list(lotto_month_df['당첨번호4'])+list(lotto_month_df['당첨번호5'])+list(lotto_month_df['당첨번호6'])+list(lotto_month_df['보너스번호'])

    month_freq = Counter(month_lottolist)   # 월별 출현 숫자 빈도수

    data = pd.Series(month_freq)
    sored_data = data.sort_values(ascending=False)  # 빈도수 순으로 내림차순
    top10_data = sored_data.head(10) # 빈도수 상위 10 개만 추출

    plt.subplot(4,3, month)
    plt.subplots_adjust(left=0.125, bottom = 0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.5)
    top10_data.plot(figsize=(12,20), kind='barh', grid=True, title=f'{month}월별 최다 출현 로또 번호')
    plt.xlabel('빈도수')
    plt.ylabel('로또 번호')

plt.show()
cur.close()
dbConn.close()