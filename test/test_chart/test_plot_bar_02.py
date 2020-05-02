from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets

from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from settings.setting import Settings
from ui import create_qapp

s = Settings()
app = create_qapp(s)

database_manager = init('_',s)

bars = database_manager.load_bar_data(
        "002192",
        Exchange.SZ,
        interval=Interval.DAILY,
        start=datetime(2015, 1, 1),
        end=datetime(2019, 8, 14)
)

class TimeLine(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # self.setMinimumSize(640, 430)  # 设置窗口最小尺寸
        self.setGeometry(300, 300, 960, 650)
        self.setWindowTitle('分时行情走势')
        self.setStyleSheet("QWidget { background-color: black }")
        # self.setMouseTracking(True)
        self.m_x = 0  # 光标x轴位置
        self.m_y = 0  # 光标y轴位置
        self.w = 960
        self.h = 650

        self.total_amount_data = 3000
        self.grid_padding_left = 55  # 左侧补丁边距
        self.grid_padding_right = 55  # 右侧补丁边距 如果设置为245，则显示五档盘口等信息
        self.grid_padding_top = 20  # 顶部补丁边距
        self.grid_padding_bottom = 17  # 底部补丁边距
        self.paint = QtGui.QPainter()

        self.sum_height = self.grid_padding_top + self.grid_padding_bottom
        self.sum_width = self.grid_padding_left + self.grid_padding_right
        # self.paint.begin(self)
        #
        # sum_height = self.grid_padding_top + self.grid_padding_bottom
        # self.paint.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine))
        # self.paint.drawRect(self.grid_padding_left, self.grid_padding_top, self.w - sum_width, self.h - sum_height)
        # self.paint.drawText(4 + self.grid_padding_left, self.grid_padding_top - 4
        #                     , 'test_name')  # 股票名称
        # self.paint.end()


    def mouseMoveEvent(self, event):
        self.m_x = int(event.x())
        self.m_y = int(event.y())
        self.repaint()

    def paintEvent(self, event):
        self.paint.begin(self)

        self.paint.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine))
        self.paint.drawRect(self.grid_padding_left, self.grid_padding_top, self.w - self.sum_width, self.h - self.sum_height)
        self.paint.drawText(4 + self.grid_padding_left, self.grid_padding_top - 4
                            , 'test_name')  # 股票名称
        self.paint.end()
    #     widget = ChartWidget(self)
    #     widget.add_plot("candle", hide_x_axis=True)
    #     widget.add_item(CandleItem, "candle", "candle")
    #     widget.add_cursor()
    #     widget.update_history(bars)

dt = TimeLine()
dt.show()
app.exec_()
