from datetime import datetime

import matplotlib.pyplot as plt

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


# fig = plt.figure()
# ax1 = fig.add_axes([0.1,0.1,0.3,0.3])
# ax2 = fig.add_axes([0.5,0.5,0.3,0.3])
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xticks(rotation=45)
ax1 = plt.subplot(211)
ax1.plot(RJ['close_price'],color='k')
ax1.set_ylabel('收盘价')
ax1.set_title('融捷股份收盘价')
# ax1.xticks(rotation=45)

ax2 = plt.subplot(212)

left1 = RJ['volume'].index[RJ['close_price']>RJ['open_price']]
high1 = RJ['volume'][left1]

left2 = RJ['volume'].index[RJ['close_price']<= RJ['open_price']]
high2 = RJ['volume'][left2]

ax2.bar(left1,high1,color='r')
ax2.bar(left2,high2,color='g')
# ax2.xticks(rotation=45)

plt.show()




plt.show()






