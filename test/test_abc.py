import datetime
from typing import Sequence

from base_database.database import BaseDatabaseManager
from base_utils.constant import Exchange, Interval


class A(object):

    def __init__(self):
        self.a = 1
        self.b = 2

# a = A
# test_a : 'A' = a
# print(test_a)

class TestDataBase(BaseDatabaseManager):

    def __init__(self):
        self.a = 'test'

    def load_bar_data(
        self,
        symbol: str,
        exchange: "Exchange",
        interval: "Interval",
        start: datetime,
        end: datetime
    ):
        print('load_bar_data')

    def load_tick_data(
        self,
        symbol: str,
        exchange: "Exchange",
        start: datetime,
        end: datetime
    ):
        pass

    def save_bar_data(self):
        pass

    def save_tick_data(
        self,
        datas: Sequence["TickData"],
    ):
        pass

    def get_newest_bar_data(
        self,
        symbol: str,
        exchange: "Exchange",
        interval: "Interval"
    ) :

        pass


    def get_newest_tick_data(
        self,
        symbol: str,
        exchange: "Exchange",
    ) :

        pass


    def clean(self, symbol: str):

        pass


tdb = TestDataBase()
print(tdb.a)