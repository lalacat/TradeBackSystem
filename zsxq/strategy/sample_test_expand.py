#!/usr/bin/env python
# coding: utf-8

import backtrader as bt
from backtrader.feeds import PandasData

import pandas as pd
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False


token = 'e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d'
pro = ts.pro_api(token)
def get_code_data(code, start, end):
    df = pro.daily(ts_code=code, start_date=start, end_date=end)
    # df['openinterest']=0
    # print(df.columns)
    # df.index = pd.to_datetime(df['trade_date'])
    # df=df[['open','high','low','close','amount','openinterest']]
    data2 = pro.daily_basic(ts_code=code, fields='trade_date,turnover_rate,pe,pb')
    data = pd.merge(df, data2, on='trade_date')
    data.index = pd.to_datetime(data.trade_date)
    data = data.sort_index()
    data['volume'] = data.vol
    data['openinterest'] = 0
    data['datetime'] = pd.to_datetime(data.trade_date)
    data = data[['datetime', 'open', 'high', 'low', 'close', \
                 'volume', 'openinterest', 'turnover_rate', 'pe', 'pb']]
    data = data.fillna(0)
    return data

s = get_code_data('002475.SZ','20200101','20201101')
print(s)


class my_strategy1(bt.Strategy):
    # 全局设定交易策略的参数
    params=(
        ('maperiod',5),
           )

    def __init__(self):
        #指定价格序列
        self.dataclose=self.datas[0].close
        print(self.dataclose)
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None

        #添加移动均线指标，内置了talib模块
        self.sma = bt.indicators.SimpleMovingAverage(
                      self.datas[0], period=self.params.maperiod)

    def next(self):
        if self.order: # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        print(self.dataclose[0])
        print(self.sma[0])
        if not self.position: # 没有持仓
            #执行买入条件判断：收盘价格上涨突破20日均线
            if self.dataclose[0] > self.sma[0]:
                #执行买入
                self.order = self.buy(size=500)
        else:
            #执行卖出条件判断：收盘价格跌破20日均线
            if self.dataclose[0] < self.sma[0]:
                #执行卖出
                self.order = self.sell(size=500)
class Addmoredata(PandasData):
    lines = ('turnover_rate','pe','pb',)
    params = (('turnover_rate',7),('pe',8),('pb',9),)

def main():
    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    #回测期间
    start=datetime(2020, 1, 1)
    end=datetime(2020,11, 1)
    # 加载数据
    data = bt.feeds.PandasData(dataname=s,fromdate=start,todate=end)
    #将数据传入回测系统
    cerebro.adddata(data)
    # 将交易策略加载到回测系统中
    cerebro.addstrategy(my_strategy1)
    # 设置初始资本为10,000
    startcash = 10000
    cerebro.broker.setcash(startcash)
    # 设置交易手续费为 0.2%
    cerebro.broker.setcommission(commission=0.002)
    #股票交易的手续费一般由交易佣金、印花税、过户费3部分组成，其中佣金不同证券公司的收费不同，一般在买卖金额的0.1%-0.3%之间，最低收费为5元

    d1=start.strftime('%Y%m%d')
    d2=end.strftime('%Y%m%d')
    print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')
    #运行回测系统
    cerebro.run()
    #获取回测结束后的总资金
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash
    #打印结果
    print(f'总资金: {round(portvalue,2)}')
    print(f'净收益: {round(pnl,2)}')
