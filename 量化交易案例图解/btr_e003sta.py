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
import os,time,arrow,math,random,pytz
import datetime  as dt
#
import backtrader as bt
import topquant2019 as tq
#
#from IPython.display import display, Image
import matplotlib.pyplot as plt
#import pylab as plt

#
#----------------------

# 创建一个自定义策略类class
class TQSta001(bt.Strategy):

    def log(self, txt, dt=None):
        # log记录函数
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 默认数据，一般使用股票池当中，下标为0的股票，
        # 通常使用close收盘价，作为主要分析数据字段
        self.dataclose = self.datas[0].close

    def next(self):
        # next函数是最重要的trade交易（运算分析）函数， 
        # 调用log函数，输出BT回溯过程当中，工作节点数据包BAR，对应的close收盘价
        self.log('Close收盘价, %.2f' % self.dataclose[0])


#-------------

#----
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
t0str,t9str='2018-01-01','2018-12-31'
data=bt.feeds.PandasData(dataname=get_code_data(xcod,t0str,t9str))

#
cerebro.adddata(data)
#
print('\n\t#2-3,添加BT量化回溯程序，对应的策略参数')
cerebro.addstrategy(TQSta001)
#
print('\n#3,调用BT回溯入口程序，开始执行run量化回溯运算')
cerebro.run()

#
print('\n#4,完成BT量化回溯运算')
dval9=cerebro.broker.getvalue()   
print('\t起始资金 Starting Portfolio Value: %.2f' % dcash0)
print('\t资产总值 Final Portfolio Value: %.2f' % dval9)
#
#---------
#
#plt.figure(0)
print('\n#9,绘制BT量化分析图形')
cerebro.plot(iplot=False)
plt.show()

#---------
#
print('\nzok')
