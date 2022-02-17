#!/usr/bin/env python
# coding: utf-8

# # 引言
# 题材概念是主力炒作永恒的主题。市场的本质是资金驱动市，资金驱动的核心是主力。很多人都在复杂的理论、指标、图形和消息上折腾，把对股市的理解复杂化，理论的作用扩大化，没有从实践上去认识。题材是市场资金达成共识的工具，而题材的级别大小和想象力大小则决定了股票上涨的空间，级别越大，空间越大。市场的本质就是市场的主要矛盾，不外乎六点：经济、政策、情绪、资金、技术和外围环境。一旦出现赚钱效应，首先看的是那个整体板块在领涨，这个板块是什么概念，是不是当下的大热点？选股就是先看热点板块，龙头股与题材有关，题材代表了一个板块，不会是单打独斗，关注热点板块，在板块中选股非常重要。发现最大题材板块后，核心是找龙大。在整个板块中最先上涨，涨势最强的个股就一定要关注并分析。

# In[69]:


import pandas as pd
import numpy as np
#可视化：matplotlib、seaborn、pyecharts
import matplotlib.pyplot as plt
import seaborn as sns
#正确显示中文和负号
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
#这里的pyecharts使用的是0.5.11版本
from pyecharts import Bar,HeatMap
#导入时间处理模块
from dateutil.parser import parse
from datetime import datetime,timedelta
#pandas赋值老提升警告
import warnings
warnings.filterwarnings('ignore')
#使用tushare pro获取数据，需要到官网注册获取相应的token
# import tushare as ts
# token='输入你的token'
# pro=ts.pro_api(token)


# # 数据获取与探索性分析

# ## 同花顺概念和行业列表

# In[70]:


# index_list=pro.ths_index()
# #查看数据前几行
# index_list.head()


# In[71]:


#数据保存本地
#index_list.to_csv('index_list.csv')
#读取本地数据
index_list=pd.read_csv('index_list.csv',index_col=0)


# 其中，ts_code：代码；name：名称；count：成分个数；exchange：交易所，包括A股、港股（H）和美股（US）；list_date：上市日期；type：指数类型N-板块指数，I-行业指数，S-同花顺特色指数。

# In[72]:


def plot_bar(data,title,label=True,zoom=False):
    bar=Bar('')
    attr=list(data.index)
    v=list(data.values)
    bar.add(title,attr,v,is_label_show=label,
           is_splitline_show=False,
           is_datazoom_show=zoom)
    return bar


# In[73]:


data=index_list.groupby('exchange')['name'].count()
title='同花顺概念和行业指数\nA股\港股\美股'
plot_bar(data,title)


# 下面主要分析A股上的同花顺概念和行业指数

# In[74]:


A_index_list=index_list.query("exchange=='A'")
A_index_list=A_index_list.copy()
A_index_list['nums']=pd.to_numeric(A_index_list['count'])
#去掉缺失值
A_index_list.dropna(inplace=True)
A_index_list['nums'].describe()


# 概念或行业成分个股数量太多或太少，相当于涵盖面太宽泛或代表性不足，分析起来意义不大。

# In[75]:


#删除代码重复项，筛掉概念成份个股数量低于12大于52（相当于取25%到75%分位数）
#保留type为N板块的指数
final_index_list=(A_index_list
                  .drop_duplicates(subset=['ts_code'], keep='first')
                 .query("12<nums<52")
                 .query("type=='N'"))
#去掉样本股或成份股指数
final_index_list=final_index_list[-final_index_list.name.apply(lambda s:s.endswith('样本股')or s.endswith('成份股'))]
final_index_list.sort_values('nums')


# In[76]:


data=(final_index_list.sort_values('nums',ascending=False)
      .set_index('name')['nums'])
title='同花顺概念和行业指数成分股个数'
plot_bar(data,title,False,True)


# ## 获取概念行业指数行情
# 通过日期循环获取某时间段所有概念行业指数行情数据

# In[77]:


#获取股票交易日历
def get_cals():
    #获取交易日历
    cals=pro.trade_cal(exchange='')
    cals=cals[cals.is_open==1].cal_date.values
    return cals
    
#获取某段时间内的交易日期（如200个交易日）
def get_trade_date(n):
    #获取当天日期时间
    d0=datetime.now()
    if d0.hour>20:
        d=d0.strftime('%Y%m%d')
    else:
        d=(d0-timedelta(1)).strftime('%Y%m%d')
    while d not in get_cals():
        d1=parse(d)
        d=(d1-timedelta(1)).strftime('%Y%m%d')
    #当前交易日在交易日历的索引
    n1=np.where(get_cals()==d)[0][0]
    #起始日期
    n0=n1-n+1
    return n0,n1
#获取某段时间内的概念指数行情数据

def get_index_data(n=200):
    n0,n1=get_trade_date(n)
    date1=get_cals()[n1]
    #获取起始日期至结束日期数据
    df=pro.ths_daily(trade_date=date1)
    for date in get_cals()[n0:n1]:
        temp=pro.ths_daily(trade_date=date)
        df=pd.concat([df,temp])
    return df


# In[78]:


