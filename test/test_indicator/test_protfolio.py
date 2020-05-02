import math
import numpy as np
import matplotlib.pyplot as plt

"""
计算两个资产不同权重，不同相关系数对组合资产的影响
"""
# 计算两个资产组合均值
# 资产A 期望8%，标准差12%
# 资产B 期望15%，标准差25%
def cal_mean(weight):
    return 0.08*weight+0.15*(1-weight)
# 生成50个权重的组合收益率
mean = list(map(cal_mean,[weight/50 for weight in range(51)]))

print(mean)
std_mat = np.array(
    [
    list(map(lambda w: math.sqrt((w*0.12)**2+((1-w)*0.25)**2+2*w*(1-w)*0.12*0.25*(0.5*i-1.5)),
            [w/50 for w in range(51)]))
        for i in range(1,6)]
                   )
print(std_mat[0,:])

# plt.plot(std_mat[0,:],mean,label='-1')
# plt.plot(std_mat[1,:],mean,label='-0.5')
# plt.plot(std_mat[2,:],mean,label='0')
# plt.plot(std_mat[3,:],mean,label='0.5')
# plt.plot(std_mat[4,:],mean,label='1')
# plt.show()