from datetime import datetime

from PyQt5 import QtCore, QtGui,QtWidgets

from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from chart import VolumeItem, CandleItem
from chart.widget_test import ChartWidget
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
        end=datetime(2019, 9, 18)
)
widget = ChartWidget()
# widget.add_plot("candle", hide_x_axis=False)
widget.add_plot("volume", hide_x_axis=False)
# widget.add_item(CandleItem, "candle", "candle")
widget.add_item(VolumeItem, "volume", "volume")
widget.add_cursor()


new_data = bars[:]

widget.update_history(bars)


def update_bar():
    bar = new_data.pop(0)
    widget.update_bar(bar)



widget.show()



app.exec_()
