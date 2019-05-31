from base_database.database_mongo import init, Test, Task_anshan
from settings.setting import Settings

s = Settings()
init('a',s)
#
# a = Test(
#     sold_unitPrice='10000',
#     sold_address = '20000',
#     community_name = 'Test'
#          )
# a.save()
# c = Task_anshan(
#     community_name='10000',
#     community_url = '20000',
#     community_sale_num = ['Test']
#          )
# c.save()
# names  = c._get_collection_name()
# print(names)

b = Task_anshan.objects(community_name='鞍山一村')
print(b[0].to_print())
