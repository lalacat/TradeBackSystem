from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
股票的日收益计算
包含日收益图
"""

s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
returns=RJ.close_price.pct_change().dropna()
returns.plot(figsize=(14,6),label=u'日收益率')
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.title(u'融捷股份日收益图',fontsize=15)
my_ticks = pd.date_range('2018-9-1','2019-9-30',freq='q')

plt.xticks(my_ticks,fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('',fontsize=12)
# 将右边、上边的两条边颜色设置为空 其实就相当于抹掉这两条边
plt.axhline(returns.mean(), color='r',label=u'日收益均值')
plt.axhline(returns.mean()+1.5*returns.std(), color='g',label=u'正负1.5倍标准差')
plt.axhline(returns.mean()-1.5*returns.std(), color='g')
plt.legend()
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.show()