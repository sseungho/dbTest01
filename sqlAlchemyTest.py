from sqlalchemy import create_engine
import pandas as pd
import pymysql

data = {'학번': range(2000,2015),'성적':[55,66,77,22,33,55,34,88,99,100,1,2,3,4,5]}

df= pd.DataFrame(data = data, columns=['학번','성적'])

print(df)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
engine.connect()

df.to_sql(name="test_tbl", con=engine, if_exists='append', index=False)

