from datetime import datetime

from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
from statsmodels.tsa import stattools
from statsmodels.graphics.tsaplots import *
from arch.unitroot import ADF

"""
时间序列的自相关性
自相关性的绘图
平稳性的检验
单位根检验
白噪声检验
Ljung-Box检验
"""
# '000300.SH', # 沪深300  I
# '510050.SH', # 上证50ETF  FD
s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 4, 24)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)

returns = RJ['close_price'].pct_change().dropna()
returns.name = 'return'
# returns.plot()
# returns.column = ['return']
# print(returns)

# 计算自相关系数
# acfs = stattools.acf(returns)
# # print(acfs)
# # 偏自相关系数
# pacfs = stattools.pacf(returns)
# # print(pacfs)
# # 自相关性图
# plot_acf(returns,use_vlines=True,lags=30)
# # 偏自相关性图
# plot_pacf(returns,use_vlines=True,lags=30)
# plot_acf(RJ['close_price'],use_vlines=True,lags=30)
#
# plt.show()

# 单位根检验
# adfRJ= ADF(returns)
# print(adfRJ.summary().as_text())
# adfClose = ADF(RJ['close_price'])
# print(adfClose.summary().as_text())

# 白噪声检验
LB = stattools.q_stat(stattools.acf(returns),len(returns))
print(LB)