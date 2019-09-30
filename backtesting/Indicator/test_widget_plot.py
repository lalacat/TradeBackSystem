
from datetime import datetime

from PyQt5 import QtCore, QtGui,QtWidgets

from base_database.database_mongo import init
from base_utils.constant import Exchange, Interval
from chart import VolumeItem, ChartWidget, CandleItem
from chart.item import LineItem
from chart.manager import LineManager
from settings.setting import Settings
from ui import create_qapp

s = Settings()
app = create_qapp(s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 18)


database_manager = init('_',s)
RJ_new = database_manager.load_bar_dataframe_data(
        '002192',Exchange.SZ , Interval.DAILY, start, end)
RJ_new = RJ_new.sort_index()

widget = ChartWidget(manager=LineManager)
# widget.add_plot("candle", hide_x_axis=False)
widget.add_plot("line", hide_x_axis=False)
# widget.add_item(CandleItem, "candle", "candle")
widget.add_item(LineItem, "line", "line")
# widget.add_cursor()


# new_data = bars[:]

widget.update_history(RJ_new)



# timer = QtCore.QTimer()
# timer.timeout.connect(update_bar)
# timer.start(100)

widget.show()



app.exec_()
