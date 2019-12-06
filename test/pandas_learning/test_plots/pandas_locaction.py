from datetime import datetime

import pandas as pd

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

print(RJ)
RJ_describe = RJ.describe()
# print(RJ_describe)


