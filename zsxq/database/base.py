# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:27:12 2019
#请把token换成你自己的，不然刷新后可能用不了
@author: zjy
"""
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# filename='sqlite:///X:\\股票\\db_stock\\'
# filename = 'C:\\Users\\scott\\Documents\\学习文档\\stock_db' + '\\'
# filename = 'W:\\stock_db'+ '\\'
filename = 'X:\\股票'+ '\\'
db_name='stock_data.db'

def sql_engine(file=filename,db=db_name):
    # path=file+db

    engine = sqlite3.connect(filename + db)
    return engine

def ts_pro():
    import tushare as ts 
    token='f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8'
    pro=ts.pro_api(token)
    return pro

def ts():
    import tushare as ts
    token = 'f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8'
    ts.set_token(token)
    return ts

def get_data(ts_code,start_date=None,end_date=None):
    sql=f"select distinct * from '{ts_code}'"
    data = pd.read_sql(sql,sql_engine(filename,db_name))
    if data is None:
        return data
    else:
        data.index = pd.to_datetime(data.trade_date)
        data = data.sort_index()
        if start_date is not None and end_date is None:
            data = data[start_date:]
        elif start_date == None and end_date is not None :
            data = data[:end_date]
        else:
            data = data[start_date:end_date]
        return data

def get_code_data(code, start, end):
    df =get_data(ts_code=code, start_date=start, end_date=end)
    df['openinterest']=0
    df=df[['open','high','low','close','amount','openinterest']]
    df.columns =['open','high','low','close','volume','openinterest']
    return df

