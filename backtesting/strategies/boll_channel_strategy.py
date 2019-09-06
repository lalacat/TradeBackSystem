
from collections import defaultdict
from datetime import datetime

from backtesting.template import CtaTemplate
from base_utils.base import StopOrder
from base_utils.object import TickData, BarData, OrderData, TradeData
from base_utils.utility import BarGenerator, ArrayManager

import pyqtgraph as pg

from chart import ChartWidget, CandleItem
from settings.setting import Settings
from ui import create_qapp


class BollChannelStrategy(CtaTemplate):
    """"""

    author = "用Python的交易员"

    boll_window = 18
    boll_dev = 3.4
    cci_window = 10
    atr_window = 30
    sl_multiplier = 5.2
    fixed_size = 1

    boll_up = 0
    boll_down = 0
    cci_value = 0
    atr_value = 0

    intra_trade_high = 0
    intra_trade_low = 0
    long_stop = 0
    short_stop = 0

    parameters = ["boll_window", "boll_dev", "cci_window",
                  "atr_window", "sl_multiplier", "fixed_size"]
    variables = ["boll_up", "boll_down", "cci_value", "atr_value",
                 "intra_trade_high", "intra_trade_low", "long_stop", "short_stop"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(BollChannelStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )
        s = Settings()
        self.app = create_qapp(s)
        self.am = ArrayManager()
        self.addition_line = defaultdict(dict)
        self.ups={}
        self.downs={}
        self.mids={}
        self.mids={}
        self.bars=list()
        self.bar_opens=[]

    def on_init(self,size=None):
        """
        Callback when strategy is inited.
        """
        print("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        print("策略停止")
        self.addition_line['up'] = self.ups
        self.addition_line['down'] = self.downs
        self.addition_line['mid'] = self.mids
        widget = ChartWidget()
        widget.add_plot("candle", hide_x_axis=False)
        widget.add_item(CandleItem, "candle", "candle")
        widget.add_cursor()
        # widget.addItem()
        arrow = pg.ArrowItem(pos=(len(self.bars),40), angle=90, tipAngle=60, headLen=8, tailLen=3, tailWidth=5,
                             pen={'color': 'w', 'width': 1}, brush='r')
        widget.update_history(self.bars,self.addition_line)
        widget.addItem(arrow)
        widget.show()
        self.app.exec_()

        # print(self.addition_line)

        # self.write_log("策略停止")


    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)


    def on_bar(self,bar,am=None):
        """
        在run_backtesting中先初始化定义数量的数据，先在callback，默认on_bar中将数据库中的bar加入到程序中根据需要形成所需要的时间段的bar数据，
        在bg.update_bar(bar)中调用on_15min_bar方法，对形成新的bar数据加载到dataframe数据中，为后来的数据处理做准备，只有数据全部加载完后am.inited，才会生效，后续的数据计算才会继续进行
        """
        # 如果当前交易日没有成交上一个交易日策略生成的价格，则把上个交易日报的单全部取消
        self.cancel_all()
        self.bars.append(bar)

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return
        # self.bar_opens.append(bar.close_price)
        self.boll_up, self.boll_down = am.boll(self.boll_window, self.boll_dev)
        self.boll_mid = am.sma(self.boll_window)
        self.mids[bar.datetime]=self.boll_mid
        self.ups[bar.datetime] = self.boll_up
        self.downs[bar.datetime] = self.boll_down


        self.cci_value = am.cci(self.cci_window)
        self.atr_value = am.atr(self.atr_window)

        if self.pos == 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = bar.low_price

            if self.cci_value > 0:
                # 向engine中send_order
                self.buy(self.boll_up, self.fixed_size, True)
            elif self.cci_value < 0:
                self.short(self.boll_down, self.fixed_size, True)

        elif self.pos > 0:
            self.intra_trade_high = max(self.intra_trade_high, bar.high_price)
            self.intra_trade_low = bar.low_price

            self.long_stop = self.intra_trade_high - self.atr_value * self.sl_multiplier
            self.sell(self.long_stop, abs(self.pos), True)

        elif self.pos < 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = min(self.intra_trade_low, bar.low_price)

            self.short_stop = self.intra_trade_low + self.atr_value * self.sl_multiplier
            self.cover(self.short_stop, abs(self.pos), True)


        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade datooa update.
        """
        # print("已成交:%s 此时仓位为:%d手" %(trade.tradeid,self.pos))
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
