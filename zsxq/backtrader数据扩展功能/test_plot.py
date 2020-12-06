import datetime
import math

import backtrader as bt

from zsxq.database.base import get_data
from pylab import mpl

from zsxq.backtrader数据扩展功能.zjy_plot import plot_result, out_result
from zsxq.database.base import get_data

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

class St(bt.Strategy):
    # 交易紀錄
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    # 設定交易參數
    params = dict(
        ma_period_short=5,
        ma_period_long=10
    )

    def __init__(self):
        # 均線交叉策略
        sma1 = bt.ind.SMA(period=self.p.ma_period_short)
        sma2 = bt.ind.SMA(period=self.p.ma_period_long)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

        # 使用自訂的sizer函數，將帳上的錢all-in
        self.setsizer(sizer())

        # 用開盤價做交易
        self.dataopen = self.datas[0].open

    def next(self):
        # 帳戶沒有部位
        if not self.position:
            # 5ma往上穿越20ma
            if self.crossover > 0:
                # 印出買賣日期與價位
                self.log('BUY ' + ', Price: ' + str(self.dataopen[0]))
                # 使用開盤價買入標的
                self.buy(price=self.dataopen[0])
        # 5ma往下穿越20ma
        elif self.crossover < 0:
            # 印出買賣日期與價位
            self.log('SELL ' + ', Price: ' + str(self.dataopen[0]))
            # 使用開盤價賣出標的
            self.close(price=self.dataopen[0])

    # 計算交易部位


class sizer(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return math.floor(cash / data[1])
        else:
            return self.broker.getposition(data)


start = '20200101'
end = '20201202'
def get_code_data(code, start, end):
    df =get_data(ts_code=code, start_date=start, end_date=end)
    df['openinterest']=0
    df=df[['open','high','low','close','amount','openinterest']]
    return df

s = get_code_data('603345',start,end)
p = '.\\test.csv'
data = bt.feeds.PandasData(dataname=s)
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot(volume=False,iplot=False)