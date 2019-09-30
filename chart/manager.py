from collections import defaultdict
from typing import Dict, List, Tuple
from datetime import datetime

from pandas import DataFrame, DatetimeIndex,RangeIndex


from base_utils.object import BarData
from .base import to_int


class LineManager:
    """
    管理dateFrame类型的数据
    """
    def __init__(self):
        self._data_type = None
        self._data:DataFrame = None
        self._index_dataframe_map: Dict = {}
        self._value_ranges:Dict = {}

    def get_datetime(self,ix):
        ix = max(to_int(ix) -1,0)
        return self._index_dataframe_map.get(ix,None)

    def get_count(self):
        return len(self._data)

    def get_all_bars(self) -> DataFrame:
        """
        返回所有要划线的数据
        """
        return self._data

    def get_data(self, ix: float):
        """
        Get bar data with index.
        """
        ix = to_int(ix)
        dt = self._index_dataframe_map.get(ix, None)
        if not dt:
            return None

        return self._data.loc[dt]

    def update_history(self,history):
        # 对进来的数据按index排序，默认Index是datetime
        self._data = history.sort_index()
        del self._data['volume']
        ix_list = range(len(self._data))
        # 将横坐标与index对应起来
        self._index_dataframe_map = dict(zip(ix_list,self._data.index))
        # self._datas = dict(ix_list,self._data)
        self._clear_cache()

    def get_price_range(self, min_ix: float = None, max_ix: float = None) -> Tuple[float, float]:
        if len(self._data) == 0:
            return 0, 1

        if not min_ix:
            min_ix = 0
            max_ix = len(self._data) - 1
        else:
            min_ix = to_int(min_ix)
            max_ix = to_int(max_ix)
            max_ix = min(max_ix, self.get_count())

        buf = self._value_ranges.get((min_ix, max_ix), None)
        if buf:
            return buf

        lines_list = self._data[min_ix:max_ix + 1]
        max_value = lines_list.max().max()
        min_value = lines_list.min().min()

        self._value_ranges[(min_ix, max_ix)] = min_value,max_value

        return min_value,max_value

    def _clear_cache(self) -> None:
        """
        Clear cached range data.
        """
        self._value_ranges.clear()



