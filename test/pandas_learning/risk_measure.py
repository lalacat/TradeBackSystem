from datetime import datetime

import pandas as pd
from scipy.stats import norm

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
计算常见的风险度量
VAR和ES
最大回撤
"""



s = Settings()

dbm = init('_',s)
start = datetime(2019, 11, 1)
end = datetime(2019, 11, 22)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)

close = RJ['close_price']
lagclose = close.shift(1)
Calclose = pd.DataFrame({'close':close,'lagclose':lagclose})

simpleret = (close-lagclose)/lagclose
simpleret = simpleret.dropna()
simpleret.name = 'simpleret'
print(simpleret.std())


# 半方差
def cal_half_dev(returns):
    mu = returns.mean()
    temp = returns[returns<mu]
    half_dev = ((sum(mu-temp)**2)/len(returns))**0.5
    return half_dev

RJ_half_dev = cal_half_dev(simpleret)

# print(RJ_half_dev)

# VAR
# 历史模拟法分位函数
rj_var = simpleret.quantile(0.05)
# print(rj_var)

# 协方差矩阵法
rj_var_cov = norm.ppf(0.05,simpleret.mean(),simpleret.std())
# print(rj_var_cov)

# ES
rj_es = simpleret[simpleret<=simpleret.quantile(0.05)].mean()
# print(rj_es)

# 持仓期间收益率最大回撤
# 在时间窗口内，从峰值到低谷的幅度，表示在持有资产期间面临的最大亏损
# print(simpleret)
# 持仓期间累积的持仓收益
value = (1+simpleret).cumprod()
print(value)
# 前几个数中最大的数即最大收益-持仓期间的总的累计收益
D = value.cummax() - value
print(D)
#相应的回撤率，回落值/最大值
d = D/value.cummax()
print(d)
# 最大的回撤值
MDD = D.max()
print(MDD)
# 最大的回撤率
mdd = d.max()
print(mdd)