from abc import abstractmethod
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Tuple

import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from pandas import DataFrame

from base_utils.constant import Direction, Offset
from base_utils.object import BarData, TradeData
from .base import UP_COLOR, DOWN_COLOR, PEN_WIDTH, BAR_WIDTH, UP_LINE_COLOR, DOWN_LINE_COLOR, COLOR_GROUP, WHITE_COLOR, \
    OPEN_COLOR, CLOSE_COLOR
from .manager import BarManager


class ChartItem(pg.GraphicsObject):
    """"""

    def __init__(self, manager: BarManager):
        """"""
        super().__init__()

        self._manager: BarManager = manager
        # 保存画笔，一个bar对应一个画笔，画笔能够设定bar的颜色图形
        self._bar_picutures: Dict[int, QtGui.QPicture] = {}
        self._item_picuture: QtGui.QPicture = None

        # 笔刷用于画阳线段
        self._up_pen: QtGui.QPen = pg.mkPen(
            color=UP_COLOR, width=PEN_WIDTH
        )
        self._up_brush: QtGui.QBrush = pg.mkBrush(color=UP_COLOR)
        # 用于画阴线段
        self._down_pen: QtGui.QPen = pg.mkPen(
            color=DOWN_COLOR, width=PEN_WIDTH
        )
        self._down_brush: QtGui.QBrush = pg.mkBrush(color=DOWN_COLOR)

        self._rect_area: Tuple[float, float] = None

        # Very important! Only redraw the visible part and improve speed a lot.
        # 只重画部分图形，大大提高界面更新速度
        self.setFlag(self.ItemUsesExtendedStyleOption)

    @abstractmethod
    def _draw_bar_picture(self, ix: int, bar: BarData,**kwargs) -> QtGui.QPicture:
        """
        Draw picture for specific bar.
        """
        pass

    @abstractmethod
    def boundingRect(self) -> QtCore.QRectF:
        """
        Get bounding rectangles for item.
        """
        pass

    @abstractmethod
    def get_y_range(self, min_ix: int = None, max_ix: int = None) -> Tuple[float, float]:
        """
        Get range of y-axis with given x-axis range.

        If min_ix and max_ix not specified, then return range with whole data set.
        """
        pass

    @abstractmethod
    def get_info_text(self, ix: int) -> str:
        """
        Get information text to show by cursor.
        """
        pass

    def update_history(self, history: List[BarData], addition_line: defaultdict() = None, tradeorders : defaultdict() =None ) -> BarData:
        """
        Update a list of bar data.
        将bar数据装入到绘画组中
        """
        self._bar_picutures.clear()

        bars = self._manager.get_all_bars()  # List
        if isinstance(bars,list):
            for ix, bar in enumerate(bars):
                line_value = {}
                tradeorder = None
                # 添加附加线
                if addition_line:
                    for value in addition_line:
                        if addition_line[value].get(bar.datetime):
                            line_value[value] = addition_line[value].get(bar.datetime)
                # 添加成交点
                if tradeorders:
                    tradeorder = tradeorders.get(bar.datetime,None)

                # 具体的item实现_draw_bar_picture方法，返回的是picture
                bar_picture = self._draw_bar_picture(ix, bar,line_value,tradeorder)
                self._bar_picutures[ix] = bar_picture
        else:
            ixs = range(self._manager.get_count())
            for ix,bar in zip(ixs,bars.iterrows()):
                bar_picture = self._draw_bar_picture(ix, bar[1])
                self._bar_picutures[ix] = bar_picture
        self.update()

    def update_bar(self, bar: BarData) -> BarData:
        """
        Update single bar data.
        """
        ix = self._manager.get_index(bar.datetime)

        bar_picture = self._draw_bar_picture(ix, bar)
        self._bar_picutures[ix] = bar_picture

        self.update()

    def update(self) -> None:
        """
        Refresh the item.
        """
        if self.scene():
            self.scene().update()

    def paint(
        self,
        painter: QtGui.QPainter,
        opt: QtWidgets.QStyleOptionGraphicsItem,
        w: QtWidgets.QWidget
    ):
        """
        Reimplement the paint method of parent class.

        This function is called by external QGraphicsView.
        """
        rect = opt.exposedRect

        min_ix = int(rect.left())
        max_ix = int(rect.right())
        max_ix = min(max_ix, len(self._bar_picutures))

        rect_area = (min_ix, max_ix)
        if rect_area != self._rect_area or not self._item_picuture:
            self._rect_area = rect_area
            self._draw_item_picture(min_ix, max_ix)

        self._item_picuture.play(painter)

    def _draw_item_picture(self, min_ix: int, max_ix: int) -> None:
        """
        Draw the picture of item in specific range.
        """
        self._item_picuture = QtGui.QPicture()
        painter = QtGui.QPainter(self._item_picuture)

        for n in range(min_ix, max_ix):
            bar_picture = self._bar_picutures[n]
            bar_picture.play(painter)

        painter.end()

    def clear_all(self) -> None:
        """
        Clear all data in the item.
        """
        self._item_picuture = None
        self._bar_picutures.clear()
        self.update()


