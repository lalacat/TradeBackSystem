from datetime import datetime

import pandas as pd

from base_database.initialize import database_manager
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
"""
股票之间的相关性
写入到csv文件
"""
s = Settings()
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 18)

RJ = database_manager.load_bar_data(
        '002192',Exchange.SZ , Interval.DAILY, start, end
    )
TQ = database_manager.load_bar_data(
        '002466',Exchange.SZ , Interval.DAILY, start, end
    )
GF = database_manager.load_bar_data(
        '002460',Exchange.SZ , Interval.DAILY, start, end
    )

RJ_close = pd.DataFrame([{bar.datetime : bar.close_price for bar in RJ}])
RJ_close = RJ_close.T
RJ_close.rename(columns={0:'close'},inplace=True)#注意这里0和1都不是字符串

TQ_close = pd.DataFrame([{bar.datetime : bar.close_price for bar in TQ}])
TQ_close = TQ_close.T
TQ_close.rename(columns={0:'close'},inplace=True)

GF_close = pd.DataFrame([{bar.datetime : bar.close_price for bar in GF}])
GF_close = GF_close.T
GF_close.rename(columns={0:'close'},inplace=True)


# 合并数据
df = pd.concat([RJ_close.close,TQ_close.close,GF_close.close], axis = 1,keys=['RJ_close','TQ_close','GF_close'])
# 保存数据
# df.to_csv('RJ_TQ.csv')
# 填充缺失数据
df.ffill(axis=0, inplace=True)
# 两两相关系数
corr = df.corr(method = 'pearson', min_periods = 1)
# print(corr)

# 指定两个相关系数
# result = df['RJ_close'].corr(df['TQ_close'])


# returns = df.pct_change()
# print(returns)

# matplot画图
# df.plot(figsize = (10,6))
# plt.savefig('qjd_gm.jpg')
# plt.show()



# 根据index获得数据
dt = datetime(2019, 9, 2).strftime("%Y-%m-%d")
data= df.loc[dt] #<class 'pandas.core.series.Series'>
d = data['RJ_close']
print(d)
# for d in data:
#     print(d)

# pyqtgraph画图
# plot = pg.plot(title='相关系数')
# plot.plot(df['RJ_close'],)
# plot.plot(df['TQ_close'], pen='r')
# plot.plot(df['GF_close'], pen='b')
# pg.QtGui.QGuiApplication.exec_()
