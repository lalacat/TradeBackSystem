import tushare as ts
from datetime import datetime

from scipy import  stats
from statsmodels.stats import anova

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 11, 22)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
print(RJ)
RJ_returns = RJ.close_price.pct_change().dropna()
RJ['return'] = RJ_returns
a= RJ.fillna(0)
# print(a)
model = sm.OLS(a['return'],sm.add_constant(a['volume'])).fit()
# print(model.summary())
# 拟合值
fitvalue = model.fittedvalues
# print(fitvalue)
# plt.subplot(311)
# plt.plot(fitvalue)
#
# # 残差检验
# plt.subplot(312)
# plt.scatter(fitvalue,model.resid)
#
# plt.show()

# 正态性假设
# sm.qqplot(model.resid_pearson,stats.norm,line='45')

# 同方差
plt.scatter(fitvalue,model.resid_pearson**0.5)
plt.show()