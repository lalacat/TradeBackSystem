from collections import deque
from datetime import datetime
from functools import partial

import numpy as np
import pandas as pd
import pyqtgraph as pg
import tushare as ts
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont

from base_database.database_mongo import init, MongoManager
from base_utils.constant import Interval, Exchange
# 主窗口类
from settings.setting import Settings

token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'
pro = ts.pro_api(token)

########################################################################
# 键盘鼠标功能
########################################################################
class KeyWraper(QtWidgets.QWidget):
    """键盘鼠标功能支持的元类"""

    # 初始化
    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

    # 重载方法keyPressEvent(self,event),即按键按下事件方法
    # ----------------------------------------------------------------------
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.onUp()
        elif event.key() == QtCore.Qt.Key_Down:
            self.onDown()
        elif event.key() == QtCore.Qt.Key_Left:
            self.onLeft()
        elif event.key() == QtCore.Qt.Key_Right:
            self.onRight()
        elif event.key() == QtCore.Qt.Key_PageUp:
            self.onPre()
        elif event.key() == QtCore.Qt.Key_PageDown:
            self.onNxt()

    # 重载方法mousePressEvent(self,event),即鼠标点击事件方法
    # ----------------------------------------------------------------------
    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:
            self.onRClick(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLClick(event.pos())

    # 重载方法mouseReleaseEvent(self,event),即鼠标点击事件方法
    # ----------------------------------------------------------------------
    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:
            self.onRRelease(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLRelease(event.pos())
        self.releaseMouse()

    # 重载方法wheelEvent(self,event),即滚轮事件方法
    # ----------------------------------------------------------------------
    def wheelEvent(self, event):

        if event.delta() > 0:
            self.onUp()
        else:
            self.onDown()

    # 重载方法dragMoveEvent(self,event),即拖动事件方法
    # ----------------------------------------------------------------------
    def paintEvent(self, event):
        self.onPaint()

    # PgDown键
    # ----------------------------------------------------------------------
    def onNxt(self):
        pass

    # PgUp键
    # ----------------------------------------------------------------------
    def onPre(self):
        pass

    # 向上键和滚轮向上
    # ----------------------------------------------------------------------
    def onUp(self):
        pass

    # 向下键和滚轮向下
    # ----------------------------------------------------------------------
    def onDown(self):
        pass

    # 向左键
    # ----------------------------------------------------------------------
    def onLeft(self):
        pass

    # 向右键
    # ----------------------------------------------------------------------
    def onRight(self):
        pass

    # 鼠标左单击
    # ----------------------------------------------------------------------
    def onLClick(self, pos):
        pass

    # 鼠标右单击
    # ----------------------------------------------------------------------
    def onRClick(self, pos):
        pass

    # 鼠标左释放
    # ----------------------------------------------------------------------
    def onLRelease(self, pos):
        pass

    # 鼠标右释放
    # ----------------------------------------------------------------------
    def onRRelease(self, pos):
        pass

    # 画图
    # ----------------------------------------------------------------------
    def onPaint(self):
        pass
########################################################################
# 时间序列，横坐标支持
########################################################################
class MyStringAxis(pg.AxisItem):
    """时间序列横坐标支持"""

    # 初始化
    # ----------------------------------------------------------------------
    def __init__(self, xdict, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self.minVal = 0
        self.maxVal = 0
        self.xdict = xdict
        self.x_values = np.asarray(xdict.keys())
        self.x_strings = xdict.values()
        self.setPen(color=(255, 255, 255, 255), width=0.8)
        self.setStyle(tickFont=QFont("Roman times", 10, QFont.Bold), autoExpandTextSpace=True)

    # 更新坐标映射表
    # ----------------------------------------------------------------------
    def update_xdict(self, xdict):
        self.xdict.update(xdict)
        self.x_values = np.asarray(self.xdict.keys())
        self.x_strings = self.xdict.values()
        # print(self.x_strings)

    # 将原始横坐标转换为时间字符串,第一个坐标包含日期
    # ----------------------------------------------------------------------
    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            vs = v * scale
            if vs in self.x_values:
                vstr = self.x_strings[np.abs(self.x_values - vs).argmin()]
                if (isinstance(vstr, (str))):
                    vstr = vstr
                else:
                    vstr = vstr.strftime('%Y-%m-%d %H:%M:%S')
            else:
                vstr = ""
            strings.append(vstr)
        return strings
########################################################################
# 选择缩放功能支持
########################################################################
class CustomViewBox(pg.ViewBox):
    # ----------------------------------------------------------------------
    def __init__(self, parent, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.parent = parent
        # 拖动放大模式
        # self.setMouseMode(self.RectMode)

    ## 右键自适应
    # ----------------------------------------------------------------------
    def mouseClickEvent(self, ev):

        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()

    # 重载方法mousePressEvent(self,event),即鼠标点击事件方法
    # ----------------------------------------------------------------------
    def mousePressEvent(self, event):

        pg.ViewBox.mousePressEvent(self, event)

    # 重载方法mouseDragEvent(self,event),即拖动事件方法
    def mouseDragEvent(self, ev, axis=None):
        # if ev.start==True and ev.finish==False: ##判断拖拽事件是否结束
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos

        rect = self.sceneBoundingRect()

        pianyi = dif.x() * self.parent.countK * 2 / rect.width()

        self.parent.index -= int(pianyi)
        self.parent.index = max(self.parent.index, 60)
        xMax = self.parent.index + self.parent.countK  ##
        xMin = self.parent.index - self.parent.countK
        if xMin < 0:
            xMin = 0

        # self.parent.plotAll(False, xMin, xMax) #注释原因：拖动事件不需要先绘制图形界面

        pg.ViewBox.mouseDragEvent(self, ev, axis)
    # ## 重载方法resizeEvent(self, ev)

    def resizeEvent(self, ev):
        self.linkedXChanged()
        self.linkedYChanged()
        self.updateAutoRange()
        self.updateViewRange()
        self._matrixNeedsUpdate = True
        self.sigStateChanged.emit(self)
        self.background.setRect(self.rect())
        self.sigResized.emit(self)
        self.parent.refreshHeight()
########################################################################
# K线图形对象
########################################################################
class CandlestickItem(pg.GraphicsObject):
    """K线图形对象"""

    # 初始化
    # ----------------------------------------------------------------------
    def __init__(self, data):

        """初始化"""
        pg.GraphicsObject.__init__(self)

        # 数据格式: [ (time, open, close, low, high),...]
        self.data = data
        # 只重画部分图形，大大提高界面更新速度
        self.setFlag(self.ItemUsesExtendedStyleOption)
        # 画笔和画刷
        w = 0.4
        self.offset = 0
        self.low = 0
        self.high = 1
        self.pictures = []
        self.new_lines_low=[]
        self.new_lines_high=[]
        self.bPen = pg.mkPen(color=(0, 240, 240, 255), width=w * 2)
        self.bBrush = pg.mkBrush((0, 240, 240, 255))
        self.rPen = pg.mkPen(color=(255, 60, 60, 255), width=w * 2)
        self.rBrush = pg.mkBrush((255, 60, 60, 255))
        self.new_pictures = {}
        self.flag = False
        # self.rBrush.setStyle(pg.Qt.NoBrush)
        # 刷新K线
        self.generatePicture(self.data)


    # 画K线
    # ----------------------------------------------------------------------
    def generatePicture(self, data=None, redraw=False):
        """重新生成图形对象"""
        # 重画或者只更新最后一个K线
        if redraw:
            self.pictures = []
        elif self.pictures:
            self.pictures.pop()
        w = 0.4
        bPen = self.bPen
        bBrush = self.bBrush
        rPen = self.rPen
        rBrush = self.rBrush
        low, high = (data[0]['low'], data[0]['high']) if len(data) > 0 else (0, 1)
        prehigh= 0
        prelow =0

        # '''
        for (t, open0, close0, low0, high0) in data:
            if t >= len(self.pictures):
                tShift = t

                low, high = (min(low, low0), max(high, high0))
                picture = QtGui.QPicture()
                p = QtGui.QPainter(picture)
                # # 下跌蓝色（实心）, 上涨红色（空心）
                pen, brush, pmin, pmax = (bPen, bBrush, close0, open0) \
                    if open0 > close0 else (rPen, rBrush, open0, close0)
                p.setPen(pen)
                p.setBrush(brush)
                # 画K线方块和上下影线
                if pmin > low0:
                    p.drawLine(QtCore.QPointF(tShift, low0), QtCore.QPointF(tShift, pmin))
                if high0 > pmax:
                    p.drawLine(QtCore.QPointF(tShift, pmax), QtCore.QPointF(tShift, high0))
                # 指定图片绘制的区域 QRect,画方块
                p.drawRect(QtCore.QRectF(tShift - w, open0, w * 2, close0 - open0))
                if self.flag:
                    p.setPen(pg.mkPen('w'))
                    p.setBrush(pg.mkBrush('w'))
                    if prehigh==0:
                        p.drawLine(QtCore.QPointF(t, high0+5), QtCore.QPointF(t, high0+5))
                    else:
                        p.drawLine(QtCore.QPointF(t-1, prehigh), QtCore.QPointF(t, high0+5))
                    prehigh = high0+5

                    p.setPen(pg.mkPen(color=(255,215,0)))
                    if prelow == 0:
                        p.drawLine(QtCore.QPointF(t, low0-3), QtCore.QPointF(t, low0-3))
                    else:
                        p.drawLine(QtCore.QPointF(t - 1, prelow), QtCore.QPointF(t, low0-3))
                    prelow = low0-3


                p.end()
                self.pictures.append(picture)
                self.new_pictures[t] = p

        # '''
        # prehigh= 0
        # prelow = 0
        # t = 0
        # for (t, open0, close0, low0, high0) in data:
        #     p = self.new_pictures[t]
        #     p.setPen(pg.mkPen('w'))
        #     p.setBrush(pg.mkBrush('w'))
        #     if prehigh==0:
        #         p.drawLine(QtCore.QPointF(t, high0), QtCore.QPointF(t, high0))
        #     else:
        #         p.drawLine(QtCore.QPointF(t-1, prehigh), QtCore.QPointF(t, high0))
        #     prehigh = high0
        #     p.end()

        self.low, self.high = low, high

    # 手动重画
    # ----------------------------------------------------------------------
    def update(self):
        if not self.scene() is None:
            self.scene().update()

    # 自动重画
    # ----------------------------------------------------------------------
    def paint(self, p, o, w):
        rect = o.exposedRect
        # 决定此时界面显示的bar的范围，即当前大小窗口最多显示几根bar，就画这几根bar的图形
        xmin, xmax = (max(0, int(rect.left())), min(len(self.pictures), int(rect.right())))

        [p.drawPicture(0, 0, pic) for pic in self.pictures[xmin:xmax]]
        # p.drawPicture(0, 0, self.picture)
        # print(len(self.pictures))
        # print(len(self.new_lines_high))
        # [p.drawPicture(0, 0, pic) for pic in self.new_lines_high[xmin:xmax]]



    # 定义边界
    # ----------------------------------------------------------------------
    def boundingRect(self):
        return QtCore.QRectF(0, self.low, len(self.pictures), (self.high - self.low))

class MainUi(KeyWraper):

    # 保存K线数据的列表和Numpy Array对象
    listBar = []
    listVol = []
    listHigh = []
    listLow = []
    listSig = []
    listOpenInterest = []
    arrows = []

    # 是否完成了历史数据的读取
    initCompleted = False

    def __init__(self,parent=None, name=None,datas=None):
        """Constructor"""
        self.parent = parent
        self.name = name
        super(MainUi, self).__init__(parent)

        # 当前序号
        self.index = None  # 下标
        self.countK = 60  # 显示的Ｋ线范围
        self.oldsize = 0  # rectd的hieght

        # 缓存数据

        self.datas = []
        self.listBar = []
        self.listVol = []
        self.listHigh = []
        self.listLow = []
        self.listSig = []
        self.listOpenInterest = []
        self.arrows = []
        self.sars = []

        # 所有K线上信号图
        self.allColor = deque(['blue', 'green', 'yellow', 'white'])
        self.sigData = {}
        self.sigColor = {}
        self.sigPlots = {}

        # 初始化完成
        self.initCompleted = False

        # 调用函数
        self.initUi(datas)

        '''     
        super().__init__()
        self.setWindowTitle("州的先生zmister.com A股股票历史走势K线图")
        self.main_widget = QtWidgets.QWidget() # 创建一个主部件
        self.main_layout = QtWidgets.QGridLayout() # 创建一个网格布局
        self.main_widget.setLayout(self.main_layout) # 设置主部件的布局为网格
        self.setCentralWidget(self.main_widget) # 设置窗口默认部件

        self.stock_code = QtWidgets.QLineEdit() # 创建一个文本输入框部件
        self.option_sel = QtWidgets.QComboBox() # 创建一个下拉框部件
        self.option_sel.addItem("近7天")
        self.option_sel.addItem("近30天")
        self.option_sel.addItem("近60天")
        self.option_sel.addItem("近180天")
        self.option_sel.addItem("近360天")
        self.que_btn = QtWidgets.QPushButton("查询") # 创建一个按钮部件
        self.k_widget = QtWidgets.QWidget() # 实例化一个widget部件作为K线图部件
        self.k_layout = QtWidgets.QGridLayout() # 实例化一个网格布局层
        self.k_widget.setLayout(self.k_layout) # 设置K线图部件的布局层
        self.k_plt = pg.PlotWidget() # 实例化一个绘图部件
        self.k_layout.addWidget(self.k_plt) # 添加绘图部件到K线图部件的网格布局层

        # 将上述部件添加到布局层中
        self.main_layout.addWidget(self.stock_code,0,0,1,1)
        self.main_layout.addWidget(self.option_sel,0,1,1,1)
        self.main_layout.addWidget(self.que_btn,0,2,1,1)
        self.main_layout.addWidget(self.k_widget,1,0,3,3)

        self.plot_k_line()

        # self.que_btn.clicked.connect(self.query_slot)  # 绑定按钮点击信号
        '''

    def initUi(self,datas):
        """初始化界面"""
        self.setWindowTitle(u'K线工具')
        # 主图,只能添加item
        self.pw = pg.PlotWidget()
        # 界面布局
        self.lay_KL = pg.GraphicsLayout(border=(100, 100, 100))
        self.lay_KL.setContentsMargins(10, 10, 10, 10)
        self.lay_KL.setSpacing(0)
        self.lay_KL.setBorder(color=(255, 255, 255, 255), width=0.8) # 设置边框颜色和线段粗细
        self.lay_KL.setZValue(0)
        self.lay_KL.setMinimumHeight(140)
        # self.KLtitle = self.lay_KL.addLabel(u'')
        self.pw.setCentralItem(self.lay_KL)
        # 设置横坐标
        xdict = {}
        self.axisTime = MyStringAxis(xdict, orientation='bottom')
        # 初始化子图
        self.initplotKline()
        # self.initplotOI()
        # 注册十字光标
        # self.crosshair = Crosshair(self.pw, self)

        # 设置界面，可以添加其他的例如文本框，下拉菜单项之类的
        self.vb = QtWidgets.QVBoxLayout()
        self.vb.addWidget(self.pw)
        self.setLayout(self.vb)
        # 初始化完成
        self.initCompleted = True
        self.oldsize=self.rect().height()
        self.customBox = {}

    def makePI(self, name):
        """生成PlotItem对象"""
        # vb = CustomViewBox(self)
        # plotItem = pg.PlotItem(viewBox=vb,name=name)
        plotItem = pg.PlotItem(name=name)
        plotItem.setMenuEnabled(False)
        plotItem.setClipToView(True)
        plotItem.hideAxis('left')
        plotItem.showAxis('right')
        plotItem.setDownsampling(mode='peak')
        plotItem.setRange(xRange=(0, 1), yRange=(0, 1))
        plotItem.getAxis('right').setWidth(60)
        plotItem.getAxis('right').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        plotItem.getAxis('right').setPen(color=(255, 255, 255, 255), width=0.8)
        plotItem.showGrid(True, True)
        plotItem.hideButtons()
        # plotItem.setMinimumHeight(50)

        return plotItem
    # ----------------------------------------------------------------------
    def initplotKline(self):
        """初始化K线子图"""
        self.pwKL = self.makePI('PlotKL' + self.name)
        self.candle = CandlestickItem(self.listBar)
        self.pwKL.addItem(self.candle)
        self.pwKL.setXLink('PlotOI' + self.name)
        self.pwKL.hideAxis('bottom')
        # self.lay_KL.nextRow()
        self.lay_KL.addItem(self.pwKL)

    def initplotVol(self):
        """初始化成交量子图"""
        self.pwVol = self.makePI('PlotVol' + self.name)
        self.volume = CandlestickItem(self.listVol)
        self.pwVol.addItem(self.volume)
        # self.pwVol.setMaximumHeight((self.rect().height()-30)/4)
        # self.pwVol.setMinimumHeight(12)
        self.pwVol.setXLink('PlotOI' + self.name)
        self.pwVol.hideAxis('bottom')
        self.lay_KL.nextRow()
        self.lay_KL.addItem(self.pwVol)
        self.lay_KL.adjustSize()
    # ----------------------------------------------------------------------
    #  画图相关
    # ----------------------------------------------------------------------
    def plotVol(self, redraw=False, xmin=0, xmax=-1):
        """重画成交量子图"""
        if self.initCompleted:
            self.volume.generatePicture(self.listVol[xmin:xmax], redraw)  # 画成交量子图

    # ----------------------------------------------------------------------
    def plotKline(self, redraw=False, xmin=0, xmax=-1):
        """重画K线子图"""
        if self.initCompleted:
            self.candle.generatePicture(self.listBar[xmin:xmax], redraw)  # 画K线
            self.plotMark()  # 显示开平仓信号位置


    # ----------------------------------------------------------------------
    def plotAll(self, redraw=True, xMin=0, xMax=-1):
        """
        重画所有界面
        redraw ：False=重画最后一根K线; True=重画所有
        xMin,xMax : 数据范围
        """
        # xMax = len(self.datas) if xMax < 0 else xMax
        # self.countK = xMax-xMin
        # self.index = int((xMax+xMin)/2)
        if redraw:
            xmax = len(self.datas) if xMax < 0 else xMax
            xmin=max(0,xmax-self.countK)
            self.index = int((xmax + xmin) / 2)
        # self.pwOI.setLimits(xMin=xMin, xMax=xMax)
        self.pwKL.setLimits(xMin=xMin, xMax=xMax)
        # self.pwVol.setLimits(xMin=xMin, xMax=xMax)
        self.plotKline(redraw, xMin, xMax)  # K线图
        # self.plotVol(redraw, xMin, xMax)  # K线副图，成交量
        # self.plotOI(0, len(self.datas))  # K线副图，持仓量
        self.refresh()

    def plotMark(self):
        """显示开平仓信号"""
        # 检查是否有数据
        # if len(self.datas) == 0:
        #     return
        # for arrow in self.arrows:
        #     self.pwKL.removeItem(arrow)
        # # 画买卖信号
        # for i in range(len(self.listSig)):
        #     # 无信号
        #     if self.listSig[i] == None:
        #         continue
        #     # 买信号
        #     elif self.listSig[i] != None:
                # direction = self.listSig[i]["direction"]
                # offset = self.listSig[i]["offset"]
                # price = self.listSig[i]["price"]

                # if direction == "空" and offset == "开仓":
                    # arrow = pg.ArrowItem(pos=(i, price),  angle=-90, brush=(255, 0, 0))
                # arrow = pg.ArrowItem(pos=(i, 20+i), angle=180, tipAngle=60, headLen=8, tailLen=3, tailWidth=5,
                #                      pen={'color': 'w', 'width': 1}, brush='r')
                # elif direction == "多" and offset == "开仓":
                #     # arrow = pg.ArrowItem(pos=(i, price),  angle=90, brush=(255, 0, 0))
                #     arrow = pg.ArrowItem(pos=(i, price), angle=180, tipAngle=60, headLen=8, tailLen=3, tailWidth=5,
                #                          pen={'color': 'w', 'width': 1}, brush='b')
                # elif direction == "空" and offset == "平仓":
                #     # arrow = pg.ArrowItem(pos=(i, price),  angle=-90, brush=(0, 0, 255))
                #     arrow = pg.ArrowItem(pos=(i, price), angle=0, tipAngle=40, headLen=8, tailLen=None, tailWidth=8,
                #                          pen={'color': 'w', 'width': 1}, brush='y')
                # elif direction == "多" and offset == "平仓":
                #     # arrow = pg.ArrowItem(pos=(i, price),  angle=90, brush=(0, 0, 255))
                #     arrow = pg.ArrowItem(pos=(i, price), angle=0, tipAngle=40, headLen=8, tailLen=None, tailWidth=8,
                #                          pen={'color': 'w', 'width': 1}, brush='y')
        arrow = pg.ArrowItem(pos=(len(self.datas)-3,30 ), angle=90, tipAngle=60, headLen=8, tailLen=3, tailWidth=5,
                             pen={'color': 'w', 'width': 1}, brush='r')
        self.pwKL.addItem(arrow)
        self.arrows.append(arrow)

    def updateSig(self, sig):
        """刷新买卖信号"""
        self.listSig = sig
        self.plotMark()

    def refresh(self):
        """
        刷新三个子图的显示范围
        """
        datas = self.datas
        minutes = int(self.countK / 2)
        print(minutes)
        xmin = max(0, self.index - minutes)
        xmax = xmin + 2 * minutes
        # self.pwOI.setRange(xRange=(xmin, xmax))
        self.pwKL.setRange(xRange=(xmin, xmax))
        # self.pwVol.setRange(xRange=(xmin, xmax))

    def resignData(self, datas):
        """更新数据，用于Y坐标自适应"""
        # self.crosshair.datas = datas

        def viewXRangeChanged(low, high, self):
            vRange = self.viewRange()
            xmin = max(0, int(vRange[0][0]))
            xmax = max(0, int(vRange[0][1]))
            xmax = min(xmax, len(datas))
            if len(datas) > 0 and xmax > xmin:
                ymin = min(datas[xmin:xmax][low])
                ymax = max(datas[xmin:xmax][high])
                if ymin and ymax:
                   self.setRange(yRange=(ymin, ymax))
            else:
                self.setRange(yRange=(0, 1))

        view = self.pwKL.getViewBox()
        view.sigXRangeChanged.connect(partial(viewXRangeChanged, 'low', 'high'))

        # view = self.pwVol.getViewBox()
        # view.sigXRangeChanged.connect(partial(viewXRangeChanged, 'volume', 'volume'))
        #
        # view = self.pwOI.getViewBox()
        # view.sigXRangeChanged.connect(partial(viewXRangeChanged, 'openInterest', 'openInterest'))
    def loadData(self, datas):
        """
        载入pandas.DataFrame数据
        datas : 数据格式，cols : datetime, open, close, low, high
        """
        # 设置中心点时间
        self.index = 0

        # 绑定数据，更新横坐标映射，更新Y轴自适应函数，更新十字光标映射
        datas['time_int'] = np.array(range(len(datas.index)))
        self.datas = datas[['open', 'close', 'low', 'high', 'volume', 'openInterest']].to_records()
        self.axisTime.xdict = {}
        xdict = dict(enumerate(datas['datetime'].tolist()))
        self.axisTime.update_xdict(xdict)
        self.resignData(self.datas)
        # 更新画图用到的数据
        self.listBar = datas[['time_int', 'open', 'close', 'low', 'high']].to_records(False)
        self.listHigh = list(datas['high'])
        self.listLow = list(datas['low'])
        self.listOpenInterest = list(datas['openInterest'])
        # 成交量颜色和涨跌同步，K线方向由涨跌决定
        '''
        datas0 = pd.DataFrame()
        datas0['open'] = datas.apply(lambda x: 0 if x['close'] >= x['open'] else x['volume'], axis=1)
        datas0['close'] = datas.apply(lambda x: 0 if x['close'] < x['open'] else x['volume'], axis=1)
        datas0['low'] = datas0['open']
        datas0['high'] = datas0['close']
        datas0['time_int'] = np.array(range(len(datas.index)))
        self.listVol = datas0[['time_int', 'open', 'close', 'low', 'high']].to_records(False)
        '''
        self.plotAll(True, 0, len(self.datas))



def get_datas(s):
    init('a', s)
    symbol = '002192'
    exchange = Exchange('SZ')
    day = Interval.DAILY
    start = datetime(2019, 1, 1)
    end = datetime(2019, 6, 3)

    data = MongoManager()
    datas = data.load_bar_data(symbol, exchange, day, start, end)
    bars = pd.DataFrame(columns=['open', 'close', 'low', 'high', 'volume', 'openInterest'])
    opens = [data.open_price for data in datas]
    closes = [data.close_price for data in datas]
    low = [data.low_price for data in datas]
    high = [data.high_price for data in datas]
    volume = [data.volume for data in datas]
    datetimes=[data.datetime for data in datas]
    bars['open'] = opens
    bars['close'] = closes
    bars['low'] = low
    bars['high'] = high
    bars['volume'] = volume
    bars['openInterest'] = 0
    bars['datetime'] = datetimes
    return bars




if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    s = Settings()
    timer = QtCore.QTimer()

    datas = get_datas(s)
    main_widget = MainUi(name="opt",datas=datas)
    main_widget.show()
    # main_widget.updateSig('test')

    # main_widget.loadData(datas)
    # main_widget.plotAll(True,)
    # main_widget.candle.flag = True
    # main_widget.plotAll(True, 0, len(datas))
    sys.exit(app.exec_())
