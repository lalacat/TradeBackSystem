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
CSV,index
'''

s = Settings()

dbm = init('_',s)
start = datetime(2020, 1, 1)
end = datetime(2020, 5, 20)
codes = pd.read_csv('resultCoint.csv',index_col=[0])
nameX,nameY = codes.iloc[0].name.split(':')
print(nameX)
print(nameY)
def get_closeprice(codes,start,end):
    code,exchange = codes.split('.')
    price = dbm.load_bar_dataframe_data(
        code,Exchange(exchange), Interval.DAILY, start, end
        )
    return price['close_price']
# 整合bank的收盘价
# for index, codes in codes.iterrows():
#     code,exchange = codes[1].split('.')
#     result = dbm.load_bar_dataframe_data(
#         code,Exchange(exchange), Interval.DAILY, start, end
#         )
#     result_name.append(code)
#     result_list.append(result['close_price'])
# all_banks = pd.concat(result_list,axis=1,keys=result_name)
# fill_banks = all_banks.dropna()
# st = PairTrading()

