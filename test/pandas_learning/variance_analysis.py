from datetime import datetime

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

"""
半方差计算
"""

def cal_MSD(returns):
    mu = returns.mean()
    temp = returns[returns<mu]
    MSD = ((sum(mu-temp)**2)/len(returns))**0.5
    return MSD

s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
RJ_returns = RJ.close_price.pct_change().dropna()
RJ['return'] = RJ_returns

MSD_RJ = cal_MSD(RJ_returns)
print(MSD_RJ)


