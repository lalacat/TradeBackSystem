from datetime import datetime,timedelta

from base_database.database import Driver
from settings.setting import Settings, BaseSettings

# s = Settings()

# print(s)
#
# for i,j in s:
#     # print(i,j)
#     if isinstance(j,BaseSettings):
#         for p,q in j:
#             print(p,q)
#             print(type(q))
# driver = Driver(s['DRIVER'])

# a = driver is Driver.MONGODB
# print(a)

end = datetime.now()
start = end - timedelta(10)
print(end)
print(start)
