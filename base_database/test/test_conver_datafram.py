import pandas as pd
from datetime import datetime

from backtesting.Indicator.test_plotitem import ChartLineWidget
from base_database.initialize import database_manager
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
from ui import create_qapp

s = Settings()

start = datetime(2018, 9, 1)
end = datetime(2019, 9, 18)

RJ = database_manager.load_bar_data(
        '002192',Exchange.SZ , Interval.DAILY, start, end)


# result= None
#
# for bar in RJ:
#     if result is None:
#         result =pd.DataFrame(
#             {
#                 'open_price':bar.open_price,
#                 'close_price':bar.close_price,
#                 'high_price':bar.high_price,
#                 'low_price':bar.low_price,
#                 'volume':bar.volume
#             },
#             index = [bar.datetime]
#         )
#     else:
#         result = result.append(pd.DataFrame(
#             {
#                 'open_price':bar.open_price,
#                 'close_price':bar.close_price,
#                 'high_price':bar.high_price,
#                 'low_price':bar.low_price,
#                 'volume':bar.volume
#             },
#             index = [bar.datetime]
#         ))
# print(result)

RJ_new = database_manager.load_bar_dataframe_data(
        '002192',Exchange.SZ , Interval.DAILY, start, end)
RJ_new = RJ_new.sort_index()

# if isinstance(RJ_new.index, pd.DatetimeIndex):
#     print(type(RJ_new.index))
#     l = range(len(RJ_new))
#     b = dict(zip(l,RJ_new.index))
#     if isinstance(RJ_new.index[0],datetime):
#         print('datetime')
#     new_df = RJ_new[0:5]
#     print(new_df)
#     maxs= new_df.max()
#     print(maxs)
#     print(maxs.max())
#
#     for name, value in maxs.items():
#         print(name)
#     print(type(new_df.max()))
#
# df1 = pd.DataFrame([['Snow','M',22],['Tyrion','M',32],['Sansa','F',18],['Arya','F',14]], columns=['name','gender','age'])
# print(len(df1.columns))

ix = range(len(RJ_new))
for _,data in zip(ix,RJ_new.iterrows()):
    # print(ix)
    # print(_)
    for n,v in data[1].items():
        print(v)



# minvalue = RJ_new['close_price'][1:4].min()
# print(minvalue)
#
# print(RJ_new.loc[RJ_new.index[253]]['close_price'])
# print(RJ_new['close_price'][253])

# print(RJ_new)
#
# print(RJ_new['close_price'].max())


# app = create_qapp(s)
# w = ChartLineWidget(RJ_new)
# w.add_plot()
# w.show()
#
# app.exec_()