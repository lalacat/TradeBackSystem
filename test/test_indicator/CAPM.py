from datetime import datetime

from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import statsmodels.api as sm
"""
散点图
OLS应用
"""

# '000300.SH', # 沪深300  I
# '510050.SH', # 上证50ETF  FD
s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 4, 24)
HS_300 = dbm.load_bar_dataframe_data(
'000300',Exchange.SH , Interval.DAILY, start, end
)
# print(len(HS_300))

GX = dbm.load_bar_dataframe_data(
'300251',Exchange.SZ , Interval.DAILY, start, end
)

# print(len(GX))

returns = getReturn(['300251.SZ','000300.SH'],start,end)


rf = 1.036**(1/360)-1

Eret = returns - rf

print(Eret.head())
# plt.scatter(Eret.values[:,0],Eret.values[:,1])
# plt.show()


# 拟合CAPM模型
model = sm.OLS(Eret['300251'][1:],sm.add_constant(Eret['000300'][1:]))
result = model.fit()
print(result.summary())