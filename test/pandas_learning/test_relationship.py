from datetime import datetime

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import pandas as pd
s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
FX = dbm.load_bar_dataframe_data(
        '600196',Exchange.SH , Interval.DAILY, start, end
    )
RJ_returns = RJ.close_price.pct_change().dropna()
FX_returns = FX.close_price.pct_change().dropna()

plt.scatter(RJ_returns,FX_returns)
plt.show()