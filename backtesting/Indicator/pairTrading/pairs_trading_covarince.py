import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from arch.unitroot import ADF

from backtesting.Indicator.pairTrading.PairTrading import PairTrading
from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
'''
协整模型
'''
s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 4, 24)
bank_path = s['PATH_BANK']

PA = dbm.load_bar_dataframe_data(
'300251',Exchange.SZ , Interval.DAILY, start, end
)

ZS = dbm.load_bar_dataframe_data(
'600036',Exchange.SH , Interval.DAILY, start, end
)

PAlog = np.log(PA['close_price'])
ZSlog = np.log(ZS['close_price'])

"""
单位根验证对数收盘价为非平稳序列,收益率序列为平稳序列
"""
# adfPA = ADF(PAlog)
# print(adfPA.summary().as_text())
'''
   Augmented Dickey-Fuller Results   
=====================================
Test Statistic                 -1.626
P-value                         0.470
Lags                                0
-------------------------------------

Trend: Constant
Critical Values: -3.45 (1%), -2.87 (5%), -2.57 (10%)
'''
retPA = PAlog.diff()[1:]
# adfretPA = ADF(retPA)
# print(adfretPA.summary().as_text())
'''
   Augmented Dickey-Fuller Results   
=====================================
Test Statistic                 -9.891
P-value                         0.000
Lags                                2
-------------------------------------

Trend: Constant
Critical Values: -3.45 (1%), -2.87 (5%), -2.57 (10%)
Null Hypothesis: The process contains a unit root.
Alternative Hypothesis: The process is weakly stationary.
'''
# adfZS = ADF(ZSlog)
# print(adfZS.summary().as_text())
'''
   Augmented Dickey-Fuller Results   
=====================================
Test Statistic                 -3.659
P-value                         0.005
Lags                                0
-------------------------------------

Trend: Constant
Critical Values: -3.45 (1%), -2.87 (5%), -2.57 (10%)
Null Hypothesis: The process contains a unit root.
Alternative Hypothesis: The process is weakly stationary.
'''
retZS = ZSlog.diff()[1:]
# adfretZS = ADF(retZS)
# print(adfretZS.summary().as_text())
'''
   Augmented Dickey-Fuller Results   
=====================================
Test Statistic                -19.088
P-value                         0.000
Lags                                0
-------------------------------------

Trend: Constant
Critical Values: -3.45 (1%), -2.87 (5%), -2.57 (10%)
Null Hypothesis: The process contains a unit root.
Alternative Hypothesis: The process is weakly stationary.
'''

# PAlog.plot(label='PA',style='--')
# ZSlog.plot(label='ZS',style='-')
# retPA.plot(label='PA',style='--')
# retZS.plot(label='ZS',style='-')
# plt.legend()
"""
最小二乘法构造回归模型
"""
import statsmodels.api as sm

model= sm.OLS(PAlog,sm.add_constant(ZSlog))
result = model.fit()
"""
print(result.summary())
                            OLS Regression Results                            
==============================================================================
Dep. Variable:            close_price   R-squared:                       0.069
Model:                            OLS   Adj. R-squared:                  0.066
Method:                 Least Squares   F-statistic:                     23.62
Date:                Sat, 09 May 2020   Prob (F-statistic):           1.85e-06
Time:                        14:42:28   Log-Likelihood:                 147.35
No. Observations:                 319   AIC:                            -290.7
Df Residuals:                     317   BIC:                            -283.2
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
===============================================================================
                  coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------
const           0.5756      0.331      1.737      0.083      -0.076       1.228
close_price     0.4559      0.094      4.860      0.000       0.271       0.640
==============================================================================
Omnibus:                        7.988   Durbin-Watson:                   0.027
Prob(Omnibus):                  0.018   Jarque-Bera (JB):                5.772
Skew:                          -0.206   Prob(JB):                       0.0558
Kurtosis:                       2.486   Cond. No.                         148.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""
beta = result.params[1]
# 残差
spread = PAlog - beta*ZSlog

print(spread.head())
spread.plot()
# 残差的均值为0,tread设置为c
adfspread = ADF(spread,trend='c')
print(adfspread.summary().as_text())
"""
Name: close_price, dtype: float64
   Augmented Dickey-Fuller Results   
=====================================
Test Statistic                 -1.429
P-value                         0.568
Lags                                0
-------------------------------------

Trend: Constant
Critical Values: -3.45 (1%), -2.87 (5%), -2.57 (10%)
Null Hypothesis: The process contains a unit root.
Alternative Hypothesis: The process is weakly stationary.

不能拒绝原假设，误差太大了

"""
st = PairTrading()
st.setStock(ZSlog,PAlog)
alpha,beta = st.cointegration()
print(alpha,beta)
# plt.show()