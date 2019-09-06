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


class DownloadData(object):

    def __init__(self,settings,database_manager=None):
        self.settings = settings
        self.token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'
        self.pro = ts.pro_api(self.token)
        if not database_manager:
            self.database_manager = init('_',self.settings)
        else:
            self.database_manager = database_manager

    @staticmethod
    def str2datatime(time:str):
        return dt.datetime.strptime(time, '%Y%m%d')

    def generate_bar_from_row(self,row, symbol, exchange):
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
            datetime=self.str2datatime(row['trade_date']),
            gateway_name="DB"
        )
        return bar

    def download_day_bar(self,vt_symbol,start_date,end_data=None):
        """下载某一合约的分钟线数据"""
        print(f"开始下载合约数据{vt_symbol}")
        symbol, exchange = vt_symbol.split(".")

        start = time()

        if not end_data:
            end_data = start_date

        df = self.pro.daily(
            ts_code=vt_symbol,
            start_date=start_date,
            end_date=end_data
        )
        df.sort_values(by='trade_date',ascending=True,inplace=True)

        bars = []
        for ix, row in df.iterrows():
            bar = self.generate_bar_from_row(row, symbol, exchange)
            bars.append(bar)
        self.database_manager.save_bar_data(bars)

        end = time()
        cost = (end - start) * 1000

        print(
            "合约%s的K线数据下载完成共%d，耗时%7.2f毫秒"
            % (symbol, len(df),cost)
        )


if __name__ == "__main__":
    s = Settings()
    dd = DownloadData(s)
    dd.download_day_bar('002192.SZ','20190618','20190813')



