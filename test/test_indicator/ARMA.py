import math
from datetime import datetime

from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import statsmodels.api as sm
from arch.unitroot import ADF
from statsmodels.tsa import stattools,arima_model
from statsmodels.graphics.tsaplots import *

"""
模型预测
白噪声验证
单位根验证
ACF和PACF的多图
"""

# '000300.SH', # 沪深300  I
# '510050.SH', # 上证50ETF  FD
s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 4, 24)

GX = dbm.load_bar_dataframe_data(
'300251',Exchange.SZ , Interval.DAILY, start, end
)

# print(len(GX))

returns = getReturn(['300251.SZ'],start,end)
# print(returns.head(3))

RerTrain = returns[:-3]
# print(RerTrain.tail())



# 单位根检验
# print(ADF(RerTrain,max_lags=10).summary().as_text())
"""
   Augmented Dickey-Fuller Results   
=====================================
Test Statistic                 -9.890
P-value                         0.000
Lags                                2
-------------------------------------

Trend: Constant
Critical Values: -3.45 (1%), -2.87 (5%), -2.57 (10%)
Null Hypothesis: The process contains a unit root.
Alternative Hypothesis: The process is weakly stationary.

t统计量小于临界值，拒绝原假设，判断序列是平稳的
"""

# 白噪声判断
# LB = stattools.q_stat(stattools.acf((RerTrain[1:12])),len(RerTrain))
# print(LB[1][-1])
'''
6.334296527278717e-84
远小于0.05，拒绝原假设序列为白噪声，次序列是非白噪声
'''

# 模型识别与估计
# axe1 = plt.subplot(121)
# axe2 = plt.subplot(122)
# plot1 = plot_acf(RerTrain,lags=30,ax=axe1)
# plot2 = plot_pacf(RerTrain,lags=30,ax=axe2)
#
# plt.show()

# 模型建立
# model1 = arima_model.ARMA(RerTrain,order=(1,0,1)).fit()
# model2 = arima_model.ARMA(RerTrain,order=(1,0,2)).fit()
# model3 = arima_model.ARMA(RerTrain,order=(2,0,1)).fit()
# model4 = arima_model.ARMA(RerTrain,order=(2,0,2)).fit()
# model5 = arima_model.ARMA(RerTrain,order=(3,0,1)).fit()
model6 = arima_model.ARMA(RerTrain,order=(3,0,2)).fit()
"""
# print(model1.aic)
# print(model2.aic)
# print(model3.aic)
# print(model4.aic)
# print(model5.aic)
# print(model6.aic)
-1378.8654882799538
-1378.8654882799538
-1378.6358441141479
-1378.6358441141479
-1379.2524615748107
-1379.2524615748107
"""
# 系数的置信区间
# print(model6.conf_int())
# # # 模型的残差
# # stdresid = model6.resid/math.sqrt(model6.sigma2)
# #
# # plt.plot(stdresid)
# # plot_acf(stdresid,lags=20)
# #
# # plt.show()

#预测
# print(model6.forecast(3)[0])
# print(returns.tail(3))