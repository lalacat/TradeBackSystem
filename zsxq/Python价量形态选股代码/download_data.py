# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:29:06 2019

@author: zhangjinyi
"""
#只需运行一次即可
import pandas as pd

from zsxq.base import sql_engine,ts_pro

pro=ts_pro()
engine = sql_engine()

class Data(object):
    def __init__(self,start,end,table_name='daily_data'):
        self.start=start
        self.end=end
        self.table_name=table_name
        self.codes=self.get_code()
        
    def get_code(self):
        codes = pro.stock_basic(list_status='L').ts_code.values
        return codes
    
    #每日行情数据
    def daily_data(self,code):
        try:
            #每日交易数据
            df0=pro.daily(ts_code=code,start_date=self.start,end_date=self.end)
            #复权因子
            df1=pro.adj_factor(ts_code=code, trade_date='')
            df=pd.merge(df0,df1)
        except Exception as e:
            print(code)
            print(e)
        return df
    
    def save_sql(self):
        for code in self.codes:
            data=self.daily_data(code)
            data.to_sql(self.table_name,engine,index=False,if_exists='append')
                
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
    data=Data('20050101','20201126',table_name='daily_data')
    data.save_sql() 
    data.info_sql()               