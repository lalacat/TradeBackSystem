from datetime import datetime

import numpy
from  scipy import stats

import matplotlib.pyplot as plt
import pandas as pd
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings


"""
高斯密度函数的绘图

"""
s = Settings()

dbm = init('_',s)
start = datetime(2015, 1, 1)
end = datetime(2020, 3, 31)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
# 收益率
# rj = RJ['close_price'].pct_change()
RJ_returns = (RJ['close_price']-RJ['close_price'].shift(1))/RJ['close_price'].shift(1)
df_returns = pd.DataFrame(RJ_returns).dropna()
# 高斯密度函数
density = stats.kde.gaussian_kde(df_returns.iloc[:1000,0])
bins = numpy.arange(-0.2,0.2,0.00001)
print(density)
plt.subplot(211)
# 概率密度函数
plt.plot(bins,density(bins))
plt.subplot(212)
# 累积密度函数
plt.plot(bins,density(bins).cumsum())
plt.show()