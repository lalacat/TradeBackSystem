import numpy as np
import pandas as pd

from backtesting.Indicator.Meanvariance import MeanVariance
from backtesting.example.measure.annualize_return import getReturn
"""
expand_dims的应用
预估收益率和协方差矩阵
"""

def black_litterman(returns,tau,P,Q):
    # 先验收益率
    expect_returns = returns.mean()
    # 协方差矩阵
    cov_returns = returns.cov()

    # 代表假设分布的方差
    t_cov = tau * cov_returns
    # 构建观点的方差矩阵，只有对角线上的数，才代表观点的方差
    w = np.dot(np.dot(P,t_cov),P.T)
    # 构建观点的对角线矩阵，对角线上表示的时候每个观点的方差，代表观点的精度
    # [p1.T*cov*p1       0    ]
    # [     0      p2.T*cov*p2]
    Omega = w*np.eye(Q.shape[0])
    # 求逆矩阵
    t_cov_inv = np.linalg.inv(t_cov)
    Omega_inv = np.linalg.inv(Omega)

    """
    # 方法一：
    # 方法一和二的结果是一样的    
    middle = np.linalg.inv(w+Omega)
    er = np.expand_dims(expect_returns,axis=0).T + np.dot(np.dot(np.dot(t_cov,P.T),middle),
                             (Q-np.expand_dims(np.dot(P,expect_returns.T),axis=1)))
    pSigma = cov_returns+t_cov -np.dot(t_cov.dot(P.T).dot(middle).dot(P),t_cov)
    """

    '''
    计算出每一个资产的后验收益率
    简单就是（先验+新息）的加权平均
    权重就是先验协方差矩阵和新息的协方差矩阵之和
    '''
    posteriorWeight = np.linalg.inv(t_cov_inv+np.dot(np.dot(P.T,Omega_inv),P))
    posteriorReturn =np.dot(posteriorWeight,np.expand_dims(np.dot(t_cov_inv,expect_returns.T),axis=1)+np.dot(np.dot(P.T,Omega_inv),Q))
    posteriorCov = cov_returns + posteriorWeight
    # print(posteriorReturn)
    # print(pd.DataFrame(cov_returns+posteriorSigma))

    return [posteriorReturn,posteriorCov]


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
returns = getReturn(code_list,'20190101','20200413')
mean = returns.mean()
pick1 = np.array([1,0,1,1,1])
q1 = np.array([0.003*4])
pick2 = np.array([0.5,0.5,0,0,-1])
q2 = np.array([0.001])
P = np.array([pick1,pick2])
Q = np.array([q1,q2])

# print(np.dot(P,mean.T))
# print(Q)

res = black_litterman(returns,0.1,P,Q)

p_mean = pd.DataFrame(res[0],index= returns.columns,columns=['posterior_mean'])
print(mean)
print(p_mean)

p_cov = res[1]*252
mv  = MeanVariance(returns,res[0]*252,p_cov)
qv = mv.quadraticVar(0.003*252)
m = mv.minVar(0.003*252)
print(qv.sum())
print(qv)
print(mv.meanRet(qv))
print(np.sqrt(mv.varianceRet(qv)))
print(m.sum())
print(m)
print(mv.meanRet(m))
print(np.sqrt(mv.varianceRet(m)))


'''
mean = returns.mean()
print(mean)
print(mean.shape)
new = np.expand_dims(mean,axis=0)
print(new)
print(new.shape)

a = np.expand_dims(np.dot(P,mean.T),axis=1)
# print(P.shape)
# print(mean.T.shape)
print(a.shape)
print(a)
print(a+Q)
'''

#
# a = np.array([[1,2],[2,3]])
# b = np.array([[3,4],[5,6]])
# print(np.dot(a,b))
# print(a.dot(b))