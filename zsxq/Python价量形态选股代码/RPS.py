# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:39:06 2019

@author: zhangjinyi
"""

import pandas as pd
from .base import sql_engine,ts_pro
import matplotlib.pyplot as plt
#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

pro=ts_pro()
engine = sql_engine()

#剔除次新股和st股票
def get_code():
    dd = pro.stock_basic(exchange='', list_status='L')
    #剔除2018年以后上市的新股次新股
    dd=dd[dd['list_date'].apply(int).values<20180101]
    #剔除st股
    dd=dd[-dd['name'].apply(lambda x:x.startswith('*ST'))]
    dd=dd[-dd['name'].apply(lambda x:x.startswith('ST'))]
    #将剩下的股票代码和名称映射为字典
    codes=dd.ts_code.values
    names=dd.name.values
    return codes,names

def get_data(date='20190101'):
    codes,names=get_code()
	#获取最近300天数据
    sql=f'select * from daily_data where trade_date>{date}'
    data=pd.read_sql(sql,engine)
    data=data.sort_values(['ts_code','trade_date'])
	#前复权
    data['adjclose']=data.groupby('ts_code').apply(lambda x:x.close*x.adj_factor/x.adj_factor.iloc[-1]).values
    df=data.set_index(['trade_date','ts_code'])['adjclose']
    #数据重排，列名为代码
    df=df.unstack()
    new_code=list(set(df.columns).intersection(set(codes)))
    df=df[new_code]
    df.rename(columns=dict(zip(codes,names)),inplace=True)
    return df

class RPS(object):
    def __init__(self,data,w_list=[5,20,60,120,250]):
        self.data=data
        self.w_list=w_list
        
    def cal_rps(self,ser):
        df=pd.DataFrame(ser.sort_values(ascending=False))
        df['n']=range(1,len(df)+1)
        df['rps']=(1-df['n']/len(df))*100
        return df.rps
    
    def all_rps(self,w):
        ret=(self.data/self.data.shift(w)-1).iloc[w:].fillna(0)
        rps=ret.T.apply(self.cal_rps)
        return rps.T

    def date_rps(self):
        df=pd.DataFrame()
        for w in self.w_list:
            rps=self.all_rps(w)
            rps.index=(pd.to_datetime(rps.index)).strftime('%Y%m%d')
            rps=rps.T
            df['rps_'+str(w)]=rps.iloc[:,-1]
        return df
        
    def plot_stock_rps(self,stock,n=120):
        df_rps=pd.DataFrame()
        for w in self.w_list:
            df_rps['rps_'+str(w)]=self.all_rps(w)[stock]
        df_rps.iloc[-n:,:].plot(figsize=(16,6))
        plt.title(stock+'RPS相对强度',fontsize=15)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        ax1 = plt.gca()  
        ax1.spines['right'].set_color('none') 
        ax1.spines['top'].set_color('none')
        plt.show()
        
        
if __name__ == "__main__":
    data=get_data(date='20180101')
    rps=RPS(data)
    df=rps.date_rps()
    #print(df.sort_values('rps_250',ascending=False)[:20])
    rps.plot_stock_rps('坚朗五金')