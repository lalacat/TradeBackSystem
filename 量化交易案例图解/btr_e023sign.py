# -*- coding: utf-8 -*-
'''
TopQuant-TQ极宽智能量化回溯分析系统
培训课件系列 2019版

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2019.01.011 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化总群，124134140

'''
import sys;

from zsxq.database.base import get_code_data

sys.path.append("topqt/")
#
import matplotlib as mpl
import matplotlib.pyplot as plt
import collections


#
import os,time,arrow,math,random,pytz
import datetime  as dt
#
import backtrader as bt
from backtrader.analyzers import SQN, AnnualReturn, TimeReturn, SharpeRatio,TradeAnalyzer

#
import topquant2019 as tq
#   
#----------------------


# 创建一个：最简单的SMA均线指标类class
# 作为买卖点信号
class SMA_Signal(bt.Indicator):
    #定义信号名称  lines=
    lines = ('mysignal',)
    # 定义MA均线策略的周期参数变量period，默认值是15
    params = (('period', 15),)
    
    # 调用初始化函数
    def __init__(self):
        #增加一个信号参数 mysignal
        #mysignal信号是源自当前的价格数据，与SMA均线价格的差值，默认是收盘价close
        # >0:long，多头信号，买入
        # <0:short，空头信号，卖出
        # =0:None，无操作，
        self.lines.mysignal = self.data - bt.indicators.SMA(period=self.p.period)
        #
        #改用open等其他数据字段测试。也可以是sma，rsi等其他衍生指标数据
        #self.lines.mysignal = self.data.close - bt.indicators.SMA(period=self.p.period)
        #
        #self.lines.mysignal = self.data.open - bt.indicators.SMA(period=self.p.period)
        #self.lines.mysignal = self.data.low - bt.indicators.SMA(period=self.p.period)
        #self.lines.mysignal = self.data.high - bt.indicators.SMA(period=self.p.period)




#----------
        


print('\n#1,设置BT量化回溯程序入口')
cerebro = bt.Cerebro()

#
print('\n#2,设置BT回溯初始参数：起始资金等')
dmoney0=100000.0
cerebro.broker.setcash(dmoney0)
dcash0=cerebro.broker.startingcash

#
#
print('\n\t#2-2,设置数据文件，数据文件，需要按时间字段，正序排序')
rs0='data/stk/'
xcod='002046'
fdat=rs0+xcod+'.csv'
print('\t@数据文件名：',fdat)

# 
print('\t设置数据BT回溯运算：起始时间、结束时间')  
print('\t数据文件,可以是股票期货、外汇黄金、数字货币等交易数据')  
print('\t格式为：标准OHLC格式，可以是日线、分时数据。')  
t0str,t9str='2018-10-01','2018-12-31'
data=bt.feeds.PandasData(dataname=get_code_data(xcod,t0str,t9str))

#
# 增加一个股票名称变量xcod，可以在策略函数、绘图中使用
cerebro.adddata(data,name=xcod)
#
#
print('\n\t#2-3,添加BT量化回溯程序，对应的买卖点signal信号参数')
print('\t# 案例当中，使用的是SMA均线与当前价格的差值，作为买卖点信号')
print('\t# 买入long，卖出shrot信号，都是采用这个')
cerebro.add_signal(bt.SIGNAL_LONGSHORT, SMA_Signal,period=15)
#
print('\n\t#2-4,添加broker经纪人佣金，默认为：千一')
cerebro.broker.setcommission(commission=0.001)
#
print('\n\t#2-5,设置每手交易数目为：10，不使用默认值：1手')
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

print('\n\t#2-5,设置addanalyzer分析参数')
      
cerebro.addanalyzer(SQN)
#
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio', legacyannual=True)
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
#
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')

      
#
print('\n#3,调用BT回溯入口程序，开始执行run量化回溯运算')
results=cerebro.run()

#
print('\n#4,完成BT量化回溯运算')
dval9=cerebro.broker.getvalue()   
dget=dval9-dcash0
kret=dget/dcash0*100
# 最终投资组合价值
print('\t起始资金 Starting Portfolio Value: %.2f' % dcash0)
print('\t资产总值 Final Portfolio Value: %.2f' % dval9)
print('\t利润总额:  %.2f,' % dget)
print('\tROI投资回报率 Return on investment: %.2f %%' % kret)

#
#---------
print('\n#8,analyzer分析BT量化回测数据')
strat =results[0]
anzs=strat.analyzers
#
dsharp=anzs.SharpeRatio.get_analysis()['sharperatio']
trade_info=anzs.TradeAnalyzer.get_analysis()
#
dw=anzs.DW.get_analysis()
max_drowdown_len =dw['max']['len']
max_drowdown =dw['max']['drawdown']
max_drowdown_money =dw['max']['moneydown']
#
print('\t夏普指数SharpeRatio : ',dsharp)
print('\t最大回撤周期 max_drowdown_len : ', max_drowdown_len)
print('\t最大回撤 max_drowdown : ', max_drowdown)
print('\t最大回撤(资金)max_drowdown_money : ', max_drowdown_money)

#---------
#
print('\n#9,绘制BT量化分析图形')
cerebro.plot(iplot=False)

#---------
#
print('\nzok')
#---------------
'''

-12.45,     @data
-12.45,     @data.close
2.202       @data.open
2.32        @data.low
-8.56       @data.high

'''
 


