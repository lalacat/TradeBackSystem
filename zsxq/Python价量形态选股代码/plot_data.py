# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:15:36 2019

@author: zhangjinyi
"""

import pandas as pd

#设置数据库引擎
from sqlalchemy import create_engine
engine = create_engine('sqlite:///c:\\zjy\\select_stock\\stock_data.db')

from pyecharts import Bar

def plot_data(condition,title):
    #distinct删除重复值
    sql="select distinct * from daily_basic where trade_date>'20190101' and "+ condition
    data=pd.read_sql(sql,engine)
    count_=data.groupby('trade_date')['ts_code'].count()
    attr=count_.index
    v1=count_.values
    bar=Bar(title,title_text_size=15)
    bar.add('',attr,v1,is_splitline_show=False,is_datazoom_show=True,linewidth=2)
    bar.render(title+'.html')

if __name__ == "__main__":
    c1="close<2"
    t1="股价低于2元个股时间分布"
    #plot_data(c1,t1)
    c2="pe<30 and pe>0"
    t2="市盈率低于30倍数量"
    plot_data(c2,t2)





