# -*- coding: utf-8 -*-
'''
TopQuant-TQ极宽智能量化回溯分析系统
培训课件系列 2019版

Top极宽量化(原zw量化)，Python量化第一品牌 
by Top极宽·量化开源团队 2019.01.011 首发

网站： www.TopQuant.vip      www.ziwang.com
QQ群: Top极宽量化总群，124134140

'''

#

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
import topq_edu2019 as tqedu
#   
#----------------------
#
rs0='data/'     #rs0='/TQData/'
rsyb0,rbas0=rs0+'stk/',rs0+'inx/'
syblst=['002046','600663']
baslst=['000001']  #上证
tim0str,tim9str='2018-01-01','2018-12-31'
#
qx=tq.tq_init('TQ01')
#
tq.pools_get4flst(qx,rsyb0,syblst,tim0str,tim9str,fgInx=False)
tq.pools_get4flst(qx,rbas0,baslst,tim0str,tim9str,fgInx=True)
#
tq.bt_set(qx,anzMod=1)
#
qx.cb.addstrategy(tqedu.ma)
#
qx.bt_results= qx.cb.run() 
#
qx.cb.plot()
tq.bt_anz(qx)
#
tq.bt_anz_folio(qx)
