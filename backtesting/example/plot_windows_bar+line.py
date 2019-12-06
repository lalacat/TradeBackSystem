from datetime import datetime

from PyQt5 import QtCore, QtGui,QtWidgets

from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from chart import VolumeItem, ChartWidget, CandleItem
from settings.setting import Settings
from ui import create_qapp
import pyqtgraph as pg

app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

## Create some widgets to be placed inside
btn = QtGui.QPushButton('press me')
text = QtGui.QLineEdit('enter text')
listw = QtGui.QListWidget()
plot = pg.PlotWidget()

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)






s = Settings()
# app = create_qapp(s)

database_manager = init('_',s)

bars = database_manager.load_bar_data(
        "002192",
        Exchange.SZ,
        interval=Interval.DAILY,
        start=datetime(2015, 1, 1),
        end=datetime(2019, 9, 18)
)

widget = ChartWidget()
widget.add_plot("candle", hide_x_axis=False)
widget.add_plot("volume", hide_x_axis=False)
widget.add_item(CandleItem, "candle", "candle")
widget.add_item(VolumeItem, "volume", "volume")
widget.add_cursor()


new_data = bars[:]

widget.update_history(bars)


def update_bar():
    bar = new_data.pop(0)
    widget.update_bar(bar)


## Add widgets to the layout in their proper positions
layout.addWidget(btn, 0, 0)   # button goes in upper-left
layout.addWidget(text, 1, 0)   # text edit goes in middle-left
layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
layout.addWidget(widget, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()


## Start the Qt event loop
app.exec_()



#
# widget.show()
#
#
#
# app.exec_()
