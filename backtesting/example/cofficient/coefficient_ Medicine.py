from datetime import datetime

import pandas as pd
import pyqtgraph as pg

from base_database.initialize import database_manager
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

s = Settings()
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)

HR = database_manager.load_bar_dataframe_data(
        '600276',Exchange.SH , Interval.DAILY, start, end
    )
FX = database_manager.load_bar_dataframe_data(
        '600196',Exchange.SH , Interval.DAILY, start, end
    )
# 合并数据
df = pd.concat([HR.close_price,FX.close_price], axis = 1,keys=['HR_close','FX_close'])
# 保存数据
# df.to_csv('RJ_TQ.csv')
# 填充缺失数据
df.ffill(axis=0, inplace=True)
# 两两相关系数
corr = df.corr(method = 'pearson', min_periods = 1)
print(corr)

# pyqtgraph画图
plot = pg.plot(title='相关系数')
plot.plot(df['FX_close'],)
plot.plot(df['HR_close'], pen='r')
# plot.plot(df['GF_close'], pen='b')
# plot.plot(df['SD_close'], pen='w')
pg.QtGui.QGuiApplication.exec_()


# 指定两个相关系数
# result = df['RJ_close'].corr(df['TQ_close'])


# returns = df.pct_change()
# print(returns)

# matplot画图
# df.plot(figsize = (10,6))
# plt.savefig('qjd_gm.jpg')
# plt.show()



# 根据index获得数据
# dt = datetime(2019, 9, 2).strftime("%Y-%m-%d")
# data= df.loc[dt] #<class 'pandas.core.series.Series'>
# d = data['RJ_close']
# for d in data:
#     print(d)


