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
import datetime  as dt
import pandas as pd
#
import backtrader as bt
import matplotlib.pyplot as plt
#

#
#----------------------

def pools_get4fn(fnam,tim0str,tim9str,fgSort=True):
    # 数据读取函数，兼容csv标准OHLC数据格式文件
    df = pd.read_csv(fnam, index_col=0, parse_dates=True)
    df.sort_index(ascending=fgSort,inplace=True)  #True：正序
    #
    tim0=None if tim0str=='' else dt.datetime.strptime(tim0str,'%Y-%m-%d')
    tim9=None if tim9str=='' else dt.datetime.strptime(tim9str,'%Y-%m-%d')
    #
    df['openinterest'] = 0
    print(df.head(10))
    #
    data = bt.feeds.PandasData(dataname=df,fromdate=tim0,todate =tim9)
    #
    return data
#----------------------
#
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

t0str,t9str='2018-11-01','2018-12-31'
data=pools_get4fn(fdat,t0str,t9str)
#
cerebro.adddata(data)

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
print('\n#9,绘制BT量化分析图形')
cerebro.plot(iplot=False)
plt.show()
#
print('\nzok')




