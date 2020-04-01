import tushare as ts
from datetime import datetime

from scipy import  stats
from statsmodels.stats import anova

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

s = Settings()

dbm = init('_',s)
start = datetime(2019, 11, 23)
end = datetime(2019, 11, 28)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
print(RJ)

close = RJ['close_price']
lagclose = close.shift(1)
Calclose = pd.DataFrame({'close':close,'lagclose':lagclose})
# print(Calclose.head(5))
simpleret = (close-lagclose)/lagclose
simpleret.name = 'simpleret'
# print(simpleret.head(5))
# plt.plot(simpleret)

simpleret2=(close-close.shift(2))/close.shift(2)
simpleret2.name = 'simpleret2'
# print(simpleret2.head(5))

cum_return = (1+simpleret).cumprod()-1
plt.plot(cum_return)


# 年化
# annualize = (1+simpleret).cumprod()[-1]**(252/len(simpleret))-1
# print(annualize)


# 复利
comporet = np.log(close/lagclose)
comporet.name = 'comporet'
print(comporet.head(5))
# plt.show()
# 多期复利
comporet2 = np.log(close/close.shift(2))
comporet2.name = 'comporet2'
print(comporet2.head(5))
