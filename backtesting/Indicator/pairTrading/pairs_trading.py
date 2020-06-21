import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from backtesting.Indicator.pairTrading.PairTrading import PairTrading
from backtesting.example.measure.annualize_return import getReturn
from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
from itertools import combinations
'''

读CSV文件
获取Code
NAN值填充
最小距离法筛选两只股票
排列组合
'''
s = Settings()

dbm = init('_',s)
start = datetime(2019, 1, 1)
end = datetime(2020, 4, 24)
bank_path = s['PATH_BANK']
# delta = end - start
# print(delta)
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
    result_name.append(code)
    result_list.append(result['close_price'])
all_banks = pd.concat(result_list,axis=1,keys=result_name)
# fill_banks = all_banks.fillna(method='bfill')
fill_banks = all_banks.dropna()
# print(fill_banks)
# all_com = [c for c in combinations(fill_banks.columns,2)]
# print(len(all_com))
# print(all_com)

#
# # 计算最小距离
# def SSD(priceX,priceY):
#     if priceX is None or priceY is None:
#         return  None
#     returnX = (priceX - priceX.shift(1))/priceX.shift(1)[1:]
#     returnY = (priceY - priceY.shift(1))/priceY.shift(1)[1:]
#     standardX = (returnX + 1).cumprod()
#     standardY = (returnY + 1).cumprod()
#     SSD = np.sum((standardX+standardY)**2)
#     return  SSD
# print(len(fill_banks))
# # print(codes)
# temp = fill_banks
# results = []
# # 两两计算ssd
# for name, value in fill_banks.iteritems():
#     name_1 = name
#     second = temp.drop([name_1],axis=1)
#     print(name_1)
#     for name,value in second.iteritems():
#         name_2 = name
#         # 选出最小距离的股票对
#         ssd = SSD(fill_banks[name_1], fill_banks[name_2])
#         results.append([name_1+':'+name_2,ssd])
#     temp = second
# results_csv = pd.DataFrame(results,columns=['name','ssd']).sort_values(by=['ssd'])
# results_csv.to_csv('banks_ssd_nan.csv',index=False)
# print(results_csv)


"""
bank_ssd = pd.read_csv('banks_ssd_nan.csv')
print(bank_ssd)
after_sort = bank_ssd.sort_values(by=['ssd'])
print(after_sort.head(5))
选出最小ssd
              name         ssd
436  601860:601077  296.716141
170  601997:601860  300.628881
48   600919:601860  302.659752
183  601997:601077  303.990073
430  601860:002936  304.446743
"""


'''
计算上下边界
'''
A = dbm.load_bar_dataframe_data(
'601860',Exchange.SH , Interval.DAILY, start, end
)

B = dbm.load_bar_dataframe_data(
'601077',Exchange.SH , Interval.DAILY, start, end
)
banks = pd.concat([A['close_price'],B['close_price']],keys=['A','B'],axis=1).dropna()
print(banks)
logA = np.log(banks['A'])
logB = np.log(banks['B'])

returnA = (logA - logA.shift(1)) / logA.shift(1)[1:]
returnB = (logB - logB.shift(1)) / logB.shift(1)[1:]
# 标准化价格
standardA = (1+returnA).cumprod()
standardB = (1+returnB).cumprod()
ssd_pair = standardB - standardA
meanSSD_pair = np.mean(ssd_pair)
stdSSD_pair = np.std(ssd_pair)



up_ssd = meanSSD_pair + 1.5*stdSSD_pair
down_ssd = meanSSD_pair - 1.5*stdSSD_pair
print(up_ssd)
print(down_ssd)

st = PairTrading()
st.setStock(logA,logB)
up_ssd,down_ssd = st.calBound('SSD')

print(up_ssd)
print(down_ssd)

ssd_pair.plot()
plt.axhline(y=meanSSD_pair,color='black')
plt.axhline(y=up_ssd,color='green')
plt.axhline(y=down_ssd,color='green')
plt.xlim((datetime(2019,11,1),datetime(2019,12,1)))
plt.show()