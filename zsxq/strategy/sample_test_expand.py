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


def _get_cal_date(start, end=None):
    cal_date = pro.trade_cal(exchange='', start_date=start, end_date=end)
    cal_date = cal_date[cal_date.is_open == 1]
    dates = cal_date.cal_date.values
    return dates
def get_north_money(start, end):
    # 获取交易日历
    dates = _get_cal_date(start, end)
    # tushare限制流量，每次只能获取300条记录
    df = pro.moneyflow_hsgt(start_date=start, end_date=end)
    if len(df) <= 300:
        df = df.drop_duplicates()
    else:
        # 拆分时间进行拼接，再删除重复项
        for i in range(0, len(dates) - 300, 300):
            d0 = pro.moneyflow_hsgt(start_date=dates[i], end_date=dates[i + 300])
            df = pd.concat([d0, df])
            # 删除重复项
            df = df.drop_duplicates()
    return df
def get_code_data(code, start,end):
    df = pro.daily(ts_code=code, start_date=start,end_date=end)
    data2 = get_north_money(start,end)
    data=pd.merge(df,data2,on='trade_date')
    data.index = pd.to_datetime(data.trade_date)
    data = data.sort_index()
    data['datetime'] = pd.to_datetime(data.trade_date)
    data = data[['datetime', 'open', 'high', 'low', 'close', \
                 'vol', 'north_money']]
    data = data.fillna(0)
    data['signal']=0
    return data

s = get_code_data('002475.SZ','20201101','20201124')
s2 = get_code_data('002192.SZ','20201101','20201124')
print(s)
print(s2)


class my_strategy1(bt.Strategy):
    # 默认参数
    params = (('long_period', 10),
              ('short_period', 5),
              ('printlog', False),)
    def __init__(self):
        self.order = None
        self.buyprice = 0
        self.buycomm = 0
        self.buy_size = 0
        self.buy_count = 0
        self.closeprice1 = self.data[0]
        self.closeprice2 = self.data1[-1]

        # 海龟交易法则中的唐奇安通道和平均波幅ATR
        # self.H_line = bt.indicators.Highest(self.data.high(-1), period=self.p.long_period)
        # self.L_line = bt.indicators.Lowest(self.data.low(-1), period=self.p.short_period)
        # self.TR = bt.indicators.Max((self.data.high(0) - self.data.low(0)), \
        #                             abs(self.data.close(-1) - self.data.high(0)), \
        #                             abs(self.data.close(-1) - self.data.low(0)))
        # self.ATR = bt.indicators.SimpleMovingAverage(self.TR, period=14)
        # # 价格与上下轨线的交叉
        # self.buy_signal = bt.ind.CrossOver(self.data.close(0), self.H_line)
        # self.sell_signal = bt.ind.CrossOver(self.data.close(0), self.L_line)
        #
        # print(self.closeprice1)
        # print(self.closeprice2)
        bt.indicators.ATR(self.data.close(0), plot=True)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        print(len(self))
        self.log(f"北向资金:{self.datas[0].north_money[0]}")



class NorthMoney(PandasData):
    lines = ('north_money',)
    params = (('north_money',-1),)




def main():
    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()
    #回测期间
    start=datetime(2020, 11, 1)
    end=datetime(2020,11, 24)
    # 加载数据
    data = NorthMoney(dataname=s,fromdate=start,todate=end)
    data2 = NorthMoney(dataname=s2,fromdate=start,todate=end)
    #将数据传入回测系统
    cerebro.adddata(data)
    cerebro.adddata(data2)
    # 将交易策略加载到回测系统中
    cerebro.addstrategy(my_strategy1)
    cerebro.run()
    cerebro.plot()


if __name__ == '__main__':
    main()

