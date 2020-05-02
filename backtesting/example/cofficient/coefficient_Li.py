from datetime import datetime

import pandas as pd
import pyqtgraph as pg

from base_database.initialize import database_manager
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

s = Settings()
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)

RJ = database_manager.load_bar_dataframe_data(
        '002192',Exchange.SZ , Interval.DAILY, start, end
    )
TQ = database_manager.load_bar_dataframe_data(
        '002466',Exchange.SZ , Interval.DAILY, start, end
    )
GF = database_manager.load_bar_dataframe_data(
        '002460',Exchange.SZ , Interval.DAILY, start, end
    )

SD = database_manager.load_bar_dataframe_data(
        '603026',Exchange.SH , Interval.DAILY, start, end
    )

FX = database_manager.load_bar_dataframe_data(
        '600196',Exchange.SH , Interval.DAILY, start, end
    )

# 合并数据
df = pd.concat([RJ.close_price,TQ.close_price,GF.close_price,SD.close_price], axis = 1,keys=['RJ_close','TQ_close','GF_close','SD_close'])
# 保存数据
# df.to_csv('RJ_TQ.csv')
# 填充缺失数据
df.ffill(axis=0, inplace=True)
# 两两相关系数
corr = df.corr(method = 'pearson', min_periods = 1)
print(corr)

# pyqtgraph画图
plot = pg.plot(title='相关系数')
plot.plot(df['RJ_close'],)
plot.plot(df['TQ_close'], pen='r')
plot.plot(df['GF_close'], pen='b')
plot.plot(df['SD_close'], pen='w')
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


