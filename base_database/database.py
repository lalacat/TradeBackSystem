from abc import abstractmethod, ABC
from enum import Enum
from datetime import datetime
from enum import Enum

# 提供基础设定，及基础的抽象方法
from typing import Optional, Sequence


class Driver(Enum):
    '''
    Enum 的成员均为单例（Singleton），并且不可实例化，不可更改.
    枚举是可以比较的:
    举成员可进行同一性比较,可进等值比较,不能进行大小比较.
    总结:Enum可以把一组相关常量定义在一个class中，且class不可变，而且成员可以直接比较,并且枚举有多种实现方法。
    '''
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"


class BaseDatabaseManager(ABC):

    @abstractmethod
    def load_bar_data(
        self,
        symbol: str,
        exchange: "Exchange",
        interval: "Interval",
        start: datetime,
        end: datetime
    ) -> Sequence["BarData"]:
        pass

    @abstractmethod
    def load_tick_data(
        self,
        symbol: str,
        exchange: "Exchange",
        start: datetime,
        end: datetime
    ) -> Sequence["TickData"]:
        pass

    @abstractmethod
    def save_bar_data(
        self,
        datas: Sequence["BarData"],
    ):
        pass

    @abstractmethod
    def save_tick_data(
        self,
        datas: Sequence["TickData"],
    ):
        pass

    @abstractmethod
    def get_newest_bar_data(
        self,
        symbol: str,
        exchange: "Exchange",
        interval: "Interval"
    ) -> Optional["BarData"]:
        """
        If there is data in database, return the one with greatest datetime(newest one)
        otherwise, return None
        """
        pass

    @abstractmethod
    def get_newest_tick_data(
        self,
        symbol: str,
        exchange: "Exchange",
    ) -> Optional["TickData"]:
        """
        If there is data in database, return the one with greatest datetime(newest one)
        otherwise, return None
        """
        pass

    @abstractmethod
    def clean(self, symbol: str):
        """
        delete all records for a symbol
        """
        pass

