import pandas as pd
from datetime import datetime

from backtesting.example.stocks_collection import stocks_TMT
from base_database.initialize import database_manager
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import pyqtgraph as pg

s = Settings()
start = datetime(2019, 1, 1)
end = datetime(2019, 12, 9)
results = dict()
key = []
for name, codes in stocks_TMT.items():
    code,exchange = codes[0].split('.')
    result = database_manager.load_bar_dataframe_data(code,Exchange(exchange),Interval.DAILY,start, end)
    results[name] = result['close_price']

df = pd.DataFrame(results)
# print(df)
corr = df.corr(method = 'pearson', min_periods = 1)
print(corr)