from enum import Enum
from time import time

import tushare as ts
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

from backtesting.example.stocks_collection import stocks_TMT
from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from base_utils.object import BarData
from settings.setting import Settings
stocks_TMT

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
        if time:
            return dt.datetime.strptime(time, '%Y%m%d')
        else:
            return None

    def generate_bar_from_row(self,row, symbol, exchange,build_time=None,remove_time=None):
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
            build_time = self.str2datatime(build_time),
            remove_time =self.str2datatime(remove_time),
            gateway_name="DB"
        )
        return bar

    def download_day_bar(self,vt_symbol,start_date,end_data=None,build_time=None):
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
            bar = self.generate_bar_from_row(row, symbol, exchange,build_time)
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
    start_day = '20191125'
    end_day = '20191225'
    # end_day = None
    code_list = [
        '002192.SZ', # 融捷
        # '002466.SZ', # 天齐
        '002460.SZ', # 赣锋锂业
        # '603026.SH', # 石大
        #
        # '600276.SH', # 恒瑞
        '600196.SH', # 复星
        # '300760.SZ', # 迈瑞
        # '000001.SH', #上证
        # '399001.SZ' #深证
    ]

    for code in code_list:
        dd.download_day_bar(code,start_day,end_day)
    # dd.download_day_bar('002466.SZ','20190921','20190930') # 天齐
    # dd.download_day_bar('002460.SZ','20190921','20190930') # 赣锋锂业
    # dd.download_day_bar('600276.SH','20170101','20191010') # 恒瑞
    # dd.download_day_bar('600196.SH','20170101','20191010') # 复星
    # dd.download_day_bar('300760.SZ','20170101','20191010') # 迈瑞

    # for name,code in stocks_TMT.items():
    #     print(name)
    #     dd.download_day_bar(code[0],start_day,end_day,code[1])
