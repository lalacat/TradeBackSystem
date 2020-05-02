from datetime import datetime
from arch import arch_model
from backtesting.example.measure.annualize_return import getReturn

"""
求波动率的长期均值
"""


start = datetime(2019, 1, 1)
end = datetime(2020, 4, 24)


GX_return = getReturn(['300251.SZ'],start,end)

# 设定模型，默认GARCH(1,1)
am = arch_model(GX_return)

# 估计参数,只输出结果，不输出过程
model = am.fit(update_freq=0)

print(model.summary())
'''
                                  Mean Model                                 
=============================================================================
                 coef    std err          t      P>|t|       95.0% Conf. Int.
-----------------------------------------------------------------------------
mu         1.0738e-03  1.515e-03      0.709      0.478 [-1.896e-03,4.043e-03]
                              Volatility Model                              
============================================================================
                 coef    std err          t      P>|t|      95.0% Conf. Int.
----------------------------------------------------------------------------
omega      2.1999e-04  3.960e-05      5.556  2.764e-08 [1.424e-04,2.976e-04]
alpha[1]       0.0268  4.301e-02      0.624      0.533  [-5.746e-02,  0.111]
beta[1]        0.6648  6.077e-02     10.939  7.472e-28     [  0.546,  0.784]
============================================================================
alpha的p-value>0.05接受原假设，alpha = 0
omega = Vl * r
r + alpha + beta =1
vl = omega/(1-0.6648）

'''