from datetime import datetime,timedelta

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