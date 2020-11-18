#!/usr/bin/env python
# coding: utf-8
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

from backtesting.example.cofficient.cofficient_General import Coff_General

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

import tushare as ts
token='e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d'
pro=ts.pro_api(token)


#获取交易日历
def get_cal_date(start,end=None):
    cal_date=pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date=cal_date[cal_date.is_open==1]
    dates=cal_date.cal_date.values
    return dates


start='20200101'
# trade_data = get_cal_date('20200101')
# print(trade_data)



#获取指数数据
def get_index_data(code,start,end):
    index_df = pro.index_daily(ts_code=code, start_date=start,end_date=end)
    index_df.index=pd.to_datetime(index_df.trade_date)
    index_df=index_df.sort_index()
    return index_df

#获取北向资金数据
def get_north_money(start,end):
    #获取交易日历
    dates=get_cal_date(start,end)
    #tushare限制流量，每次只能获取300条记录
    df=pro.moneyflow_hsgt(start_date=start, end_date=end)
    if len(datas) <= 300:
        df = df.drop_duplicates()
        df.index = pd.to_datetime(df.trade_date)
        df = df.sort_index()
        return df
    else:
        #拆分时间进行拼接，再删除重复项
        for i in range(0,len(dates)-300,300):
            d0=pro.moneyflow_hsgt(start_date=dates[i], end_date=dates[i+300])
            df=pd.concat([d0,df])
            #删除重复项
            df=df.drop_duplicates()
            df.index=pd.to_datetime(df.trade_date)
            df=df.sort_index()
        return df

#获取指数数据
#常用大盘指数
indexs={'上证综指': '000001.SH','深证成指': '399001.SZ','沪深300': '000300.SH',
       '创业板指': '399006.SZ','上证50': '000016.SH','中证500': '000905.SH',
       '中小板指': '399005.SZ','上证180': '000010.SH'}
all_code = {
    '融捷股份':'002192.SZ','卫宁健康':'300253.SZ',
    # '安井食品': '603345.SH', '天味食品': '603317.SH', '中宠股份': '002891.SZ'
    }
start='20200101'
# end='20200812'
# 当前时间
now = datetime.strftime(datetime.now(),'%Y%m%d')
new_path = 'X:\\股票\\stock.xlsx'
index_path = 'X:\\股票\\indexs.xlsx'



def download_index(cg,start,end):
    index_data=pd.DataFrame()
    for name,code in indexs.items():
        index_data[name]=get_index_data(code,start,end)['close']
    cg.save_excel(index_data,index_path,'index')


cg = Coff_General()

# 自选股
def read_selfcode(cg,now,end):
    datas = cg.read_excel(all_code,new_path,(start,end))
    new_name= {}
    for n,v in all_code.items():
        new_name[v]=n
    datas.columns = [new_name.get(n) for n in datas.columns]
    return datas


datas = cg.read_excel(indexs,index_path,(start,now),'index')
#累计收益
# (datas/datas.iloc[0]).plot(figsize=(14,6))
# plt.title('A股指数累积收益率\n 2014-2020',size=15)
# plt.show()

#将价格数据转为收益率
all_ret=datas/datas.shift(1)-1
north_data=get_north_money(start,now)
all_data=all_ret.join(north_data['north_money'],how='inner')
all_data.rename(columns={'north_money':'北向资金'},inplace=True)
all_data.dropna(inplace=True)
# print(all_data.corr())




import seaborn as sns

"""
# plt.figure(figsize=(10, 6))
# sns.regplot(x=list(all_data["北向资金"][-120:]),y=list(all_data["卫宁健康"][-120:]))
# plt.title('卫宁健康与北向资金拟合回归线',size=15)
# plt.xlabel('北向资金',size=12)
# plt.ylabel('卫宁健康收益率',size=12)
# plt.show()

# final_data=all_data[['卫宁健康','北向资金']].dropna()
# final_data.plot(secondary_y='北向资金',figsize=(12,6))
# plt.title('卫宁健康日收益率 VS 北向资金',size=15)
# plt.show()
"""

#沪深300指数收益率与北向资金
final_data=all_data[['沪深300','北向资金']].dropna()
# final_data.plot(secondary_y='北向资金',figsize=(12,6))
# plt.title('沪深300日收益率 VS 北向资金',size=15)
# plt.show()



def cal_rol_cor(data,period=30):
    cors=data.rolling(period).corr()
    # list[param1:param2:param3]
    # param1，相当于start_index，可以为空，默认是0
    # param2，相当于end_index，可以为空，默认是list.size
    # param3，步长，默认为1。步长为 - 1时，返回倒序原序列
    cors=cors.dropna().iloc[1::2,0]
    cors=cors.dropna()
    cors=cors.reset_index()
    cors=cors.set_index('trade_date')
    print(cors['level_1'])
    return cors['沪深300']


# cor=cal_rol_cor(final_data,period=30)
# print(cor.describe())
# cor.plot(figsize=(14,6),label='移动120日相关系数')
# plt.title('沪深300与北向资金移动120日相关系数',size=15)
# plt.axhline(cor.mean(), c='r',label='相关系数均值=0.33')
# plt.legend(loc=2)
# plt.show()
