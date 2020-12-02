# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:06:28 2019

@author: zjy
"""

#先引入后面可能用到的包（package）
import pandas as pd  
import numpy as np
from pyecharts.basic_charts  import Kline,Line, Bar,Overlap
from zsxq.database.base import ts_pro
#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

pro=ts_pro()

#常用大盘指数
indexs={'上证综指': '000001.SH','深证成指': '399001.SZ','沪深300': '000300.SH',
       '创业板指': '399006.SZ','上证50': '000016.SH','中证500': '000905.SH',
       '中小板指': '399005.SZ','上证180': '000010.SH'}

class Index_data(object):
    def __init__(self,name,n=250):
        self.name=name
        self.n=n
    def get_index_data(self):
        code=indexs[self.name]
        
        df=pro.index_daily(ts_code=code)
        df.index=pd.to_datetime(df.trade_date)
        df=(df.sort_index()).drop('trade_date',axis=1)
        return df[-self.n:] 
   
    def cal_hadata(self):
        df=self.get_index_data()
        #计算修正版K线
        df['ha_close']=(df.close+df.open+df.high+df.low)/4.0
        ha_open=np.zeros(df.shape[0])
        ha_open[0]=df.open[0]
        for i in range(1,df.shape[0]):
            ha_open[i]=(ha_open[i-1]+df['ha_close'][i-1])/2
        df.insert(1,'ha_open',ha_open)
        df['ha_high']=df[['high','ha_open','ha_close']].max(axis=1)
        df['ha_low']=df[['low','ha_open','ha_close']].min(axis=1)
        df=df.iloc[1:]
        return df
    
    def kline_plot(self,ktype=0):
        df=self.cal_hadata()
        #画K线图数据
        date = df.index.strftime('%Y%m%d').tolist()
        if ktype==0:
            k_value = df[['open','close', 'low','high']].values
        else:
            k_value = df[['ha_open','ha_close', 'ha_low', 'ha_high']].values
        #引入pyecharts画图使用的是0.5.11版本，新版命令需要重写
        
        kline = Kline(self.name+'行情走势')
        kline.add('日K线图', date, k_value,
              is_datazoom_show=True,is_splitline_show=False)
        #加入5、20日均线
        df['ma20']=df.close.rolling(20).mean()
        df['ma5']=df.close.rolling(5).mean()
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