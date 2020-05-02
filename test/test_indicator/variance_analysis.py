from datetime import datetime

import matplotlib.pyplot as plt
import numpy
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats import anova
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
方差分析的实现
最小二乘法的实现
FLAG对收盘价的影响
"""
s = Settings()

dbm = init('_',s)
start = datetime(2019, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
# 分组
RJ['FLAG']=0
# 链式索引会报错
# RJ['FLAG'][RJ['close_price']>=RJ['open_price']]='positive'
# RJ['FLAG'][RJ['close_price']<RJ['open_price']]='negotive'
RJ.loc[RJ['close_price']>=RJ['open_price'],['FLAG']]= 'positive'
RJ.loc[RJ['close_price']<RJ['open_price'],['FLAG']] = 'negotive'
RJ['return'] = RJ['close_price'].pct_change()
print(RJ)
# 建立FLAG与收益率的关系
model = ols('close_price ~ C(FLAG)',data=RJ.dropna()).fit()
table = anova.anova_lm(model)
print(table)