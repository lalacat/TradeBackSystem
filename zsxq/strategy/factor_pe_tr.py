#!/usr/bin/env python
# coding: utf-8

import backtrader as bt
import pandas as pd
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from backtrader.feeds import PandasData
from pylab import mpl

from zsxq.database.base import get_data

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False



def get_code_data(code, start, end):
    df =get_data(ts_code=code, start_date=start, end_date=end)
    df['openinterest']=0
    df=df[['open','high','low','close','amount','openinterest','turnover_rate','pe','pb']]
    return df


class Factor_PE(bt.Strategy):
    # 全局设定交易策略的参数
    params=(
        ('maperiod',5),
           )

    def __init__(self):
        #指定价格序列
        self.dataclose=self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None

        #添加移动均线指标，内置了talib模块
        self.sma = bt.indicators.SimpleMovingAverage(
                      self.datas[0], period=self.params.maperiod)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        self.log(f"换手率:{self.datas[0].turnover_rate[0]},市净率:{self.datas[0].pb[0]},市盈率:{self.datas[0].pe[0]}")


class ExtraFactor(PandasData):
    lines = ('turnover_rate', 'pe', 'pb',)
    params = (('turnover_rate', -1), ('pe', -1), ('pb', -1),)

# 初始化cerebro回测系统设置
cerebro = bt.Cerebro()
#回测期间
start = '20190101'
end = '20201202'
# 加载数据
s = get_code_data('002475', start, end)
feed = ExtraFactor(dataname=s)
#将数据传入回测系统
cerebro.adddata(feed)
# 将交易策略加载到回测系统中
cerebro.addstrategy(Factor_PE)
cerebro.run()
