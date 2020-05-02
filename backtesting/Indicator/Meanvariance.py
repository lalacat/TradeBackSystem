import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix,solvers,blas

"""
利用二次规划方法求解权重
两种实现
1.numpy
2.cvxopt

"""
solvers.options['show_progress'] = False

class MeanVariance(object):
    def __init__(self,returns,return_mean=None,return_cov=None):
        self.returns = returns
        if len(return_mean) != 0:
            # # 回报率均值矩阵
            self._means = np.array(returns.mean())
        else:
            self._means = return_mean

        if len(return_cov) != 0:
            # 协方差矩阵
            self._covs = np.array(returns.cov())
        else:
            self._covs = return_cov

        # 权重的个数
        self._num = len(self._means)

    def minVar(self,goalRet):
        # 目的是求解
        # [cov     1  return] [w] = [0]
        # [1       0   0   ] [x]  = [1]
        # [return  0   0   ] [y]  = [Rp]

        # 构建矩阵
        # [cov 1 return]
        # L1 = np.append(np.append(self._covs, [np.ones(self._num)], 0), [self._means], 0).swapaxes(0, 1)
        L1 = np.append(np.append(self._covs.swapaxes(0,1),[self._means], 0),[np.ones(self._num)] , 0).swapaxes(0, 1)


        # 构建
        # [1 0 0 ]
        L2 = list(np.ones(self._num))
        L2.extend([0, 0])

        # [return 0 0 ]
        L3 = list(self._means)
        L3.extend([0, 0])

        # 构建
        # [1 0 0]
        # [return 0 0 ]
        L4 = np.array([L2, L3])

        # 组合成大矩阵
        # [cov     1  return]
        # [1       0   0   ]
        # [return  0   0   ]
        L = np.append(L1, L4, 0)

        # 结果矩阵
        # [0]
        # [1]
        # [Rp]
        b = np.append(np.zeros(self._num), [1, goalRet], 0)

        results = np.linalg.solve(L, b)
        weights = np.array(results[:-2],dtype=np.float)
        # weight.dtype = np.float
        # print(type(weight[0]))
        # print(self._means.dot(weight.T))
        # 返回的结果与最优化中没有卖空限制的结果一样
        return weights

    def calVar(self,weight):
        # weight = weight[1][0]
        # print(weight)
        result = np.dot(np.dot(weight, self._covs), weight)
        # print(result)
        return result

    def frontierCurve(self):
        # 画有效前沿曲线
        # 目标收益的范围[-0.0002,0.08]
        goals = [x/500000 for x in range(-100,4000)]
        variances = list(map(lambda x: self.calVar(self.minVar(x)[1,:].astype(np.float)),goals))
        # variances = list(map(lambda x: self.calVar(self.quadraticVar(x)),goals))
        # print(np.array(variances).min())
        # print(np.array(variances).max())

        plt.plot(variances,goals)

    def quadraticVar(self,goal):
        '''
         minimize    (1/2)*x'*P*x + q'*x
            subject to  G*x <= h
                        A*x = b.
        '''
        #  matrix的行列与np的行列构造不同 n x n
        P= 2*matrix(np.array(self._covs))
        # P_01 = matrix(np.dot(2,self._covs))
        # print(P)
        # print(P_01)
        # n x 1
        Q = matrix(list(np.zeros(self._num)))
        # Q_01 = matrix(np.zeros((self._num,1)))
        # print(Q)
        # print(Q_01)

        # 创建对角线矩阵，所有的权重都大于0,确定权重的边界 m x n
        G = -matrix(np.eye(self._num))
        # G_02 = -matrix(np.identity(self._num))
        # G_01 = -matrix(np.zeros((self._num,self._num)))
        # print(G)
        # print(G_02)


        # m x 1
        # h = matrix(np.ones(self._num))
        h = matrix(0.0, (self._num, 1))
        # h_01 = matrix(np.zeros((self._num,1)))
        # print(h)
        # print(h_01)

        # 构建 p x n
        # 权重之和为1
        # 权重和资产相乘为期望收益
        L = list(np.ones(self._num))
        L5 = np.array([L, self._means]).transpose(0, 1)
        A = matrix(L5)
        # A_01 = matrix(np.append([np.ones(self._num)],[self._means],axis=0))
        # print(A)
        # print(A_01)


        # p x 1
        b = matrix([1, goal])
        # b_01 = matrix(np.array([[1,goal]]).swapaxes(0,1))
        # print(b)
        # print(b_01)
        results = solvers.qp(P,Q,G,h,A,b,options={'show_progress':False})
        # sol = solvers.qp(P_01, Q_01, G_01 , h_01, A_01, b_01,options={'show_progress':False})

        weights = np.array(list(results['x']),dtype=np.float32)
        # print(type(weight[0]))
        # print(self._means.dot(results['x']))
        # print(sol['x'])
        # print(self._means.dot(sol['x']))

        # return np.array([list(self.returns.columns),weight])
        return weights

    def optimal_portfolio(self,returns):
        n = len(returns)
        returns = np.asmatrix(returns)

        N = 100
        mus = [10 ** (5.0 * t / N - 1.0) for t in range(N)]  # 注意！这个mu不是我们要求的最小预期收益率mu！后面我会附上一些材料来解释。

        # Convert to cvxopt matrices
        S = matrix(np.cov(returns))
        pbar = matrix(np.mean(returns, axis=1))  #
        # print(pbar)

        # Create constraint matrices
        G = -matrix(np.eye(n))  # negative n x n identity matrix
        print(G)
        h = matrix(0.0, (n, 1))
        print(h)
        A = matrix(1.0, (1, n))
        # print(A)
        b = matrix(1.0)
        # print(b)

        # Calculate efficient frontier weights using quadratic programming
        portfolios = [solvers.qp(mu * S, -pbar, G, h, A, b)['x']
                      for mu in mus]  # 这个最优化的做法和我们的直觉有点不一样（后面我也会说）
        # print(len(portfolios))
        ## CALCULATE RISKS AND RETURNS FOR FRONTIER
        returns = [blas.dot(pbar, x) for x in portfolios]

        risks = [np.sqrt(blas.dot(x, S * x)) for x in portfolios]
        ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
        m1 = np.polyfit(returns, risks, 2)
        x1 = np.sqrt(m1[2] / m1[0])
        # CALCULATE THE OPTIMAL PORTFOLIO
        wt = solvers.qp(matrix(x1 * S), -pbar, G, h, A, b)['x']
        print(wt)
        return np.asarray(wt), returns, risks


    def meanRet(self,weight):
        # meanRisky = self.returns.pct_change().dropna()
        return (np.sum(np.multiply(self._means,np.array(weight))))

    def varianceRet(self,weight):
        return (np.dot(np.dot(weight, self._covs),weight.T))