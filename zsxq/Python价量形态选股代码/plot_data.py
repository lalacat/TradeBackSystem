# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:15:36 2019

@author: zhangjinyi
"""

import pandas as pd

#设置数据库引擎
# from pyecharts.charts import Bar
# from sqlalchemy import create_engine

from zsxq.database.base import sql_engine

# engine = sql_engine('sqlite:///c:\\zjy\\select_stock\\stock_data.db')
engine = sql_engine()

from pyecharts.charts import Bar

def plot_data(condition,title):
    #distinct删除重复值
    table_names = pd.read_sql(
        "select name from sqlite_master where type='table' order by name",engine).values
    if 'sqlite_sequence' in table_names:
        table_names = table_names[:-1]
    all_tables = table_names
    temp = None
    n = 1
    for table in all_tables[:100]:

        sql=f"select distinct * from '{table[0]}' where trade_date>'20190101' and "+ condition
        data=pd.read_sql(sql,engine)
        print(f"第{n}/{len(all_tables[:100])}:{table[0]}已筛选！")
        if temp is None:
            temp = data
        else:
            temp = pd.concat([data, temp], axis=0)
        n += 1
    count_=temp.groupby('trade_date')['ts_code'].count()
    # print(count_)
    attr=count_.index.values.tolist()
    v1=count_.values.tolist()

    bar=Bar()
    # # bar= BAR(title)
    bar.add_xaxis(attr)
    bar.add_yaxis('',v1)
    # # bar.add('',attr,v1,is_splitline_show=False,is_datazoom_show=True,linewidth=2)
    # bar.render()

    bar.render(title+'.html')

if __name__ == "__main__":
    c1="close<20"
    # t1="股价低于20元个股时间分布"
    # plot_data(c1,t1)
    c2="pe<30"
    t2="市盈率低于30倍数量"
    plot_data(c2,t2)









