import matplotlib.pyplot as plt  # python matplotlib 绘图
import numpy as np
import pandas as pd;

from datetime import datetime
from scipy import stats
import statsmodels.api as sm
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
"""
最小二乘法的实现
立讯和歌尔收益率的拟合
作图
坐标按时间截取
线性，正态性，同方差性
"""
s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 3, 30)
LX = dbm.load_bar_dataframe_data('002475',Exchange.SZ , Interval.DAILY, start, end,True)
GE = dbm.load_bar_dataframe_data('002241',Exchange.SZ , Interval.DAILY, start, end,True)

LX['return'] = LX['close_price'].pct_change()
GE['return'] = GE['close_price'].pct_change()
print(GE['return'].tail(3))
LX = LX.dropna()
GE = GE.dropna()
# print(LX)
# print(GE)
# print(GE.index)
# 构建模型
model = sm.OLS(GE['return'],sm.add_constant(LX['return'])).fit()
# print(model.summary())
# 拟合参数的预测值
# print(model.fittedvalues)


'''
# 拟合值和实际值的对比
plt.plot(LX['return'],GE['return'],'o', label='data')
plt.plot(LX['return'],model.fittedvalues,'r--.',label='OLS')
plt.plot(GE.index,GE['return'],'o', label='data')
plt.plot(GE.index,model.fittedvalues,'r--.',label='OLS')
# plt.legend()
# plt.axis((datetime(2019,3,30),datetime(2019,6,30),-0.25,0.25))
'''

'''
# 线性
plt.scatter(model.fittedvalues,model.resid)
plt.xlabel('fittedvalues')
plt.ylabel('resid')
plt.show()
'''

"""
# 正态性
# Residuals, normalized to have unit variance.残差正态化
sm.qqplot(model.resid_pearson,stats.norm,line='45')
plt.show()
"""

# 同方差
plt.scatter(model.fittedvalues,model.resid_pearson**0.5)
plt.xlabel('fittedvalues')
plt.ylabel('normalize resid')
plt.show()