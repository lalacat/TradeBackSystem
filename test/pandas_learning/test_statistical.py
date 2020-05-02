from datetime import datetime

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
returns=RJ.close_price.pct_change().dropna()

# plt.hist(returns)
# plt.show()

rj_mode = returns.mode()
print('众数 %f' %returns.mode())
print('绝对偏差 %f' %returns.mad())
print('方差 %f' %returns.var())
print('标准差 %f' %returns.std())
