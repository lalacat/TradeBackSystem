from datetime import datetime

from scipy import  stats
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
FX = dbm.load_bar_dataframe_data(
        '600196',Exchange.SH , Interval.DAILY, start, end
    )
RJ_returns = RJ.close_price.pct_change().dropna()
FX_returns = FX.close_price.pct_change().dropna()

# 均值
RJ_means= RJ_returns.mean()
FX_means= FX_returns.mean()


# 标准差
RJ_std = RJ_returns.std()
FX_std = FX_returns.std()

# 区间估计
RJ_valuation = stats.t.interval(0.95,len(RJ_returns)-1,RJ_means,RJ_std)
print(RJ_valuation)
# print(RJ_std)

plt.subplot(211)
plt.hist(RJ_returns)
plt.plot(np.arange(-0.1,0.1,0.000001),stats.norm.pdf(np.arange(-0.1,0.1,0.000001),RJ_means,RJ_std))
plt.title('融捷收益率分布')

plt.subplot(212)
plt.hist(FX_returns)
plt.plot(np.arange(-0.1,0.1,0.000001),stats.norm.pdf(np.arange(-0.1,0.1,0.000001),FX_means,FX_std))
plt.title('复星收益率分布')
plt.show()