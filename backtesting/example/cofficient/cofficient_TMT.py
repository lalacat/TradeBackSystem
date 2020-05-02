from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from base_database.initialize import database_manager
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
"""
多对象的相关系数计算
"""
s = Settings()
start = datetime(2018, 1, 1)
end = datetime(2020, 3, 31)
results = dict()
stocks_TMT = { '蓝思':'300433.SZ',
        '立讯':'002475.SZ', #
        '歌尔':'002241.SZ' #
       }
for name, codes in stocks_TMT.items():
    code,exchange = codes.split('.')
    result = database_manager.load_bar_dataframe_data(code,Exchange(exchange),Interval.DAILY,start, end)
    results[name] = result['close_price']

df = pd.DataFrame(results)
plt.scatter(df['歌尔'],df['蓝思'])
plt.legend()
plt.show()
corr = df.corr(method = 'pearson', min_periods = 1)
print(corr)