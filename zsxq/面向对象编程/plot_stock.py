# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:01:39 2019

@author: zjy
"""
# from RPS import get_code
import pandas as pd  
import numpy as np
# from pyecharts import Kline,Line, Bar,Overlap
from django.contrib.postgres.lookups import Overlap
from pyecharts.charts import Line, Bar, Kline

from zsxq.Python价量形态选股代码.RPS import get_code
from zsxq.base_bak import sql_engine

engine = sql_engine()
codes,names=get_code()
stocks=dict(zip(names,codes))

class stock_plot(object):
    def __init__(self,name,n=250):
        self.name=name
        self.n=n
        
    def get_stock_data(self):
        code=stocks[self.name]
        sql=f"select * from daily_data where ts_code='{code}'"
        df=pd.read_sql(sql,engine)
        df.index=pd.to_datetime(df.trade_date)
        df=(df.sort_index()).drop('trade_date',axis=1)
        return df[-self.n:] 
   
    def cal_hadata(self):
        df=self.get_stock_data()
        df['adjclose']=(df.close*df.adj_factor)/df.adj_factor[-1]
        df['adjopen']=(df.open*df.adj_factor)/df.adj_factor[-1]
        df['adjhigh']=(df.high*df.adj_factor)/df.adj_factor[-1]
        df['adjlow']=(df.low*df.adj_factor)/df.adj_factor[-1]
        #计算修正版K线
        df['ha_close']=(df.adjclose+df.adjopen+df.adjhigh+df.adjlow)/4.0
        ha_open=np.zeros(df.shape[0])
        ha_open[0]=df.adjopen[0]
        for i in range(1,df.shape[0]):
            ha_open[i]=(ha_open[i-1]+df['ha_close'][i-1])/2
        df.insert(1,'ha_open',ha_open)
        df['ha_high']=df[['adjhigh','ha_open','ha_close']].max(axis=1)
        df['ha_low']=df[['adjlow','ha_open','ha_close']].min(axis=1)
        df=df.iloc[1:]
        return df
    
    def kline_plot(self,ktype=0):
        df=self.cal_hadata()
        #画K线图数据
        date = df.index.strftime('%Y%m%d').tolist()
        if ktype==0:
            k_value = df[['adjopen','adjclose', 'adjlow','adjhigh']].values
        else:
            k_value = df[['ha_open','ha_close', 'ha_low', 'ha_high']].values
        #引入pyecharts画图使用的是0.5.11版本，新版命令需要重写
        
        kline = Kline(self.name+'行情走势')
        kline.add('日K线图', date, k_value,
              is_datazoom_show=True,is_splitline_show=False)
        #加入5、20日均线
        df['ma20']=df.adjclose.rolling(20).mean()
        df['ma5']=df.adjclose.rolling(5).mean()
        line = Line()
        v0=df['ma5'].round(2).tolist()
        v=df['ma20'].round(2).tolist()
        line.add('5日均线', date,v0,
             is_symbol_show=False,line_width=2)
        line.add('20日均线', date,v, 
             is_symbol_show=False,line_width=2)
        #成交量
        bar = Bar()
        bar.add('成交量', date, df['vol'],tooltip_tragger='axis', 
                is_legend_show=False, is_yaxis_show=False, 
                yaxis_max=5*max(df['vol']))
        overlap = Overlap()
        overlap.add(kline)
        overlap.add(line,)
        overlap.add(bar,yaxis_index=1, is_add_yaxis=True)
        return overlap    