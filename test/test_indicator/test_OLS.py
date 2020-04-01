import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize		# 最小二乘法拟合
import matplotlib.pyplot as plt 	# python matplotlib 绘图
import pandas as pd;

# Z=(S + s*n*100)/(n*100+N)
S = 22.143
N = 8000

p_start = 1840
delat_p = 10
p_end = 1870
# p = range(p_start,p_end,delat_p)
# p = pd.DataFrame(np.array(range(p_start,p_end,delat_p)))/100

p0 = np.arange(p_start,p_end,delat_p)/100
p = p0.reshape(1,3)
print(p)

n0 =np.arange(1,5)*100
# delat_n = 100
n = n0.reshape(1,4).T
toltal_volums = n + N
# print(toltal_volums)
z = np.dot(n,p)+S*N
# print(len(z))


len_volunm = len(toltal_volums)
len_price = len(p)
result = list()
for i in range(4):
    print(list(n0))
    temp = pd.DataFrame(z[i]/toltal_volums[i],columns=[toltal_volums[i]],index=[p0])
    result.append(temp)


r = pd.concat(result,axis=1)
r.plot()
plt.show()