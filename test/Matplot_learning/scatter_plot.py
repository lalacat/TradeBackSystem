from datetime import datetime

import matplotlib.pyplot as plt
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

s = Settings()

dbm = init('_', s)
start = datetime(2015,1, 1)
end = datetime(2020, 3, 31)
RJ = dbm.load_bar_dataframe_data(
    '002192', Exchange.SZ, Interval.DAILY, start, end
)
# 直方图
all_info = RJ['close_price'].describe()
print(all_info)
# plt.bar(RJRJ['close_price'],)
# 直方图
plt.hist([RJ['close_price'],RJ['open_price']],bins=10,histtype='stepfilled')
# 散点图
# plt.scatter(RJ['close_price'],RJ['open_price'],marker='o')
plt.show()