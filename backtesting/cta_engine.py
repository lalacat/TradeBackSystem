from datetime import datetime
from typing import Callable

from base_database.initialize import database_manager
from base_utils.constant import Interval
from base_utils.object import BarData
from base_utils.utility import extract_vt_symbol


class CtaEngine(object):

    def __init__(self):
        self.database_manager = database_manager

    def load_bar(
        self,
        vt_symbol: str,
        days: int,
        interval: Interval,
        callback: Callable[[BarData], None]
    ):
        """"""
        symbol, exchange = extract_vt_symbol(vt_symbol)
        end = datetime.now()
        start = end - datetime.timedelta(days)

        # Query bars from RQData by default, if not found, load from database.
        # bars = self.query_bar_from_rq(symbol, exchange, interval, start, end)

        # if not bars:
        bars = self.database_manager.load_bar_data(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            start=start,
            end=end,
        )

        for bar in bars:
            callback(bar)