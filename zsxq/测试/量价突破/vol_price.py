import pandas as pd

from zsxq.database.base import ts_pro, sql_engine

pro= ts_pro()
engine = sql_engine()



df=pd.read_sql("select * from stock_data where ts_code='000001'",engine)
print(len(df))