class BarManager:
    """
    将生成的Bar
    """

    def __init__(self):
        """"""
        self._bars: Dict[datetime, BarData] = {}
        self._datetime_index_map: Dict[datetime, int] = {}
        self._index_datetime_map: Dict[int, datetime] = {}

        self._price_ranges: Dict[Tuple[int, int], Tuple[float, float]] = {}
        self._volume_ranges: Dict[Tuple[int, int], Tuple[float, float]] = {}

        # 附加线有关的参数
        self._addition_line = defaultdict(dict)
        self._addition_line_first_ix = {}

        # 成交单有关
        self._trade_orders = defaultdict(dict)
        self._data_type = None

    def update_history(self, history: List[BarData]) -> None:
        """
        Update a list of bar data.
        """
        # Put all new bars into dict
        # 创建bar时间与bar本身的对应
        if self._data_type is None:
            self._data_type = history[0].interval
        for bar in history:
            self._bars[bar.datetime] = bar

        # Sort bars dict according to bar.datetime
        # 将字典根据bars时间排列
        self._bars = dict(sorted(self._bars.items(), key=lambda tp: tp[0]))

        # Update map relationiship
        ix_list = range(len(self._bars))
        dt_list = self._bars.keys()

        # 时间：序列号
        self._datetime_index_map = dict(zip(dt_list, ix_list))
        # 序列号：时间
        self._index_datetime_map = dict(zip(ix_list, dt_list))

        # Clear data range cache
        self._clear_cache()

    def update_bar(self, bar: BarData) -> None:
        """
        Update one single bar data.
        """
        dt = bar.datetime

        if dt not in self._datetime_index_map:
            ix = len(self._bars)
            self._datetime_index_map[dt] = ix
            self._index_datetime_map[ix] = dt

        self._bars[dt] = bar

        self._clear_cache()

    def get_count(self) -> int:
        """
        Get total number of bars.
        """
        return len(self._bars)

    def get_index(self, dt: datetime) -> int:
        """
        Get index with datetime.
        """
        return self._datetime_index_map.get(dt, None)

    def get_datetime(self, ix: float) -> datetime:
        """
        Get datetime with index.
        """
        ix = to_int(ix)
        return self._index_datetime_map.get(ix, None)

    def get_bar(self, ix: float) -> BarData:
        """
        Get bar data with index.
        """
        ix = to_int(ix)
        dt = self._index_datetime_map.get(ix, None)
        if not dt:
            return None

        return self._bars[dt]

    def get_addition_line(self,ix:float)->dict:
        ix = to_int(ix)
        dt = self._index_datetime_map.get(ix,None)
        result = {}
        if dt:
            for name,value in self._addition_line.items():
                line_value = self._addition_line[name].get(dt,None)
                if line_value:
                    result[name] = round(line_value,2)

        return result

    def get_trade_order(self,ix:float) -> float:
        ix = to_int(ix)
        dt = self._index_datetime_map.get(ix,None)

        if self._trade_orders:
            return self._trade_orders.get(dt,None)
        else:
            return None

    def get_all_bars(self) -> List[BarData]:
        """
        Get all bar data.
        """
        return list(self._bars.values())

    def get_price_range(self, min_ix: float = None, max_ix: float = None) -> Tuple[float, float]:
        """
        Get price range to show within given index range.
        """
        if not self._bars:
            return 0, 1

        if not min_ix:
            min_ix = 0
            max_ix = len(self._bars) - 1
        else:
            min_ix = to_int(min_ix)
            max_ix = to_int(max_ix)
            max_ix = min(max_ix, self.get_count())

        # buf = self._price_ranges.get((min_ix, max_ix), None)
        # if buf:
        #     return buf

        bar_list = list(self._bars.values())[min_ix:max_ix + 1]
        first_bar = bar_list[0]
        max_price = first_bar.high_price
        min_price = first_bar.low_price

        if len(self._addition_line_first_ix) != 0:
            # 获取附加线的最大最小值，一般都比原bar要大，所以为了能在界面中不丢失线，需要获得更大的y轴范围
            temp_ix_max = self._addition_line_first_ix['ix_range'][1]
            temp_ix_min = self._addition_line_first_ix['ix_range'][0]
            if min_ix <= temp_ix_max and max_ix >= temp_ix_min  :
                for line_name, value in self._addition_line_first_ix.items():
                    if line_name is not 'ix_range':
                        min_index = max(temp_ix_min,min_ix)
                        max_index = min(temp_ix_max, max_ix)
                        for date_ix in range(min_index, max_index):
                            temp_dt = self._index_datetime_map[date_ix]
                            if self._addition_line[line_name].get(temp_dt):
                                temp_price = self._addition_line[line_name][temp_dt]
                                min_price = min(min_price,temp_price)
                                max_price = max(max_price,temp_price)
                        # print("addition_line min:%3.3f  max: %3.3f"%(min_price,max_price))

        for bar in bar_list[1:]:
            max_price = max(max_price, bar.high_price)
            min_price = min(min_price, bar.low_price)

        # self._price_ranges[(min_ix, max_ix)] = (min_price, max_price)
        # min_y = min(min_price,min_y)
        # max_y = max(max_price,max_y)
        return min_price, max_price

    def get_volume_range(self, min_ix: float = None, max_ix: float = None) -> Tuple[float, float]:
        """
        Get volume range to show within given index range.
        """
        if not self._bars:
            return 0, 1

        if not min_ix:
            min_ix = 0
            max_ix = len(self._bars) - 1
        else:
            min_ix = to_int(min_ix)
            max_ix = to_int(max_ix)
            max_ix = min(max_ix, self.get_count())

        buf = self._volume_ranges.get((min_ix, max_ix), None)
        if buf:
            return buf

        bar_list = list(self._bars.values())[min_ix:max_ix + 1]

        first_bar = bar_list[0]
        max_volume = first_bar.volume
        min_volume = 0

        for bar in bar_list[1:]:
            max_volume = max(max_volume, bar.volume)

        self._volume_ranges[(min_ix, max_ix)] = (min_volume, max_volume)
        return min_volume, max_volume

    def _clear_cache(self) -> None:
        """
        Clear cached range data.
        """
        self._price_ranges.clear()
        self._volume_ranges.clear()

    def set_additionline_ix_range(self,addition_line:defaultdict):
        """
        获得附近线的范围，与bar的时间相互对应上
        """
        self._addition_line = addition_line
        for line_name in addition_line:
            temp_value = dict(sorted(addition_line[line_name].items(), key=lambda tp: tp[0]))
            temp_list = list(temp_value.keys())
            ix_min = self._datetime_index_map[temp_list[0]]
            ix_max = len(addition_line[line_name])+ix_min
            if not self._addition_line_first_ix.get('ix_range'):
                self._addition_line_first_ix['ix_range'] = (ix_min,ix_max)
            else:
                temp_min, temp_max = self._addition_line_first_ix['ix_range']
                self._addition_line_first_ix['ix_range'] = (min(temp_min, ix_min), max(temp_max, ix_max))
            self._addition_line_first_ix[line_name]=(ix_min,ix_max)

    def set_trade_order(self,tradeorders):
        self._trade_orders = tradeorders

    def clear_all(self) -> None:
        """
        Clear all data in manager.
        """
        self._bars.clear()
        self._datetime_index_map.clear()
        self._index_datetime_map.clear()
        self._addition_line.clear()
        self._addition_line_first_ix.clear()
        self._clear_cache()
