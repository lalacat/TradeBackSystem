from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


def annualize(returns,period):
    if period == 1:
        return((1+returns).cumprod()[-1]**(252/len(returns))-1)
    if period == 30:
        return((1+returns).cumprod()[-1]**(12/len(returns))-1)
    if period == 90:
        return ((1 + returns).cumprod()[-1] ** (4 / len(returns)) - 1)
    if period == 180:
        return ((1 + returns).cumprod()[-1] ** (2 / len(returns)) - 1)
    if period == 360:
        return ((1 + returns).cumprod()[-1] ** (1 / len(returns)) - 1)


s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2019, 11, 22)

code_list = [
    '002192.SZ',  # 融捷
    '002466.SZ',  # 天齐
    '002460.SZ',  # 赣锋锂业

    '600276.SH',  # 恒瑞
    '600196.SH',  # 复星
    '300760.SZ',  # 迈瑞
    # '000001.SH', #上证
    # '399001.SZ' #深证
]

for code in code_list:
    code,exchange = code.split('.')
    datas = dbm.load_bar_dataframe_data(
        code, Exchange(exchange), Interval.DAILY, start, end
    )
    returns = datas.close_price.pct_change().dropna()
    print('%s: %f'%(code,annualize(returns,1)))