class CandleItem(ChartItem):
    """"""

    def __init__(self, manager: BarManager):
        """"""
        super().__init__(manager)
        self.pre_values = {}
        self.pen_color = {}
        self.colors = COLOR_GROUP
        self.arrows = []

    def _draw_bar_picture(self, ix: int, bar: BarData, addition_line: dict = None,tradeorders:list() = None) -> QtGui.QPicture:
        """
        画每个bar的形态
        :param ix:
        :param bar:
        :return:
        """
        # Create objects
        candle_picture = QtGui.QPicture()
        painter = QtGui.QPainter(candle_picture)

        # Set painter color
        if bar.close_price >= bar.open_price:
            # 设置阴线的画笔和画刷
            painter.setPen(self._up_pen)
            painter.setBrush(self._up_brush)
        else:
            painter.setPen(self._down_pen)
            painter.setBrush(self._down_brush)

        # Draw candle body
        if bar.open_price == bar.close_price:
            # 当涨停或跌停的时候，直接画横线
            painter.drawLine(
                QtCore.QPointF(ix - BAR_WIDTH, bar.open_price),
                QtCore.QPointF(ix + BAR_WIDTH, bar.open_price),
            )
        else:
            rect = QtCore.QRectF(
                ix - BAR_WIDTH,
                bar.open_price,
                BAR_WIDTH * 2,
                bar.close_price - bar.open_price
            )
            painter.drawRect(rect)

        # Draw candle shadow
        body_bottom = min(bar.open_price, bar.close_price)
        body_top = max(bar.open_price, bar.close_price)

        if bar.low_price < body_bottom:
            painter.drawLine(
                QtCore.QPointF(ix, bar.low_price),
                QtCore.QPointF(ix, body_bottom),
            )

        if bar.high_price > body_top:
            painter.drawLine(
                QtCore.QPointF(ix, bar.high_price),
                QtCore.QPointF(ix, body_top),
            )

        # 附加线
        if addition_line:
            for line_name in addition_line.keys():
                line_value = addition_line[line_name]
                if not self.pen_color.get(line_name, None):
                    self.pen_color[line_name] = self.colors.pop()
                painter.setPen(pg.mkPen(color=self.pen_color[line_name]))

                if not self.pre_values.get(line_name, None):
                    self.pre_values[line_name] = 0

                if self.pre_values[line_name] == 0:
                    pass
                    # painter.drawLine(QtCore.QPointF(ix, line_value), QtCore.QPointF(ix, line_value))
                else:
                    painter.drawLine(QtCore.QPointF(ix - 1, self.pre_values[line_name]), QtCore.QPointF(ix, line_value))
                self.pre_values[line_name] = line_value

        # 成交点
        if tradeorders:
            for tradeorder in tradeorders:
                trade_price = tradeorder.price
                offset = tradeorder.offset
                if offset == Offset.OPEN :
                    arrow = pg.ArrowItem(pos=(ix, trade_price), angle=180, tipAngle=60, headLen=5, tailLen=10, tailWidth=2,
                                         pen={'color': 'w', 'width': 0.8}, brush= OPEN_COLOR)
                if offset == Offset.CLOSE :
                    # arrow = pg.ArrowItem(pos=(ix, trade_price), angle=0, tipAngle=40, headLen=8, tailLen=None, tailWidth=8,
                    #                      pen={'color': 'w', 'width': 1}, brush= CLOSE_COLOR)
                    arrow = pg.ArrowItem(pos=(ix, trade_price), angle=0, tipAngle=40, headLen=5, tailLen=10, tailWidth=2,
                                         pen={'color': 'w', 'width': 1}, brush= CLOSE_COLOR)
                self.arrows.append(arrow)
        # Finish
        painter.end()
        return candle_picture

    def boundingRect(self) -> QtCore.QRectF:
        """"""
        min_price, max_price = self._manager.get_price_range()
        rect = QtCore.QRectF(
            0,
            min_price,
            len(self._bar_picutures),
            max_price - min_price
        )
        return rect

    def get_y_range(self, min_ix: int = None, max_ix: int = None) -> Tuple[float, float]:
        """
        设置显示y轴的最大最小，如果添加自己的画线的话，需要在这里进行调整
        Get range of y-axis with given x-axis range.
        If min_ix and max_ix not specified, then return range with whole data set.
        """
        min_price, max_price = self._manager.get_price_range(min_ix, max_ix)
        return min_price, max_price

    # def get_info_text(self, ix: int) -> str:
    #     """
    #     Get information text to show by cursor.
    #     显示在光标上
    #     """
    #     bar = self._manager.get_bar(ix)
    #
    #     if bar:
    #         words = [
    #             "Date",
    #             bar.datetime.strftime("%Y-%m-%d"),
    #             "",
    #             "Time",
    #             bar.datetime.strftime("%H:%M"),
    #             "",
    #             "Open",
    #             str(bar.open_price),
    #             "",
    #             "High",
    #             str(bar.high_price),
    #             "",
    #             "Low",
    #             str(bar.low_price),
    #             "",
    #             "Close",
    #             str(bar.close_price)
    #         ]
    #         text = "\n".join(words)
    #     else:
    #         text = ""
    #
    #     return text

    def get_info_text(self, ix: int) -> str:
        bar = self._manager.get_bar(ix)
        addition_line = self._manager.get_addition_line(ix)
        tradeorders = self._manager.get_trade_order(ix)
        text = '<p>'
        if bar:
            text += "<span style='color:#FFDEAD'><strong>日期:</strong></span>" \
                   "<span style='color:white'><strong>{0} </strong></span>" \
                   "<span style='color:#FFDEAD'>开盘价:</span>" \
                   "<span style='color:white;'>{1} </span>" \
                   "<span style='color:#FFDEAD'>收盘价:</span>" \
                   "<span style='color:white;'>{2} </span>" \
                   "<span style='color:#FFDEAD'>最高价:</span>" \
                   "<span style='color:{high_color}'>{3} </span>" \
                   "<span style='color:#FFDEAD'>最低价:</span> " \
                   "<span style='color:{low_color}'>{4} </span> " .format(
                bar.datetime.strftime("%Y-%m-%d"),
                str(bar.open_price),
                str(bar.open_price),
                str(bar.high_price),
                str(bar.low_price),
                high_color = UP_COLOR,
                low_color = DOWN_COLOR)
            if tradeorders:
                # trade_text = "<p style='font-size:9pt'>"
                trade_text = ""
                for tradeorder in tradeorders:
                    if tradeorder.offset == Offset.OPEN:
                        color = OPEN_COLOR
                    else:
                        color = CLOSE_COLOR
                    trade_text += "<span ><strong>{0}: </strong></span>" \
                    "<span style='color:{1}'>{2} </span>".format(
                        tradeorder.offset.value,
                        color,
                        tradeorder.price
                    )
                # trade_text += '</p>'
                text += trade_text
            if addition_line:
                addition_text =  "<p style='color:#808069;font-size:8pt'>"
                for name, value in addition_line.items():
                    addition_text += "<span style='color:#FFDEAD' ><strong>{0}: </strong></span>" \
                                     "<span style='color:{1}'>{2} </span>" .format(
                        name,
                        self.pen_color[name],
                        value
                    )
                addition_text +='</p>'
                text += addition_text
            text += '</p>'
        else:
            text = ''
        return text


