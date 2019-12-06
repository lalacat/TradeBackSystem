from datetime import datetime
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import pandas as pd
from scipy.stats import norm

import matplotlib.pyplot as plt

s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2019, 11, 22)
RJ = dbm.load_bar_dataframe_data(
'600196',Exchange.SH , Interval.DAILY, start, end
)

FX = dbm.load_bar_dataframe_data(
        '600196',Exchange.SH , Interval.DAILY, start, end
    )

FX_returns = FX.close_price.pct_change().dropna()
print(FX_returns.std())

close = RJ['close_price']
lagclose = close.shift(1)
Calclose = pd.DataFrame({'close':close,'lagclose':lagclose})

simpleret = (close-lagclose)/lagclose
simpleret.name = 'simpleret'
print(simpleret.std())


# 半方差
def cal_half_dev(returns):
    mu = returns.mean()
    temp = returns[returns<mu]
    half_dev = ((sum(mu-temp)**2)/len(returns))**0.5
    return half_dev

RJ_half_dev = cal_half_dev(simpleret)

print(RJ_half_dev)

# VAR
# 历史模拟法分位函数
rj_var = simpleret.quantile(0.05)
print(rj_var)

# 协方差矩阵法
rj_var_cov = norm.ppf(0.05,simpleret.mean(),simpleret.std())
print(rj_var_cov)

# ES
rj_es = simpleret[simpleret<=simpleret.quantile(0.05)].mean()
print(rj_es)