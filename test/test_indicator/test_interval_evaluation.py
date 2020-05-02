from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
测试t检验
包括VAR的计算
"""
s = Settings()
dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 3, 31)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
LS = dbm.load_bar_dataframe_data(
'300433',Exchange.SZ , Interval.DAILY, start, end
)

return_ls = LS['close_price'].pct_change().dropna()
return_rj = RJ['close_price'].pct_change().dropna()
print(return_ls.sum())
mean_ls = return_ls.mean()
mean_rj = return_rj.mean()
print(mean_ls)
print(mean_rj)
std_ls = return_ls.std()
print(std_ls)
sterror_ls = stats.sem(return_ls)
print(sterror_ls)


# 95%的置信水平下回报率的估计
# 估计的是收益的均值
t = stats.t.interval(0.95,len(return_ls)-1,mean_ls,sterror_ls)
print(t)

# 95%的置信水平下的VAR值
# print(stats.norm.ppf(0.05,mean_ls,std_ls))

# plt.plot(np.arange(-0.0008,0.0008,0.00002),stats.norm.pdf(np.arange(-0.0008,0.0008,0.00002),mean_ls,std_ls))
# plt.plot(np.arange(-0.1,0.1,0.002),stats.norm.pdf(np.arange(-0.1,0.1,0.002),mean_ls,std_ls))
# plt.hist(return_ls,bins=10)
# plt.show()


# 单个变量的t检验
# 检测收益是否符合给定值
t_static_01 = stats.ttest_1samp(return_ls,0)
print(t_static_01)


#检测两个独立样本的均值是否相等

t_static_02 = stats.ttest_ind(return_ls,return_rj)
print(t_static_02)

# 检测两个不独立的样本
t_static_03 = stats.ttest_rel(return_ls,return_rj)
print(t_static_03)