class LineItem(ChartItem):
    def __init__(self, manager: BarManager):
        """"""
        super().__init__(manager)
        self.colors = COLOR_GROUP
        self.pre_values = {}
        self.pen_color = {}
        self.colors = COLOR_GROUP

    def _draw_bar_picture(self, ix: int, datas: Dict, *args,**kw) -> QtGui.QPicture:
        """"""
        # 设置颜色
        # 设置线的类型

        line_picture = QtGui.QPicture()
        painter = QtGui.QPainter(line_picture)
        # self.get_info_text(ix)
        # Set painter color
        for line_name,line_value in datas.items():
            if not self.pen_color.get(line_name, None):
                self.pen_color[line_name] = self.colors.pop()
            painter.setPen(pg.mkPen(color=self.pen_color[line_name]))

            if not self.pre_values.get(line_name, None):
                self.pre_values[line_name] = 0

            if self.pre_values[line_name] != 0:
                painter.drawLine(QtCore.QPointF(ix - 1, self.pre_values[line_name]), QtCore.QPointF(ix, line_value))
            self.pre_values[line_name] = line_value

        # Finish
        painter.end()
        return line_picture

    def boundingRect(self) -> QtCore.QRectF:
        """"""
        min_price, max_price = self._manager.get_price_range()
        rect = QtCore.QRectF(
            0,
            min_price,
            len(self._bar_picutures),
            max_price - min_price
        )
        return rect

    def get_y_range(self, min_ix: int = None, max_ix: int = None) -> Tuple[float, float]:
        """
        Get range of y-axis with given x-axis range.

        If min_ix and max_ix not specified, then return range with whole data set.
        """
        min_price, max_price = self._manager.get_price_range(min_ix, max_ix)
        return min_price, max_price

    def get_info_text(self, ix: int) -> str:
        """
        Get information text to show by cursor.
        显示在光标上
        """
        # Series
        line = self._manager.get_bar(ix)
        word = []
        if line is not None:
            for k,i in line.items():
                word.append(k)
                word.append(str(i))
            text2 = "\n".join(word)
        else:
            text2 = ""

        return text2



