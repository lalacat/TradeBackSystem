import sys
from collections import defaultdict
from typing import List, Dict, Type

import pyqtgraph as pg

from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsTextItem, QTextEdit
from pyqtgraph import GraphicsLayout


class TestWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self._layout = GraphicsLayout()  # 创建一个网格布局
        self._layout.setContentsMargins(10, 10, 10, 10)
        self.setCentralItem(self._layout)

        label = pg.LabelItem()

        label.setText("这是一个label Item")
        label.item.setPos(100,100)

        text = pg.TextItem()
        text.setText("这是一个text Item")

        plot_01 = pg.PlotItem()
        plot_01.addItem(label)
        plot_01.setMenuEnabled(False)
        plot_01.setClipToView(True)
        plot_01.hideAxis('left')  # 隐藏左纵坐标轴
        plot_01.hideAxis('bottom')

        plot_01.showAxis('right')  # 显示右纵坐标轴
        # 字体沿Y轴翻转
        plot_01.invertY()
        plot_01.setDownsampling(mode='peak')

        plot_01.setRange(xRange=(0, 1), yRange=(0, 1))

        axis_width = plot_01.getAxis("right").width()
        axis_height = plot_01.getAxis("bottom").height()
        axis_offset = QtCore.QPointF(axis_width, axis_height)
        bottom_view = plot_01.getViewBox()
        # bottom_right= bottom_view.mapSceneToView(
        # bottom_view.sceneBoundingRect().bottomRight() - axis_offset)
        # top_left = bottom_view.mapSceneToView(bottom_view.sceneBoundingRect().topLeft())
        # label.setPos(top_left)
        # plot_02 = pg.PlotItem()
        # plot_02.addItem(label)

        #
        self._layout.addItem(plot_01)
        self._layout.nextRow()
        self._layout.addItem(plot_01)


        # self._layout.nextRow()
        # self._layout.nextRow()
        # self._layout.addItem(text)
        # self.addItem(self._layout)
        # self.addItem(text)

app = QtGui.QApplication(sys.argv)

w =TestWidget()
w.show()
sys.exit(app.exec_())
