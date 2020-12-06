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



def get_code_data(code, start, end):
    df =get_data(ts_code=code, start_date=start, end_date=end)
    df['openinterest']=0
    df=df[['open','high','low','close','amount','openinterest','turnover_rate','pe','pb']]
    return df


class Factor_PE(bt.Strategy):

    def __init__(self):
        pass
    # 全局设定交易策略的参数
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    #
    def next(self):
        if not self.position:  # 没有持仓
            if self.datas[0].turnover_rate[0] < 2.308 and 0 < self.datas[0].pe[0] < 50:
                # 得到当前的账户价值
                total_value = self.broker.getvalue()
                # 1手=100股，满仓买入
                ss = int((total_value / 100) / self.datas[0].close[0]) * 100
                self.order = self.buy(size=ss)
                # self.log('开仓在%f' % self.data.close[0])

        else:  # 持仓，满足条件全部卖出
            if self.datas[0].turnover_rate[0] > 10 or self.datas[0].pe[0] > 80:
                self.close(self.datas[0])
                # self.log('平仓在%f' % self.data.close[0])


class Factor_PE_2(bt.Strategy):
    # 全局设定交易策略的参数
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        for data in self.datas:
            print(data._name)
            # self.log(f"换手率:{data.turnover_rate[0]},市净率:{data.pb[0]},市盈率:{data.pe[0]}")

class ExtraFactor(PandasData):
    lines = ('turnover_rate', 'pe', 'pb',)
    params = (('turnover_rate', -1), ('pe', -1), ('pb', -1),)

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



# 初始化cerebro回测系统设置
cerebro = bt.Cerebro()

#回测期间
start = '20150101'
end = '20201202'
s = get_code_data('603345',start,end)
tr = s['turnover_rate']
tr_mean = tr.mean()


feed = ExtraFactor(dataname=s,name='融捷股份')
print(type(feed))
cerebro.adddata(feed)
cerebro.addstrategy(Factor_PE)

"""
# 加载多个数据
codes =  ['603345','603317','002891']
for c in codes:
    s = get_code_data(c, start, end)
    feed = ExtraFactor(dataname=s,name=c)
    #将数据传入回测系统
    cerebro.adddata(feed)
# 将交易策略加载到回测系统中
cerebro.addstrategy(Factor_PE_2)
"""

startcash = 100000
cerebro.broker.setcash(startcash)
cerebro.broker.setcommission(commission=0.001)

cerebro.run()
# cerebro.plot()

df00,df0,df1,df2,df3,df4=out_result(Factor_PE,feed,startcash = 100000,commission=0.001)

portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash
#打印结果
print(f'期初总资金: {round(startcash,2)}')
print(f'期末总资金: {round(portvalue,2)}')
print(f'净收益: {round(pnl,2)}')
#
# p = kline_plot(s,'神州泰岳')
# p.render()
# plt.show()
print(df00)