class VolumeItem(ChartItem):
    """"""

    def __init__(self, manager: BarManager):
        """"""
        super().__init__(manager)

    def _draw_bar_picture(self, ix: int, bar: BarData, *args,**kw) -> QtGui.QPicture:
        """"""
        # Create objects
        volume_picture = QtGui.QPicture()
        painter = QtGui.QPainter(volume_picture)

        # Set painter color
        if bar.close_price >= bar.open_price:
            painter.setPen(self._up_pen)
            painter.setBrush(self._up_brush)
        else:
            painter.setPen(self._down_pen)
            painter.setBrush(self._down_brush)

        # Draw volume body
        rect = QtCore.QRectF(
            ix - BAR_WIDTH,
            0,
            BAR_WIDTH * 2,
            bar.volume
        )
        painter.drawRect(rect)

        # Finish
        painter.end()
        return volume_picture

    def boundingRect(self) -> QtCore.QRectF:
        """"""
        min_volume, max_volume = self._manager.get_volume_range()
        rect = QtCore.QRectF(
            0,
            min_volume,
            len(self._bar_picutures),
            max_volume - min_volume
        )
        return rect

    def get_y_range(self, min_ix: int = None, max_ix: int = None) -> Tuple[float, float]:
        """
        Get range of y-axis with given x-axis range.

        If min_ix and max_ix not specified, then return range with whole data set.
        """
        min_volume, max_volume = self._manager.get_volume_range(min_ix, max_ix)
        return min_volume, max_volume

    def get_info_text(self, ix: int) -> str:
        """
        Get information text to show by cursor.
        """
        bar = self._manager.get_bar(ix)

        if bar:
            text = f"Volume {bar.volume}"
        else:
            text = ""

        return text
