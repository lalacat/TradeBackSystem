from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
单期收益率
多期收益率
"""


s = Settings()

dbm = init('_',s)
start = datetime(2018, 11, 23)
end = datetime(2020, 4, 20)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
# print(RJ)
print(RJ['2018'])




close = RJ['close_price']
lagclose = close.shift(1)
Calclose = pd.DataFrame({'close':close,'lagclose':lagclose})
# print(Calclose.head(5))
simpleret = (close-lagclose)/lagclose
simpleret.name = 'simpleret'
# print(simpleret.head(5))

fig,ax1 = plt.subplots()
plt.plot(close,'b')

simpleret2=(close-close.shift(2))/close.shift(2)
simpleret2.name = 'simpleret2'
# print(simpleret2.head(5))
ax2 = ax1.twinx()
cum_return = (1+simpleret).cumprod()
plt.plot(cum_return)


# 年化
# annualize = (1+simpleret).cumprod()[-1]**(252/len(simpleret))-1
# print(annualize)


# 复利
comporet = np.log(close/lagclose)
comporet.name = 'comporet'
print(comporet.head(5))
plt.show()
# 多期复利
comporet2 = np.log(close/close.shift(2))
comporet2.name = 'comporet2'
print(comporet2.head(5))
