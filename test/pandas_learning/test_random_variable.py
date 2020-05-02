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


# print(returns.head(5))
#
# returns_01 = (RJ.close_price-RJ.close_price.shift(1))/RJ.close_price.shift(1)
# print(returns_01.head(5))


# density = stats.kde.gaussian_kde(returns)
#
# # plt.rcParams['font.sans-serif'] = ['SimHei']
#
# bins = np.arange(-5,5,0.02)
# # print(density(bins))
#
# plt.subplot(211)
# plt.plot(bins,density(bins))
# plt.title('概率密度函数')
#
# plt.subplot(212)
# plt.plot(bins,density(bins).cumsum())
# plt.title('累加分布函数')
#


# plt.show()

