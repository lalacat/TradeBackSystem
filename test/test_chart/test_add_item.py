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

        label = pg.LabelItem()
        label.setText("这是一个label Item")
        label_01 = pg.LabelItem()
        label_01.setText("这是一个label1 Item")
        label_02 = pg.LabelItem()
        label_02.setText("这是一个label2 Item")

        text = pg.TextItem(rotateAxis=(1,0))
        text.setText("这是一个text Item")

        self._layout.addItem(label)
        self._layout.nextRow()
        self._layout.addItem(label_01)
        self._layout.nextRow()

        self._layout.addItem(label_02)
        # self._layout.nextRow()
        # self._layout.addItem(text)
        self.addItem(self._layout)
        self.addItem(text)

app = QtGui.QApplication(sys.argv)

w =TestWidget()
w.show()
sys.exit(app.exec_())
