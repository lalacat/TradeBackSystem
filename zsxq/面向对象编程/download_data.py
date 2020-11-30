# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:29:06 2019

@author: zhangjinyi
"""

import numpy as np
import pandas as pd
from dateutil.parser import parse
from datetime import datetime,timedelta

from zsxq.base import ts_pro, sql_engine

pro=ts_pro()
engine = sql_engine()

class Data(object):
    def __init__(self,start='20050101',end='20191115',table_name='daily_data'):
        self.start=start
        self.end=end
        self.table_name=table_name
        self.codes=self.get_code()
        self.cals=self.get_cals()
        
    #获取股票代码列表    
    def get_code(self):
        codes = pro.stock_basic(list_status='L').ts_code.values
        return codes
    
    #获取股票交易日历
    def get_cals(self):
        #获取交易日历
        cals=pro.trade_cal(exchange='')
        cals=cals[cals.is_open==1].cal_date.values
        return cals
    
    #每日行情数据
    def daily_data(self,code):
        try:
            df0=pro.daily(ts_code=code,start_date=self.start,end_date=self.end)            
            df1=pro.adj_factor(ts_code=code,trade_date='') #复权因子
            df=pd.merge(df0,df1)  #合并数据
		
        except Exception as e:
            print(code)
            print(e)
        return df
    
    #保存数据到数据库
    def save_sql(self):
        for code in self.codes:
            data=self.daily_data(code)
            data.to_sql(self.table_name,engine,index=False,if_exists='append')
            
    #获取最新交易日期
    def get_trade_date(self):
        #获取当天日期时间
        d0=datetime.now()
        if d0.hour>15:
            d=d0.strftime('%Y%m%d')
        else:
            d=(d0-timedelta(1)).strftime('%Y%m%d')
        while d not in self.cals:
            d1=parse(d)
            d=(d1-timedelta(1)).strftime('%Y%m%d')
        return d

    #更新数据库数据
    def update_sql(self):
        d0=pd.read_sql(f"select max(trade_date) from {self.table_name}",engine)
        d0=d0.values[0][0]
        d1=self.get_trade_date()
        n0=np.argwhere(self.cals==d0)[0][0]+1
        n1=np.argwhere(self.cals==d1)[0][0]+1
        dates=self.cals[n0:n1]
        if len(dates)>0:
            for d in dates:
                df0=pro.daily(trade_date=d)
                df1=pro.adj_factor(trade_date=d)
                df=pd.merge(df0,df1)
                df.to_sql(self.table_name,engine,index=False,if_exists='append')
            print(f"数据库已更新至{dates[-1]}日数据")
        else:
            print("数据已经是最新的！")
    
    #查询数据库信息            
    def info_sql(self):
        sql1=f'select count(*) from {self.table_name}'
        l=pd.read_sql(sql1,engine).values[0][0]
        print(f'统计查询的总数：{l}')
        sql2=f'select min(trade_date) from {self.table_name}'
        sql3=f'select max(trade_date) from {self.table_name}'
        t0=pd.read_sql(sql2,engine).values[0][0]
        t1=pd.read_sql(sql3,engine).values[0][0]
        print(f'数据期间：{t0}——{t1}')
        sql4=f'select distinct ts_code from {self.table_name}'
        d=pd.read_sql(sql4,engine)
        print(f'数据库包含股票个数：{len(d)}')

if __name__ == "__main__":
    data=Data()
    #data.save_sql() #只需运行一次即可
    #data.update_sql()      
    data.info_sql()         