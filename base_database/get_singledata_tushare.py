import datetime as dt

import tushare as ts

from base_utils.constant import Exchange, Interval
from base_utils.object import BarData

token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'


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

ts_code = '002192.SZ'
startday = '20190603'
pro = ts.pro_api(token)
# df = pro.daily(ts_code=ts_code, start_date='20180701', end_date='20180718')

# df = pro.index_dailybasic()
df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date='20180101', end_date='20181011')

print(df)

# symbol, exchange = ts_code.split(".")
# # print(df)
# for _,row in df.iterrows():
#     bar = generate_bar_from_row(row,symbol,exchange)
# s = Settings()
# database_manager = init('a',s)
#
# # db_bar = DbBarData.from_bar(bar)
# # print(db_bar)
# # db_bar.save()
# DbBarData.objects(
#     # symbol=bar.symbol, interval=bar.interval.value, datetime=bar.datetime
# ).update_one(upsert=True,set__symbol=bar.symbol,set__interval=bar.interval.value,set__datetime=bar.datetime)
