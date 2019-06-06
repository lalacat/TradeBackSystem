import pprint
from datetime import datetime

from base_database.database_mongo import init, MongoManager, DbBarData
from base_utils.constant import Interval, Exchange
from settings.setting import Settings


s = Settings()
init('a',s)
symbol = '002192'
data = MongoManager()
exchange = Exchange('SZ')
day = Interval.DAILY
# 最新价
# newest_bar = data.get_newest_bar_data('002192',Exchange.SZ,Interval.DAILY)
# print(newest_bar)
# 指定日期价
start = datetime(2019,1,1)
end = datetime(2019,6,3)
# date = start.strftime('%Y-%m-%d')
# print(date)
datas = data.load_bar_data(symbol,exchange,day,start,end)
# # print(datas)
#
#
# # d =d
# print(datas[0])
print(pprint.pformat(datas))