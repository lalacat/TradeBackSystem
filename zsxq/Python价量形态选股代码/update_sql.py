# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:56:13 2019

@author: zhangjinyi
"""

import pandas as pd
import numpy as np
#import sqlite3 as sq3
from .base import sql_engine,ts_pro
from dateutil.parser import parse
from datetime import datetime,timedelta

pro=ts_pro()
engine = sql_engine()

#获取交易日历
cals=pro.trade_cal(exchange='SSE')
cals=cals[cals.is_open==1].cal_date.values
#获取最新交易日期
def get_trade_date():
    #获取当天日期时间
    d0=datetime.now()
    if d0.hour>15:
        d=d0.strftime('%Y%m%d')
    else:
        d=(d0-timedelta(1)).strftime('%Y%m%d')
    while d not in cals:
        d1=parse(d)
        d=(d1-timedelta(1)).strftime('%Y%m%d')
    return d

#每日行情数据：table_name='daily_data'

def update_sql(table_name='daily_data'):
    d0=pd.read_sql(f"select max(trade_date) from {table_name}",engine)
    d0=d0.values[0][0]
    d1=get_trade_date()
    n0=np.argwhere(cals==d0)[0][0]+1
    n1=np.argwhere(cals==d1)[0][0]+1
    dates=cals[n0:n1]
    if len(dates)>0:
        for d in dates:
            df0=pro.daily(trade_date=d)
            df1=pro.adj_factor(trade_date=d)
            df=pd.merge(df0,df1)
            df.to_sql(table_name,engine,index=False,if_exists='append')
        print(f"数据库已更新至{dates[-1]}日数据")
    else:
        print("数据已经是最新的！")
        
def info_sql(table_name='daily_data'):
    sql1=f'select count(*) from {table_name}'
    l=pd.read_sql(sql1,engine).values[0][0]
    print(f'统计查询的总数：{l}')
    sql2=f'select min(trade_date) from {table_name}'
    sql3=f'select max(trade_date) from {table_name}'
    t0=pd.read_sql(sql2,engine).values[0][0]
    t1=pd.read_sql(sql3,engine).values[0][0]
    print(f'数据期间：{t0}——{t1}')
    sql4=f'select distinct ts_code from {table_name}'
    d=pd.read_sql(sql4,engine)
    print(f'数据库包含股票个数：{len(d)}')

if __name__ == "__main__":
    update_sql(table_name='daily_data')