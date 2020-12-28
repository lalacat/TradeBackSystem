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
# import os,time,arrow,math,random,pytz
import datetime  as dt
#
import backtrader as bt
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
        self.log('收盘价Close, %.2f' % self.dataclose[0])
        #
        # 使用经典的"三连跌"买入策略
        if self.dataclose[0] < self.dataclose[-1]:
            # 当前close价格，低于昨天（前一天，[-1]）
            if self.dataclose[-1] < self.dataclose[-2]:
                # 昨天的close价格（前一天，[-1]），低于前天（前两天，[-2]）
                # "三连跌"买入信号成立:
                # BUY, BUY, BUY!!!，买！买！买！使用默认参数交易：数量、佣金等
                self.log('设置买单 BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


#----------
#

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
t0str,t9str='20180101','20181231'
data= bt.feeds.PandasData(dataname=get_code_data(xcod,t0str,t9str))

#
cerebro.adddata(data)

#
print('\n\t#2-3,添加BT量化回溯程序，对应的策略参数')
cerebro.addstrategy(TQSta001)
#
print('\n#3,调用BT回溯入口程序，开始执行run量化回溯运算')
print('\t注意输出文本信息的变化')      
cerebro.run()

#
print('\n#4,完成BT量化回溯运算')
dval9=cerebro.broker.getvalue()   
kret=(dval9-dcash0)/dcash0*100
# 最终投资组合价值
print('\t起始资金 Starting Portfolio Value: %.2f' % dcash0)
print('\t资产总值 Final Portfolio Value: %.2f' % dval9)
print('\tROI投资回报率 Return on investment: %.2f %%' % kret)
#
#---------
#
print('\n#9,绘制BT量化分析图形')
print('\t注意图形当中,最上面的的cash现金，value资产曲线')
print('\t注意图形当中的买点图标，以及对应的曲线波动')
cerebro.plot(iplot=False)

#---------
#
print('\nzok')
