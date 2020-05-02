from datetime import datetime,timedelta

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
