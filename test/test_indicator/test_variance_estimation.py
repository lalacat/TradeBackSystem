import pprint
from datetime import datetime, timedelta

from chinese_calendar import is_holiday

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import pandas as pd


s = Settings()
dbm = init('_',s)


# 获得一年的周
start_day = datetime(2019, 1, 1)
end_day = datetime(2019, 12, 9)
result = {}
number = 0


def get_tradingday(start_day,end_day):
    start_week = start_day.isoweekday()
    days = []
    end = False
    global number
    for day in range(6-start_week):
        t = start_day+timedelta(days=day)
        if t == end_day:
            end = True
            day =  6 - start_week - 1
        if t.isoweekday() < 6:
            if not is_holiday(t):
                days.append(t)
        if day == 6 - start_week - 1:
            if days:
                result[str(number)] = days
                number = number + 1
            if end:
                break
            next_weekday = t + timedelta(days=3)
            get_tradingday(next_weekday,end_day)

get_tradingday(start_day,end_day)


rj = dbm.load_bar_dataframe_data(
'002192',Exchange.SZ , Interval.DAILY, start_day, end_day
)


print(rj['close_price'].pct_change().dropna().std())

std_results = pd.DataFrame()
for week_num in result.keys():
    # 截取每一周
    week = rj.loc[result[week_num], 'close_price']
    # print(week)
    # print(week.index[0])
    # 计算收益率和周波动率
    return_week = week.pct_change().dropna()
    # print(return_week)
    std_week = return_week.std()
    # print(std_week)
    # print(week.index)
    std_result = pd.DataFrame({'std': std_week}, index=[week.index[0]])
    if std_results.empty:
        std_results = std_result
    else:
        std_results = pd.concat([std_results,std_result],axis=0)

print(std_results)