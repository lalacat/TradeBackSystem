import tushare as ts
from datetime import datetime

from scipy import  stats
from statsmodels.stats import anova

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols


# token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'
# pro = ts.pro_api(token)
# df = pro.index_basic(market='SSE')
s = Settings()

dbm = init('_',s)
start = datetime(2018, 9, 1)
end = datetime(2019, 9, 30)
RJ = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start, end
)
RJ_returns = RJ.close_price.pct_change().dropna()
RJ['return'] = RJ_returns
print(RJ.head(5))
# model = ols('return ~ C(volume)',data=RJ.dropna()).fit()
#
# table = anova.anova_lm(model)
# print(table)