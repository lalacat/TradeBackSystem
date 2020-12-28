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
sys.path.append("topqt/")
#
import matplotlib as mpl
import matplotlib.pyplot as plt


#
import os,time,arrow,math,random,pytz
import datetime  as dt
#
import backtrader as bt
import topquant2019 as tq

#   
#----------------------

# 创建一个：最简单的MA均线策略类class
class ma(bt.Strategy):
    # 定义MA均线策略的周期参数变量，默认值是15
    # 增加类一个log打印开关变量： fgPrint，默认自是关闭
    params = (('period', 15),('fgPrint', False), )

        
    def log(self, txt, dt=None, fgPrint=False):
        # 增强型log记录函数，带fgPrint打印开关变量
        if self.params.fgPrint or fgPrint:
            dt = dt or self.datas[0].datetime.date(0)
            tn=tq.timNSec('',self.tim0wrk)
            #print('%s, %s，tn：%.2f' % (dt.isoformat(), txt))
            print('%s, %s，tim：%.2f s' % (dt.isoformat(), txt,tn))            

    def __init__(self,vdict={}):
        # 默认数据，一般使用股票池当中，下标为0的股票，
        # 通常使用close收盘价，作为主要分析数据字段
        self.dataclose = self.datas[0].close
        #
        #
        if len(vdict)>0:
            self.p.period=int(vdict.get('period'))
            

        # 跟踪track交易中的订单（pending orders），成交价格，佣金费用
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.tim0wrk=arrow.now()
        
        # 增加一个均线指标：indicator
        # 注意，参数变量period，主要在这里使用
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.period)

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
                self.log('卖单执行SELL EXECUTED,成交价： %.2f,小计 Cost: %.2f,佣金 Comm %.2f'  
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
            if self.dataclose[0] < self.sma[0]:
                # 如果当前close收盘价<当前的ma均价
                # ma均线策略，买入信号成立:
                # BUY, BUY, BUY!!!，买！买！买！使用默认参数交易：数量、佣金等
                self.log('设置买单 BUY CREATE, %.2f, name : %s' % (self.dataclose[0],self.datas[0]._name))

                # 采用track模式，设置order订单，回避第二张订单2nd order，连续交易问题
                self.order = self.buy()
                
        else:
            # 如果该股票仓位>0 ，可以进行SELL卖出操作，
            # 这个仓位设置模式，也可以修改相关参数，进行调整
            # 使用最简单的MA均线策略
            if self.dataclose[0] > self.sma[0]:
                # 如果当前close收盘价>当前的ma均价
                # ma均线策略，卖出信号成立:
                # 默认卖出该股票全部数额，使用默认参数交易：数量、佣金等
                self.log('SELL CREATE, %.2f, name : %s' % (self.dataclose[0],self.datas[0]._name))

                # 采用track模式，设置order订单，回避第二张订单2nd order，连续交易问题
                self.order = self.sell()        

    def stop(self):
        # 新增加一个stop策略完成函数
        # 用于输出执行后数据
        self.log('(策略参数 Period=%2d) ，最终资产总值： %.2f' %
                 (self.params.period, self.broker.getvalue()), fgPrint=True)



# 多参数opt测试,均线交叉策略
class ma_cross(bt.Strategy):
    params = (('nfast', 10), ('nslow', 30),('fgPrint', False),) 
    
    def log(self, txt, dt=None, fgPrint=False):
        ''' Logging function fot this strategy'''
        if self.params.fgPrint or fgPrint:
            dt = dt or self.datas[0].datetime.date(0)
            tn=tq.timNSec('',self.tim0wrk)
            #print('%s, %s，tn：%.2f' % (dt.isoformat(), txt))
            print('%s, %s，tim：%.2f s' % (dt.isoformat(), txt,tn))

    def __init__(self,vdict={}):
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.tim0wrk=arrow.now()
        #
        #self.dataclose = self.datas[0].close
        #print('@@vdict',vdict)
        #
        if len(vdict)>0:
            self.p.nfast=int(vdict.get('nfast'))
            self.p.nslow=int(vdict.get('nslow'))
        
        #
        sma_fast,sma_slow,self.buysig={},{},{}
        for xc,xdat in enumerate(self.datas):
            sma_fast[xc] =bt.ind.SMA(xdat,period=self.p.nfast) 
            #sma_fast[xc] =bt.ind.SMA(xdat,period=self.p.nfast) 
            sma_slow[xc] =bt.ind.SMA(xdat,period=self.p.nslow) 
            self.buysig[xc] = bt.ind.CrossOver(sma_fast[xc], sma_slow[xc])
        #

      

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        #
        if self.order:
            return

        #
        for xc,xdat in enumerate(self.datas):
            xnam=xdat._name
            fgInx=xnam.find('inx_')>=0
            #print('@n',xnam,fgInx)
            if not fgInx:
                xpos = self.getposition(xdat)
                #xnam=xdat.line.name
                xss=' {:.02},@ : {} # {}'.format(xdat.close[0],xnam,xc)
                if xpos.size:
                    #if (self.buysig[xc] < 0)and(self.buysig[0] < 0):
                    if (self.buysig[xc] < 0):
                        self.log('SELL'+xss)
                        #self.log('    @@SELL CREATE, %.2f, %'  % (self.datas[xc].close[0],self.data0_Name))
                        self.sell(data=xdat)
                        
                #elif (self.buysig[xc] > 0)and(self.buysig[0] > 0):
                elif (self.buysig[xc] > 0):
                    self.log('BUY'+xss)
                    #self.log('    @@buy CREATE, %.2f'  % (self.datas[xc].close[0]))
                    #self.log('    @@buy CREATE, %.2f, %'  % (self.datas[xc].close[0],self.datas[xc].Name))
                    self.buy(data=xdat)
                    #
                    #self.order = self.sell(data=xdat,exectype=bt.Order.StopTrail,trailpercent=0.0618)
            


    def stop(self):
        #tn=arrow.now()-self.tim0wrk
        self.log('策略参数 nfast= %2d, nslow= %2d，资产总值：%.2f' %
                 (self.p.nfast,self.p.nslow, self.broker.getvalue()), fgPrint=True)


#----------------------
print('\n#1,设置BT量化回溯全局变量qx，并初始化')
qx=tq.tq_init('TQ01',cash0=1000000.0)
#
#

#
print('\n\t#2-1,设置数据文件，数据文件，需要按时间字段，正序排序')
#rs0='/TQDat/day/'
rs0='data/'
rsyb0,rbas0=rs0+'stk/',rs0+'inx/'

#
print('\t设置指数池，股票池代码')  
#baslst=['000001','399001','000002','000003'] #上证，深证，A股，B股
baslst=['000001'] #上证，深证，A股，B股
syblst=['002046','600663','600809','600648','600600','600638']
#syblst=['000001','002046']
#
print('\t设置数据BT回溯运算：起始时间、结束时间')  
print('\t数据文件,可以是股票期货、外汇黄金、数字货币等交易数据')  
print('\t格式为：标准OHLC格式，可以是日线、分时数据。')  
tim0str,tim9str='2018-01-01','2018-12-31'
#
print('\t读取股票池、指数池数据')  
#tq.pools_get4flst(qx,rbas0,baslst,tim0str,tim9str,fgInx=True)
tq.pools_get4flst(qx,rsyb0,syblst,tim0str,tim9str,fgInx=False)

#------------
print('\n#2-2,设置BT常用基本参数，anzMod为分析模式，默认为0')
tq.bt_set(qx,anzMod=1)
#
#
#---------
print('\n#3,调用BT回溯入口程序，开始执行量化回溯opt参数优化函数')
#原版optstrategy策略优化函数api接口
##cerebro.optstrategy(MyStrategy, myparam1=range(10, 20))
#
print('\n#3-1,单参数自动寻优测试')
d10=list(range(5, 50,5))
sgnlst=['period']
x100=tq.bt_opt(qx,ma,[d10],sgnlst)
#xxx
#
#print('\n#3-2,多参数自动寻优测试')
#d10=list(range(5, 35,5))
#d20=list(range(10, 190,20))
#sgnlst=['nfast','nslow']
#vlst=[d10,d20]
#x100=tq.bt_opt(qx,ma_cross,vlst,sgnlst)

#------------
print('\n@@x.end#9，没有plot绘图，analyzer分析部分')
#qx.plot(figsize=(1500,500))


print('\nzok')
                
 


