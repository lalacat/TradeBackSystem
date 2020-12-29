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

#
import os,time,arrow,math,random,pytz
import datetime  as dt
#
import backtrader as bt
#
#----------------------
# 创建一个：最简单的MA均线策略类class
class TQSta001(bt.Strategy):
    # 定义MA均线策略的周期参数变量，默认值是15
    # 增加类一个log打印开关变量： fgPrint，默认自是关闭
    params = (
        ('maperiod', 15),
        ('fgPrint', False),
    )

        
    def log(self, txt, dt=None, fgPrint=False):
        # 增强型log记录函数，带fgPrint打印开关变量
        if self.params.fgPrint or fgPrint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 默认数据，一般使用股票池当中，下标为0的股票，
        # 通常使用close收盘价，作为主要分析数据字段
        self.dataclose = self.datas[0].close

        # 跟踪track交易中的订单（pending orders），成交价格，佣金费用
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # 增加一个均线指标：indicator
        # 注意，参数变量maperiod，主要在这里使用
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 检查订单执行状态order.status：
            # Buy/Sell order submitted/accepted to/by broker 
            # broker经纪人：submitted提交/accepted接受,Buy买单/Sell卖单
            # 正常流程，无需额外操作
            return

        # 检查订单order是否完成
        # 注意: 如果现金不足，经纪人broker会拒绝订单reject order
        # 可以修改相关参数，调整进行空头交易
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行BUY EXECUTED,成交价： %.2f,小计 Cost: %.2f,佣金 Comm %.2f'  
                         % (order.executed.price,order.executed.value,order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('卖单执行SELL EXECUTED,成交价： %.2f,小计 Cost: %.2f,佣金 Comm %.2f'  
                         % (order.executed.price,order.executed.value,order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单Order： 取消Canceled/保证金Margin/拒绝Rejected')

        # 检查完成，没有交易中订单（pending order）
        self.order = None

    def notify_trade(self, trade):
        # 检查交易trade是关闭
        if not trade.isclosed:
            return

        self.log('交易操盘利润OPERATION PROFIT, 毛利GROSS %.2f, 净利NET %.2f' %
                 (trade.pnl, trade.pnlcomm)) 
             

    def next(self):
        # next函数是最重要的trade交易（运算分析）函数， 
        # 调用log函数，输出BT回溯过程当中，工作节点数据包BAR，对应的close收盘价
        self.log('当前收盘价Close, %.2f' % self.dataclose[0])
        #
        #
        # 检查订单执行情况，默认每次只能执行一张order订单交易，可以修改相关参数，进行调整
        if self.order:
            return
        #
        # 检查当前股票的仓位position
        if not self.position:
            #
            # 如果该股票仓位为0 ，可以进行BUY买入操作，
            # 这个仓位设置模式，也可以修改相关参数，进行调整
            #
            # 使用最简单的MA均线策略
            if self.dataclose[0] > self.sma[0]:
                # 如果当前close收盘价>当前的ma均价
                # ma均线策略，买入信号成立:
                # BUY, BUY, BUY!!!，买！买！买！使用默认参数交易：数量、佣金等
                self.log('设置买单 BUY CREATE, %.2f, name : %s' % (self.dataclose[0],self.datas[0]._name))

                # 采用track模式，设置order订单，回避第二张订单2nd order，连续交易问题
                self.order = self.buy()
                
        else:
            # 如果该股票仓位>0 ，可以进行SELL卖出操作，
            # 这个仓位设置模式，也可以修改相关参数，进行调整
            # 使用最简单的MA均线策略
            if self.dataclose[0] < self.sma[0]:
                # 如果当前close收盘价<当前的ma均价
                # ma均线策略，卖出信号成立:
                # 默认卖出该股票全部数额，使用默认参数交易：数量、佣金等
                self.log('SELL CREATE, %.2f, name : %s' % (self.dataclose[0],self.datas[0]._name))

                # 采用track模式，设置order订单，回避第二张订单2nd order，连续交易问题
                self.order = self.sell()        

    def stop(self):
        # 新增加一个stop策略完成函数
        # 用于输出执行后带数据
        self.log('(MA均线周期变量Period= %2d) ，最终资产总值： %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), fgPrint=True)
#
#-------------------- kline        
tq10_corUp,tq10_corDown=['#7F7F7F','#17BECF'] #plotly               
tq09_corUp,tq09_corDown=['#B61000','#0061B3']
tq08_corUp,tq08_corDown=['#FB3320','#020AF0']
tq07_corUp,tq07_corDown=['#B0F76D','#E1440F']
tq06_corUp,tq06_corDown=['#FF3333','#47D8D8']
tq05_corUp,tq05_corDown=['#FB0200','#007E00']
tq04_corUp,tq04_corDown=['#18DEF5','#E38323']
tq03_corUp,tq03_corDown=['black','blue']
tq02_corUp,tq02_corDown=['red','blue']
tq01_corUp,tq01_corDown=['red','lime']
#
tq_ksty01=dict(volup=tq01_corUp,voldown=tq01_corDown,barup =tq01_corUp,bardown =tq01_corDown)
tq_ksty02=dict(volup=tq02_corUp,voldown=tq02_corDown,barup =tq02_corUp,bardown =tq02_corDown)
tq_ksty03=dict(volup=tq03_corUp,voldown=tq03_corDown,barup =tq03_corUp,bardown =tq03_corDown)
tq_ksty04=dict(volup=tq04_corUp,voldown=tq04_corDown,barup =tq04_corUp,bardown =tq04_corDown)
tq_ksty05=dict(volup=tq05_corUp,voldown=tq05_corDown,barup =tq05_corUp,bardown =tq05_corDown)
tq_ksty06=dict(volup=tq06_corUp,voldown=tq06_corDown,barup =tq06_corUp,bardown =tq06_corDown)
tq_ksty07=dict(volup=tq07_corUp,voldown=tq07_corDown,barup =tq07_corUp,bardown =tq07_corDown)
tq_ksty08=dict(volup=tq08_corUp,voldown=tq08_corDown,barup =tq08_corUp,bardown =tq08_corDown)
tq_ksty09=dict(volup=tq09_corUp,voldown=tq09_corDown,barup =tq09_corUp,bardown =tq09_corDown)
tq_ksty10=dict(volup=tq10_corUp,voldown=tq10_corDown,barup =tq10_corUp,bardown =tq10_corDown)



class MyBuySell(bt.observers.BuySell):
    plotlines = dict(
        buy=dict(marker='$\u21E7$', markersize=12.0),  #arrow
        sell=dict(marker='$\u21E9$', markersize=12.0)
        #
        # buy=dict(marker='$++$', markersize=12.0),
        # sell=dict(marker='$--$', markersize=12.0)
        #
        # buy=dict(marker='$✔$', markersize=12.0),
        # sell=dict(marker='$✘$', markersize=12.0)
    )

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
print('\n\t#2-2,设置数据文件，需要按时间字段，正序排序')
rs0='data/stk/'
xcod='002046'
fdat=rs0+xcod+'.csv'
print('\t@数据文件名：',fdat)

# 
print('\t设置数据BT回溯运算：起始时间、结束时间')  
print('\t数据文件,可以是股票期货、外汇黄金、数字货币等交易数据')  
print('\t格式为：标准OHLC格式，可以是日线、分时数据。')  
t0str,t9str='2010-01-01','2018-12-31'
t0str,t9str='2018-10-01','2018-12-31'
#t0str,t9str='',''
data=bt.feeds.PandasData(dataname=get_code_data(xcod,t0str,t9str))
#
#----ha-k
data.addfilter(bt.filters.HeikinAshi)


# 增加一个股票名称变量xcod，可以自策略函数内部使用
cerebro.adddata(data,name=xcod)
#
#
print('\n\t#2-3,添加BT量化回溯程序，对应的策略参数')
print('\n\t# 案例当中，使用的是MA均线策略')
cerebro.addstrategy(TQSta001)
#
print('\n\t#2-4,添加broker经纪人佣金，默认为：千一')
cerebro.broker.setcommission(commission=0.001)
#
print('\n\t#2-5,设置每手交易数目为：10，不再使用默认值：1手')
cerebro.addsizer(bt.sizers.FixedSize, stake=10)
#
# 相当于增加了一个子图，显示Value的
# cerebro.addobserver(bt.observers.Value)
# cerebro.addobserver(bt.observers)
bt.observers.BuySell = MyBuySell
#bt.observers.BuySell = tq.ksyb_BuySell(xmbuy='$++$',xmsell='$--$')
#bt.observers.BuySell = tq.ksyb_BuySell
#

print('\n#3,调用BT回溯入口程序，开始执行run量化回溯运算')
cerebro.run() #shape,size

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
print('\n\t分别运行一下各种不同参数的plot绘图命令')
print('\t注意每次运行只运行一条plot，其他的用#注释符号屏蔽')
print('\t部分参数设置后，如果不清除变量，reset运行环境，效果会一直存在')
print('\t注意各种不同参数，引起的图形变化')
#cerebro.plot()                 #默认模式
#
#
#1 arrow
#cerebro.plot() 

#1 sty-cor+arrow
#cerebro.plot(style='bar',**tq_ksty10)
cerebro.plot(style='candle',**tq_ksty09,iplot=False)


#
#2 volume
# cerebro.plot(volume =False)             #取消volume成交量图形，默认为 True
# cerebro.plot(volume =True,voloverlay=True,iplot=False)        #volume成交量：采用subplot子图模式，默认为voloverlay=True叠加模式
#
#3
#plot多图拼接，BT版的股市：《清明上河图》
#注意修改其实日期参数为：空字符串
#numfigs，默认值为：1
# cerebro.plot(numfigs=1,iplot=False)

#5 ha-k line
# cerebro.plot(style='candle',iplot=False)
#



#---------
#
print('\nzok')
                
 
'''
Renko Bricks — backtrader documentation 
https://www.backtrader.com/blog/posts/2017-06-26-renko-bricks/renko-bricks.html?highlight=renko

从k线图看backtrader的专业细节 – 极宽 
http://www.topquant.vip/?p=792
'''

