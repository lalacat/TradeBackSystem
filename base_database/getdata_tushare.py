from enum import Enum
from time import time

import tushare as ts
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from base_utils.object import BarData
from settings.setting import Settings

token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'

# ts_code = '002192.SZ'
# startday = '20190326'
# endday= '20190330'
pro = ts.pro_api(token)
# df = pro.daily(ts_code=ts_code, start_date=startday, end_date=endday)
# print(df)
# # result = df.sort_values(by='trade_date', ascending=True,inplace=True)
# df.sort_values(by='trade_date', ascending=True,inplace=True)
# # print(df['trade_date'])
# print(df.iloc[0,1])

# print(result['trade_date'][0],result['trade_date'][1])
# print(df['trade_date'][0],df['trade_date'][1])





def str2datatime(time:str):
    return dt.datetime.strptime(time, '%Y%m%d')


def generate_bar_from_row(row, symbol, exchange):
    """"""
    bar = BarData(
        symbol=symbol,
        exchange=Exchange(exchange),
        interval=Interval.DAILY,
        open_price=row["open"],
        high_price=row["high"],
        low_price=row["low"],
        close_price=row["close"],
        volume=row["vol"],
        datetime=str2datatime(row['trade_date']),
        gateway_name="DB"
    )
    return bar


def download_minute_bar(vt_symbol,database_manager=None):
    """下载某一合约的分钟线数据"""
    print(f"开始下载合约数据{vt_symbol}")
    symbol, exchange = vt_symbol.split(".")

    start = time()

    df = pro.daily(
        ts_code=vt_symbol,
        start_date='20150101',
        end_date='20190531')

    df.sort_values(by='trade_date',ascending=True,inplace=True)

    bars = []
    for ix, row in df.iterrows():
        bar = generate_bar_from_row(row, symbol, exchange)
        bars.append(bar)
    # return bars
    database_manager.save_bar_data(bars)

    end = time()
    cost = (end - start) * 1000


    print(
        "合约%s的分钟K线数据下载完成%s - %s，耗时%s毫秒"
        % (symbol, df['trade_date'][len(df)-1], df['trade_date'][0], cost)
    )

if __name__ == "__main__":
    s = Settings()
    database_manager = init('a',s)

    download_minute_bar('002192.SZ',database_manager)


# def to_update_param(d):
#     return {
#         "set__" + k: v.value if isinstance(v, Enum) else v
#         for k, v in d.__dict__.items()
#     }
# bars = download_minute_bar('002192.SZ')
# for i in range(10):
#     d = bars[i]
#     updates = to_update_param(d)
#     updates.pop("set__gateway_name")
#     updates.pop("set__vt_symbol")
#     (
#         print(updates)
#     )