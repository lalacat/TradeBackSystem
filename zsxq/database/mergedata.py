
from zsxq.database.base import ts_pro, sql_engine, ts
from zsxq.database.download_dailydata import Data
import pandas as pd
starttime = '20201201'
endtime = ''

path1 = 'X://股票//test//df2.csv'
path2 = 'X://股票//test//df4.csv'
path3 = 'X://股票//test//df.csv'

engine = sql_engine()
pro = ts_pro()
ts= ts()
# stockcode = '000001.SZ'
stockcode = '000001.SZ'
df2 = ts.pro_bar(ts_code=stockcode, adj='qfq', start_date=starttime,adjfactor=True)
print(df2)
df4 = pro.daily_basic(ts_code='000002.SZ', start_date=starttime)
del df4['close']
print(df4)
# df = pd.merge(df2,df4)
df = pd.concat([df2,df4],axis=0)
# df2.to_csv(path1)
# df4.to_csv(path2)
# df.to_csv(path3)
# del df[len(df2.columns):len(df2.columns)+3]


print(df)
