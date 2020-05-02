
from datetime import datetime

import matplotlib.pyplot as plt
import numpy
import pandas as pd
from scipy import stats

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
各种分布
伯努利分布
正态分布
卡方分布
t分布
F分布
"""
s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)

# 二项分布的应用：预测上涨下跌的概率
# 分组
RJ['FLAG']=0
RJ.loc[RJ['close_price'] >= RJ['open_price'],['FLAG']] = 'positive'
RJ.loc[RJ['close_price'] < RJ['open_price'],['FLAG']] = 'negotive'
up_down = RJ.groupby('FLAG')
# 上涨的概率
p_up = len(up_down.get_group('positive'))/len(RJ)
# print(p_up)
# 下跌的概率
p_down = len(up_down.get_group('negotive'))/len(RJ)
# print(p_down)
# 未来10天中4天上涨的概率
prob = stats.binom.pmf(4,10,p_up)
# print(prob)


# 正态分布的应用：计算VAR
# 收益
return_rj = RJ['close_price'].pct_change().dropna()
# 均值
mean_rj = return_rj.mean()
# 方差
std_rj = return_rj.std()
print(std_rj)
print(return_rj.var()**0.5)
# 95%
VAR_95= stats.norm.ppf(0.05,mean_rj,std_rj)
print(VAR_95)


# 卡方分布
x = numpy.arange(0,5,0.002)
# plt.subplot(311)
# plt.plot(x,stats.chi.pdf(x,10))
# plt.subplot(312)
# t分布
# y = numpy.arange(-5,5,0.002)
# plt.plot(y,stats.t.pdf(y,5))

# F分布
plt.plot(numpy.arange(0,5,0.002),stats.f.pdf(numpy.arange(0,5,0.002),4,40))
plt.show()