from collections import defaultdict
from typing import List, Dict, Type

import pyqtgraph as pg

from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsTextItem

from chart.base import GREY_COLOR, AXIS_WIDTH, NORMAL_FONT


class DatetimeFrameAxis(pg.AxisItem):
    def __init__(self, manager, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

        self._manager = manager

        self.setPen(width=AXIS_WIDTH)
        self.tickFont = NORMAL_FONT

    def tickStrings(self, values: List[int], scale: float, spacing: int):
        """
        Convert original index to datetime string.
        # 重写方法，设置横坐标的格式
        """
        strings = []

        for ix in values:
            # dt = self._manager.get_datetime(ix)
            dt = self._manager.index[int(ix)-1]

            if not dt:
                s = ""
            else:
                s = dt.strftime("%Y-%m-%d")
            strings.append(s)

        return strings


class ChartLineWidget(pg.PlotWidget):
    def __init__(self,manager,parent: QtWidgets.QWidget = None):
        """"""
        super().__init__(parent)
        self._plots: Dict[str, pg.PlotItem] = {}
        self._first_plot: pg.PlotItem = None
        self._right_ix: int = 0  # Index of most right data
        self._item_class = set()
        self._manager = manager
        self._init_ui()
        self._bar_count = 20

    def _init_ui(self) -> None:
        """
        创建一个主要的部件
        :return:
        """
        self.setWindowTitle("ChartWidget of vn.py")

        self._layout = pg.GraphicsLayout()  # 创建一个网格布局
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.setSpacing(0)  # 每个item之间的距离

        self._layout.setBorder(color=GREY_COLOR, width=0.8)
        self._layout.setZValue(0)
        self.setCentralItem(self._layout)

        # 创建水平轴
        self._x_axis = DatetimeFrameAxis(self._manager, orientation='bottom')

    def add_plot(
        self,
        minimum_height: int = 80,
        maximum_height: int = None,
        hide_x_axis: bool = False # 隐藏坐标轴，默认是不隐藏的
    ) -> None:
        """
        Add plot area.
        """
        # Create plot object
        self._first_plot = pg.PlotItem(axisItems={'bottom': self._x_axis})
        self._first_plot.setMenuEnabled(False)
        self._first_plot.setClipToView(True)
        self._first_plot.hideAxis('left') # 隐藏左纵坐标轴
        self._first_plot.showAxis('right') # 显示右纵坐标轴
        self._first_plot.setDownsampling(mode='peak')

        # (min,max) The range that should be visible along the x-axis.
        self._first_plot.setRange(xRange=(0, 1), yRange=(0, 1))
        #  自动标尺，在左下角有个A按钮
        self._first_plot.hideButtons()
        # 默认大小的时候最小的高度，太高的话，显示不了底部
        self._first_plot.setMinimumHeight(minimum_height)

        if maximum_height:
            self._first_plot.setMaximumHeight(maximum_height)

        if hide_x_axis:
            self._first_plot.hideAxis("bottom")


        # Connect view change signal to update y range function
        # 实现缩放功能
        view = self._first_plot.getViewBox()
        # 在改变视图（就是x,y轴的范围）的时候发出
        view.sigXRangeChanged.connect(self._update_y_range)
        view.setMouseEnabled(x=True, y=False)

        # Set right axis
        right_axis = self._first_plot.getAxis('right')
        right_axis.setWidth(60)
        right_axis.tickFont = NORMAL_FONT

        # self._first_plot = plot

        self._first_plot.plot(self._manager['close_price'])
        self._first_plot.plot(self._manager['open_price'], pen='r')
        self._layout.addItem(self._first_plot)
        self._update_plot_limits()
        self.move_to_right()

    def _update_plot_limits(self) -> None:
        """
        Update the limit of plots.
        # 限定了最大和最小的显示范围
        """
        self._first_plot.setLimits(
                xMin=-1,
                xMax=len(self._manager),
                yMin=self._manager['close_price'].max(),
                yMax=self._manager['close_price'].min()
            )

    def _update_y_range(self) -> None:
        """
        Update the y-axis range of plots.
        """
        view = self._first_plot.getViewBox()
        view_range = view.viewRange()

        min_ix = max(0, int(view_range[0][0]))
        max_ix = min(len(self._manager)-1, int(view_range[0][1]))

        min_value = min(
            self._manager['close_price'][min_ix:max_ix].min(),
            self._manager['open_price'][min_ix:max_ix].min()
        )
        max_value = max(
            self._manager['close_price'][min_ix:max_ix].max(),
            self._manager['open_price'][min_ix:max_ix].max()
        )
        y_range = (min(min_value,max_value),max(min_value,max_value))
        self._first_plot.setRange(yRange=y_range)
        print(y_range)
        self._first_plot.setLimits(yMin=y_range[0],yMax=y_range[1])

    def _update_x_range(self) -> None:
        """
        Update the x-axis range of plots.
        Set the visible range of the ViewBox
        与鼠标在放大缩小有关
        """
        max_ix = self._right_ix
        min_ix = self._right_ix - 50
        self._first_plot.setRange(xRange=(min_ix, max_ix), padding=0)


    def move_to_right(self) -> None:
        """
        Move chart to the most right.
        """
        # 导入数据的总个数
        self._right_ix = len(self._manager)
        self._update_x_range()
    #
    # def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
    #     """
    #     Reimplement this method of parent to zoom in/out.
    #     """
    #     delta = event.angleDelta()
    #
    #     if delta.y() > 0:
    #         self._on_key_up()
    #     elif delta.y() < 0:
    #         self._on_key_down()

    def _on_key_down(self) -> None:
            """
            Zoom out the chart.
            """
            self._bar_count *= 1.2
            self._bar_count = min(int(self._bar_count), len(self._manager))

            self._update_x_range()

    def _on_key_up(self) -> None:
        """
        Zoom in the chart.
        """
        self._bar_count /= 1.2
        self._bar_count = max(int(self._bar_count), 50)

        self._update_x_range()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """
        Reimplement this method of parent to update current max_ix value.
        只跟pen绘图有关系
        """
        view = self._first_plot.getViewBox()
        view_range = view.viewRange()
        self._right_ix = max(0, view_range[0][1])

        super().paintEvent(event)