#通过tushare在线获取数据
all_data=get_index_data(n=200)
#数据保存本地
#all_data.to_csv('all_data.csv')
#通过本地导入数据
#all_data=pd.read_csv('all_data.csv',index_col=0)
all_data.head()


# In[79]:


#删除重复缺失值、将代码使用概念中文名代替
final_data=(all_data.sort_values(['ts_code','trade_date'])
            .drop_duplicates()
            .set_index(['trade_date','ts_code'])['close'].unstack()
            .dropna(axis=1)
            .rename(columns=dict(index_list[['ts_code','name']].values)))
final_data.tail()


# # 热点板块与个股监测分析

# ## 计算板块指数收益率

# In[80]:


def date_ret(data,w_list=[1,5,20,60,120]):
    df=pd.DataFrame()
    for w in w_list:
        df[str(w)+'日收益率%']=(((data/data.shift(w)-1)*100)
                            .round(2)
                            .iloc[w:]
                            .fillna(0)
                            .T
                            .iloc[:,-1])
    return df


# In[81]:


date_ret(final_data).sort_values('120日收益率%',ascending=False)


# 120日涨幅居前板块指数

# In[82]:


date_ret(final_data).sort_values('120日收益率%',ascending=False)[:10]


# 120日跌幅最多的前五个板块指数

# In[83]:


date_ret(final_data).sort_values('120日收益率%',ascending=True)[:5]


# ## 概念板块指数周期涨跌幅可视化

# In[84]:


#使用pyecharts0.5.11版本可视化
def out_chart(w=120):
    col=str(w)+'日收益率%'
    ddd=date_ret(final_data).sort_values(col,ascending=False)[col]
    x=list(ddd.index)
    y=list(ddd.values)
    bar=Bar(f"同花顺概念指数{w}日收益率(%)",title_text_size=15,title_pos='center')
    bar.add("", x,y,is_label_show=False, is_datazoom_show=True)
    return bar


# In[85]:


#最近一个交易日
#图形为html动态交互式，可通过拖曳查看所有概念指数的详细涨跌幅
out_chart(1)


# In[86]:


#近5个交易日
out_chart(5)


# In[87]:


#近20个交易日
#out_chart(20)


# In[88]:


#近120个交易日
out_chart(120)


# In[89]:


#由于同花顺指数行情数据获取不到下面概念，需剔除
xx=['华为汽车', '盐湖提锂', '鸿蒙概念', '共同富裕示范区', 'MCU芯片', '牙科医疗', 
    'CRO概念', '钠离子电池', '工业母机', '北交所概念', 'NFT概念', '抽水蓄能', 
    '换电概念', '海峡两岸', 'WiFi 6', '智能制造', 'EDR概念', '动力电池回收', 
    '汽车芯片', '传感器', '柔性直流输电', '虚拟数字人', '预制菜', '幽门螺杆菌概念']
sss=final_data[set(final_index_list.name.values)-set(xx)]
import seaborn as sns
pt = ((sss/sss.shift(1)-1)*100).round(2)[-10:]
plt.figure(figsize=(25,5))
sns.heatmap(pt, linewidths = 0.05,cmap='Reds');


# ## 热点板块成分股

# In[90]:


#注意，写作本文是交易日期为20220209,即默认end='20220209'.
def get_stock_price(code,start='20200101'):
    df=ts.pro_bar(ts_code=code, start_date=start,adj='hfq')
    df.index=pd.to_datetime(df.trade_date)
    df=df.sort_index()
    return df.close
def all_stock_price(name):
    #name为同花顺概念行业中文名称
    dd=pro.ths_member(ts_code=dict(index_list[['name','ts_code']].values)[name])
    df0=pd.DataFrame()
    for code,name in dict(dd[['code','name']].values).items():
        df0[name]=get_stock_price(code)
    df1=df0.fillna(method='ffill')
    return df1
def stock_rets_rank(name,p=120):
    data=all_stock_price(name)
    #p为period，即时间窗口
    col=str(p)+'日收益率%'
    rank_ret=date_ret(data).sort_values(col,ascending=False)
    return rank_ret


# In[91]:


stock_rets_rank('钾肥')


# In[92]:


stock_rets_rank('数字货币')


# In[93]:


stock_rets_rank('数字货币',p=1)[:20]


# 热力图监测热点板块个股

# In[94]:


def stock_heat(name='数字货币'):
    #name为板块指数名称，如数字货币
    #具体指数名称可通过index_list获取
    sss=all_stock_price(name)
    yy = ((sss/sss.shift(1)-1)*100).round(2)[-10:]
    yy.index=yy.index.strftime('%Y%m%d')
    y_axis = list(yy.index)
    x_axis = list(yy.columns)
    data = [[i, j, yy.loc[j,i]] for i in x_axis for j in y_axis]
    heatmap = HeatMap()
    heatmap.add(name+
    "板块个股涨跌",
    x_axis,
    y_axis,
    data,
    visual_range=[-20,20],   
    is_visualmap=True,
    visual_text_color="#000",
    visual_orient="horizontal",
    is_label_show=True,
    is_datazoom_show=True
    )
    return heatmap


# In[95]:


stock_heat('数字货币')

