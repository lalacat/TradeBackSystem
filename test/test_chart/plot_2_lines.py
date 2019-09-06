
import pprint
from datetime import datetime

from base_database.database_mongo import init, MongoManager
from base_utils.constant import Exchange, Interval
from settings.setting import Settings
from PyQt5 import QtCore
import pyqtgraph as pg
from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from chart import VolumeItem, ChartWidget, CandleItem
from settings.setting import Settings
from ui import create_qapp
import pandas as pd
# 读取数据

s = Settings()
init('a',s)
symbol = '002192'
exchange = Exchange('SZ')
day = Interval.DAILY
# 最新价
# newest_bar = data.get_newest_bar_data('002192',Exchange.SZ,Interval.DAILY)
# print(newest_bar)
# 指定日期价
start = datetime(2019,1,1)
end = datetime(2019,6,3)

data = MongoManager()
datas = data.load_bar_data(symbol,exchange,day,start,end)
print(datas[0].datetime)

# bars = pd.DataFrame(columns=['open', 'close', 'low', 'high', 'volume', 'openInterest'])
# opens = [ data.open_price for data in datas]
# closes = [data.close_price for data in datas]
# low = [data.low_price for data in datas]
# high = [data.high_price for data in datas]
# volume = [data.volume for data in datas]
# bars['open']=opens
# bars['close']=closes
# bars['low']=low
# bars['high']=high
# bars['volume']=volume
# bars['openInterest']=0
# print(bars)
#
# plot = pg.plot(title='州的先生zmister.com PyQtGraph教程 - plot()方法绘制两条线')
# plot.plot(opens)
# plot.plot(closes, pen='r')
# pg.QtGui.QGuiApplication.exec_()

class A :
    def __init__(self):
        self.a = 1
class B :
    def __init__(self):
        self.a = 1
class C :
    def __init__(self):
        self.a = 1

cls = []
dict_cls = {}
a = A()
b = B()
c = C()
cls.append(a)
cls.append(b)
cls.append(c)
dict_cls[1]=a
dict_cls[2]=b
dict_cls[3]=c

j = 5
for i in cls:
    i.a = j
    j+=1

for i in dict_cls.values():
    print(i.a)


# dict_cls.pop()


a = max(1,3,5)
print(a)
a = max(a,10)
print(a)