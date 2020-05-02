import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from backtesting.Indicator.Meanvariance import MeanVariance
from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

code_list = [
    '002192.SZ',  # 融捷
    '300618.SZ',  # 寒锐
    '300433.SZ',  # 蓝思
    '002299.SZ',  # 圣农
    '300251.SZ',  # 光线

    # '600276.SH',  # 恒瑞
    # '600196.SH',  # 复星
    # '300760.SZ',  # 迈瑞
    # '000001.SH', #上证
    # '399001.SZ' #深证
]
returns = getReturn(code_list,'20190101','20190413')
# print(returns)
#
# riskmean = returns.pct_change().replace([np.inf,-np.inf],np.NaN).fillna(method='ffill')
# print(riskmean.head(30))
# print(riskmean.mean())
# print(np.sum(np.multiply(riskmean,np.array([0.1,0.2,0.3,0.2,0.2]))))


# 相关性系数
# coff = returns.corr()
# print(coff)
# 协方差矩阵
# print(returns.cov())
# 收益率回报
# returns.plot()
# 累积回报率
# cumreturn = (1+returns).cumprod()
# cumreturn.plot()
# plt.title('daily return of 4 stocks')
def statistics(weights):

    weights = np.array(weights)

    port_returns = np.sum(returns.mean()*weights)*252

    port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*252,weights)))

    return np.array([port_returns, port_variance, port_returns/port_variance])
stds =returns.std()
means = returns.mean()

mv = MeanVariance(returns)
qv = mv.quadraticVar(0.003)
m = mv.minVar(0.003)
print(qv)
print(m)

# print(type(qv[1][0]))
# print(type(m[1][0]))


variance_qv = np.dot(np.dot(qv,returns.cov()),qv.T)
variance_m = np.dot(np.dot(m.astype(np.float),returns.cov()),m.astype(np.float).T)

# print(qv)
print(qv.sum())
print(m.sum())
print(means.dot(qv))
print(means.dot(m))

print(np.sqrt(variance_qv))
print(np.sqrt(variance_m))
'''
# optweights, optreturns, optrisks = mv.optimal_portfolio(returns)
# plt.plot(stds, means, 'o')
# plt.ylabel('mean')
# plt.xlabel('std')
# plt.plot(optrisks, optreturns, 'y-o')
# plt.plot(statistics(optweights['x'].reshape(4, 1))[1], statistics(optweights['x'].reshape(4, 1))[0], 'r^')
#
# plt.show()

# returns = getReturn(code_list,'20180101','20191231')
#
# test_return = np.dot(returns,np.array([weights[1,:].astype(np.float)]).swapaxes(0,1))
# test_return = pd.DataFrame(test_return,index=returns.index)
# test_cum_return = (1 + test_return).cumprod()
#
# # 随机生成的权重
# sim_weight = np.random.uniform(0,1,(100,5))
# print(pd.DataFrame(sim_weight))
# sim_weight = np.apply_along_axis(lambda x: x/sum(x),1,sim_weight)
# # print(pd.DataFrame(sim_return))
# print(returns.shape)
# print(sim_weight.shape)
# sim_return = np.dot(returns,sim_weight.T)
# # print(pd.DataFrame(sim_return))
# sim_return = pd.DataFrame(sim_return,index=returns.index).dropna()
# sim_cum_return = (1+sim_return).cumprod()
# plt.plot(sim_cum_return.index,sim_return,color='green')
# plt.plot(test_return.index,test_cum_return)
#
#
#
'''
