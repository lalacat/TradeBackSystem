#!/usr/bin/env python
# coding: utf-8

import backtrader as bt
import pandas as pd
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from backtrader.feeds import PandasData
from pyecharts import Kline, Bar,Overlap
from pylab import mpl

from zsxq.backtrader数据扩展功能.zjy_plot import plot_result, out_result
from zsxq.database.base import get_data

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False



def get_sheet_data(path,sheet_name=None):
    # 基础信息
    data = pd.read_excel(path, sheet_name=3 ,header=1)
    name = data['公司'].iloc[0]
    code = data['代码'].iloc[0]
    d = data.iloc[:, -6:-1]
    d.columns = ['trade_data', 'down', 'mid_01', 'mid_02', 'up']
    d.index = pd.to_datetime(d['trade_data'], format='%Y%m%d')
    d['mid'] = (d['mid_01'] + d['mid_02']) / 2
    value_data = d[['down', 'mid', 'up']]
    start= d.index[0].strftime('%Y%m%d')

    # 交易信息
    df =get_data(ts_code=code[:-3], start_date=start)
    df['openinterest']=0
    final = pd.concat([df, value_data], axis=1)
    final=final[['open','high','low','close','amount','openinterest','down','mid','up']]
    final.columns = ['open','high','low','close','volume','openinterest','down','mid','up']
    return final,name


class Factor_JL(bt.Strategy):

    def __init__(self):
        self.close = self.data.close
        self.open  = self.data.open
        self.down = self.data.down
        self.up = self.data.up
        self.mid = self.data.mid
        self.Jl = LinesJl(self.data)
    # 全局设定交易策略的参数
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    #
    def next(self):
        if not self.position:  # 没有持仓
            if self.close[-1] <= self.down[-1] :
                # 得到当前的账户价值
                total_value = self.broker.getvalue()
                # 1手=100股，满仓买入
                ss = int((total_value / 100) / self.open[0]) * 100
                self.order = self.buy(size=ss)
                self.log('开仓在%f' % self.data.close[0])

        elif self.close[-1]> self.up[-1] :
                self.close(self.open[0])
                self.log('平仓在%f' % self.data.close[0])

    def start(self):
        self.log('{%s}进行回测' % self.data._name)


class FactorJL(PandasData):
    lines = ('down', 'mid', 'up',)
    params = (('down', -1), ('mid', -1), ('up', -1),)

class LinesJl(bt.Indicator):
    lines = ('down','mid','up',)
    plotinfo = dict(subplot=True)

    def __init__(self):
        self.lines.down = self.data.down
        self.lines.mid = self.data.mid
        self.lines.up = self.data.up

def kline_plot(df,name):
    #画K线图数据
    date = df.index.strftime('%Y%m%d').tolist()
    k_value = df[['open','close', 'low','high']].values
    #引入pyecharts画图使用的是0.5.11版本，新版命令需要重写
    kline = Kline(name+'行情走势')
    kline.add('日K线图', date, k_value,
              is_datazoom_show=True,is_splitline_show=False)
    #成交量
    bar = Bar()
    bar.add('成交量', date, df['amount'],tooltip_tragger='axis',
                is_legend_show=False, is_yaxis_show=False,
                yaxis_max=5*max(df['amount']))
    overlap = Overlap()
    overlap.add(kline)
    overlap.add(bar,yaxis_index=1, is_add_yaxis=True)
    return overlap

path1 = r'X:\股票\君临计划-消费.xlsx'



# 初始化cerebro回测系统设置
cerebro = bt.Cerebro()

#回测期间

data,name= get_sheet_data(path1)



feed = FactorJL(dataname=data,name=name)
cerebro.adddata(feed)
cerebro.addstrategy(Factor_JL)


startcash = 100000
cerebro.broker.setcash(startcash)
cerebro.broker.setcommission(commission=0.001)

cerebro.run()
#
# portvalue = cerebro.broker.getvalue()
# pnl = portvalue - startcash
# #打印结果
# print(f'期初总资金: {round(startcash,2)}')
# print(f'期末总资金: {round(portvalue,2)}')
# print(f'净收益: {round(pnl,2)}')





cerebro.plot(iplot=False)

