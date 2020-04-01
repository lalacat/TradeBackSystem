import pprint
from datetime import datetime,timedelta,date
from chinese_calendar import is_holiday

t1 = datetime.now()
progress_delta = timedelta(days=30)
# print(type(progress_delta))

print(t1)

print(progress_delta)
t2 = datetime(2019,6,28,0,0,0)
print(t2)
t = t1 + progress_delta
print(t)
dt = t.replace(minute=0, second=0, microsecond=0)

print(dt)

# 字符串转换日期格式
start = datetime.strptime('20190101','%Y%m%d').date()
end_day = datetime.strptime('20191231','%Y%m%d').date()


print(start)
print(end_day)
print(end_day-start)
temp = start + timedelta(days=344)

a = start.strftime('%Y%m%d')
print(a)
print(temp==end_day)

# 返回星期几
start_weekday = start.isoweekday()
print(start_weekday)

result = {}
number = 1
# 获得一周的日期
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


get_tradingday(start,end_day)

# print(pprint.pformat(result))

start_urls = [
    # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191008.dat',
    # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191009.dat',
    # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191010.dat',
    # 'http://www.shfe.com.cn/data/dailydata/kx/pm20191011.dat',
    ]

for i in range(1,53):
    week = result[str(i)]
    for day in week:
        day = day.strftime('%Y%m%d')
        url ='http://www.shfe.com.cn/data/dailydata/kx/pm{0}.dat'.format(day)
        start_urls.append(url)

print(len(start_urls))
