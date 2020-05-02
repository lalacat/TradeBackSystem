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
    '002192', Exchange.SZ, Interval.DAILY, start, end)

figure = plt.Figure()
ax = figure.add_axes()
ax1 = plt.subplot(221)
print(type(ax1))