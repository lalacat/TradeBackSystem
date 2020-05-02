from datetime import datetime

from backtesting.backtesting import BacktestingEngine
from backtesting.strategies.double_ma_strategy import DoubleMaStrategy
from settings.setting import Settings
from ui import create_qapp

setting = {}  # ATR窗口

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="002192.SZ",
    interval="d", # 数据库读取数据
    start=datetime(2015, 9, 1),
    end=datetime(2019, 12, 26),
    rate=0,
    slippage=0,
    size=100,
    pricetick=0.01,
    capital=1_000_000,
)



# 加载策略
# engine.initStrategy(TurtleTradingStrategy, setting)
engine.add_strategy(DoubleMaStrategy, setting)
engine.load_data()
engine.run_backtesting()
engine.calculate_result()
result = engine.calculate_statistics(Output=False)
# engine.show_chart()
df = engine.daily_df

# pw = pg.plot(title='pyqtgraph.plot()')
# pw.plot(df["balance"])  # 绘制第一个图

# widget = engine.strategy.widget
# chart = engine.get_fig()
s = Settings()
app = create_qapp(s)
app.exec_()

# print(pprint(result))