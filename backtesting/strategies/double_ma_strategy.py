# from vnpy.app.cta_strategy import (
#     CtaTemplate,
#     StopOrder,
#     TickData,
#     BarData,
#     TradeData,
#     OrderData,
#     BarGenerator,
#     ArrayManager,
# )
from collections import defaultdict

from backtesting.template import CtaTemplate
from base_utils.base import StopOrder
from base_utils.object import BarData, OrderData, TradeData
from base_utils.utility import BarGenerator, ArrayManager
from chart import ChartWidget, CandleItem, VolumeItem


class DoubleMaStrategy(CtaTemplate):
    author = "用Python的交易员"

    fast_window = 10
    slow_window = 20

    fast_ma0 = 0.0
    fast_ma1 = 0.0

    slow_ma0 = 0.0
    slow_ma1 = 0.0

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(DoubleMaStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

        self.addition_line = defaultdict(dict)
        self.trade_orders = defaultdict(list)
        self.ups={}
        self.downs={}
        self.mids={}
        self.mids={}
        self.bars=list()
        self.bar_opens=[]
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")
        print("策略停止")
        self.addition_line['up'] = self.ups
        self.addition_line['down'] = self.downs
        widget = ChartWidget()
        widget.add_plot("candle", hide_x_axis=False)
        widget.add_item(CandleItem, "candle", "candle")
        widget.add_plot("volume")
        widget.add_item(VolumeItem, "volume", "volume")
        widget.add_cursor()
        widget.update_history(self.bars, self.addition_line, self.trade_orders)
        # widget.update_history(self.bars,tradeorders=self.trade_orders)
        widget.show()
        self.put_event()

    # def on_tick(self, tick: TickData):
    #     """
    #     Callback of new tick data update.
    #     """
    #     self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        fast_ma = am.sma(self.fast_window, array=True)
        # self.ups.
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]

        slow_ma = am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1


        if cross_over:
            if self.pos == 0:
                self.buy(bar.close_price, 1)

        elif cross_below:
            if  self.pos > 0:
                self.sell(bar.close_price, 1)

        """
        if cross_over:
            if self.pos == 0:
                self.buy(bar.close_price, 1)
            elif self.pos < 0:
                self.cover(bar.close_price, 1)
                self.buy(bar.close_price, 1)

        elif cross_below:
            if self.pos == 0:
                self.short(bar.close_price, 1)
            elif self.pos > 0:
                self.sell(bar.close_price, 1)
                self.short(bar.close_price, 1)
     
        """
        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
