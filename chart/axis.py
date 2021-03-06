from datetime import datetime
from typing import List

import pyqtgraph as pg

from base_utils.constant import Interval
from .base import AXIS_WIDTH, NORMAL_FONT
from .manager import BarManager, LineManager


class DatetimeAxis(pg.AxisItem):
    """"""

    def __init__(self, manager: BarManager, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

        self._manager: BarManager = manager

        self.setPen(width=AXIS_WIDTH)
        self.tickFont = NORMAL_FONT

    def tickStrings(self, values: List[int], scale: float, spacing: int):
        """
        Convert original index to datetime string.
        # 重写方法，设置横坐标的格式
        """
        strings = []
        print(values)
        for ix in values:
            dt = self._manager.get_datetime(ix)

            if not dt:
                s = ""
            else:
                if isinstance(self._manager,BarManager):
                    if self._manager._data_type == Interval.DAILY:
                        s = dt.strftime("%Y-%m-%d")
                    elif dt.hour:
                        s = dt.strftime("%Y-%m-%d\n%H:%M:%S")
                elif isinstance(self._manager,LineManager):
                    if isinstance(dt, datetime):
                        s = dt.strftime("%Y-%m-%d")
                    else:
                        s = str(dt)
                else:
                    s = ''

            strings.append(s)

        return strings
