from datetime import datetime

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import numpy as np
import pandas as pd

"""
计算收益率
"""
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


def fillInfNaN(returns,method='ffill'):
    # returns = returns.fillna(method='bfill').round(4)
    returns = returns.dropna().round(4)
    returns = returns.replace([np.inf,-np.inf],np.NaN).fillna(method=method)
    return returns

def getReturn(stocks,startday,endday,peried=1):
    s = Settings()
    dbm = init('_',s)
    if isinstance(startday,datetime):
        start_day = startday
    else:
        start_day = datetime.strptime(startday, '%Y%m%d').date()
    if isinstance(endday,datetime):
        end_day = endday
    else:
        end_day = datetime.strptime(endday, '%Y%m%d').date()

    results = pd.DataFrame()
    for code in stocks:
        code, exchange = code.split('.')
        datas = dbm.load_bar_dataframe_data(
            code, Exchange(exchange), Interval.DAILY, start_day, end_day
        )
        close = datas['close_price']
        lagclose = close.shift(peried)
        results[code] = (close-lagclose)/lagclose
        # returns = datas.close_price.pct_change().dropna()
        # print('%s: %f' % (code, annualize(returns, 1)))

    return fillInfNaN(results)

# code_list = [
#     '002192.SZ',  # 融捷
#     '300618.SZ',  # 寒锐
#     '300433.SZ',  # 蓝思
#     '002299.SZ',  # 圣农
#     '300251.SZ',  # 光线
#
#     # '600276.SH',  # 恒瑞
#     # '600196.SH',  # 复星
#     # '300760.SZ',  # 迈瑞
#     # '000001.SH', #上证
#     # '399001.SZ' #深证
# ]
# test = getReturn(code_list,'20200101','20200413')
# print(test)

