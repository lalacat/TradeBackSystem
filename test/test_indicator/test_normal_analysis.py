
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
groupy（）的应用
涉及到pandas判定条件筛选行
apply()的应用

"""

s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
# 分组
RJ['FLAG']=0
# 链式索引会报错
# RJ['FLAG'][RJ['close_price']>=RJ['open_price']]='positive'
# RJ['FLAG'][RJ['close_price']<RJ['open_price']]='negotive'
RJ.loc[RJ['close_price']>=RJ['open_price'],['FLAG']]= 'positive'
RJ.loc[RJ['close_price']<RJ['open_price'],['FLAG']] = 'negotive'
flag = RJ.groupby('FLAG')
for name,group in flag:
    print(name)
    print(group)
# 统计方法
# all_information = RJ['close_price'].describe()
# print(all_information)

# close_price = RJ['close_price']
# print(close_price.head(3))

# 函数应用
# 将每一列的数据应用到函数中
# col_max_value = RJ.apply(max,axis=0)
# print(col_max_value)
# 将每一列的数据应用到函数中
# row_max_value = RJ.apply(max,axis=1)
