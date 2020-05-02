from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from settings.setting import Settings

s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 11, 18)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
# print(RJ['close_price'].describe())
# plt.hist(RJ['close_price'],bins=20) # 直方图

prcData= RJ.iloc[:,:4]
data = np.array(prcData)
plt.boxplot(data,labels=('open','close','high','low')) # 数据是向量的形式

plt.show()



