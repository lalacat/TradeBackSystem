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
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.plot(RJ['close_price'],label='收盘价',linestyle='dashdot')
plt.plot(RJ['open_price'],marker='o',label='开盘价')
plt.title('融捷股份收盘价曲线')
plt.xticks(rotation=45)
plt.xlabel('日期')
plt.ylabel('收盘价')
plt.grid(True,axis='y')
plt.legend(loc=0)

plt.show()