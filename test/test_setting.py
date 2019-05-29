from base_database.database import Driver
from settings.setting import Setting, BaseSettings

s = Setting()

# print(s)
#
# for i,j in s:
#     # print(i,j)
#     if isinstance(j,BaseSettings):
#         for p,q in j:
#             print(p,q)
#             print(type(q))
driver = Driver(s['DRIVER'])

a = driver is Driver.MONGODB
print(a)