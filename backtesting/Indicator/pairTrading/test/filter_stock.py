from backtesting.Indicator.pairTrading.PairTrading import PairTrading
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from backtesting.Indicator.pairTrading.PairTrading import PairTrading
from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings

'''
计算一个组的最小距离
一个组的协整参数
'''

s = Settings()

dbm = init('_',s)
'''
'''
start = datetime(2019, 1, 1)
end = datetime(2020, 1, 1)
bank_path = s['PATH_BANK']
codes = pd.read_csv(bank_path)
codes.columns = ['name','code']
result_list = []
result_name = []
# 整合bank的收盘价
for index, codes in codes.iterrows():
    code,exchange = codes[1].split('.')
    result = dbm.load_bar_dataframe_data(
        code,Exchange(exchange), Interval.DAILY, start, end
        )
    result_name.append(codes[1])
    result_list.append(result['close_price'])
all_banks = pd.concat(result_list,axis=1,keys=result_name)
fill_banks = all_banks.dropna()
st = PairTrading()
# up_ssd,down_ssd = st.calBound('SSD')
# print(up_ssd)
# print(down_ssd)
st.calAllCointegration(fill_banks)
print(st.resultCoint)
print(st.resultNotCoint)
st.to_csv()
