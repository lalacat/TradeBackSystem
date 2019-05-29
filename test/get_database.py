from base_database.database_mongo import init, Test, anshan
from settings.setting import Settings

s = Settings()
init('a',s)

# a = Test(
#     sold_unitPrice='10000',
#     sold_address = '20000',
#     community_name = 'Test'
#          )
# a.save()
b = anshan.objects.all()
community_name = b[0].community_name
for c in community_name:
    print(c)