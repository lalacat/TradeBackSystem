# -*- coding: utf-8 -*-


from zsxq.database.base import ts_pro, sql_engine, ts
from zsxq.database.download_dailydata import Data
import pandas as pd
starttime = '20201130'
endtime = ''
data = Data(starttime, endtime)



engine = sql_engine()
pro = ts_pro()
ts= ts()
# stockcode = '000001.SZ'
stockcode = '000001.SZ'

# df0 = pro.daily(ts_code=stockcode, start_date=starttime,)
# df1 = pro.adj_factor(ts_code=stockcode, start_date=starttime)  # 复权因子
# df = pd.merge(df0, df1)  # 合并数据
# print(df)

df2 = ts.pro_bar(ts_code=stockcode, adj='qfq', start_date=starttime,adjfactor=True)
# print(df2)
df4 = pro.daily_basic(ts_code=stockcode, start_date=starttime)
df = pd.merge(df2,df4)
print(df)



# col2 = df2.columns.values.tolist()
# col4 = df4.columns.values.tolist()
# col = list(set(col4).difference(set(col2)))
# print(col)

# sql ="SELECT sql FROM sqlite_master WHERE type = 'table' AND tbl_name = '000001'"
# for c in col:
#     add_col_sql = f'ALTER TABLE "{stockcode[:-3]}" ADD COLUMN {c} real'
#     # print(add_col_sql)
#     engine.execute(add_col_sql)
    # df.ex(stockcode[:-3], engine, index=False, if_exists='append')
# print(data)

# data = pd.read_sql(sql,engine).values[0][0]
# df.to_sql(stockcode[:-3], engine, index=False, if_exists='append')

# print(df)



# sql = "select * from sqlite_master where type='table' order by name"
sql = "PRAGMA  table_info('000002')"
data = pd.read_sql(sql,engine)['name'].values.tolist()
col = list(set(df.columns.values.tolist()).difference(set(data)))
print(col)