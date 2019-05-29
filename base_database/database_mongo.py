from mongoengine import DateTimeField, Document, FloatField, StringField, connect,ListField
from pymongo.errors import OperationFailure

from base_database.database import Driver
from settings.setting import Settings

"""
使用时先声明一个继承自MongoEngine.Document的类,
在类中声明一些属性，相当于创建一个用来保存数据的数据结构,
即数据已类似数据结构的形式存入数据库中，
通常把这样的一些类都存放在一个脚本中，作为应用的Model模块
"""


def init(_:Driver,settings:Settings):
    database = settings['DATABASE_DATABASE']
    host = settings['DATABASE_HOST']
    port = settings['DATABASE_PORT']
    username = settings['DATABASE_USER']
    passwd = settings['DATABASE_PASSWORD']
    authentication_source = settings['DATABASE_AUTH']

    if not username:  # if username == '' or None, skip username
        username = None
        passwd = None
        authentication_source = None
    try:
        connect(
            db=database,
            host=host,
            port=port,
            username=username,
            password=passwd,
            authentication_source=authentication_source,
        )
    except OperationFailure:
        print('Authentication failed')

class Test(Document):
    sold_unitPrice:str = StringField()
    sold_address:str = StringField()
    community_name:str = StringField()
    # sold_dealDate:str = ListField()
    # sold_totalPrice:str = ListField()
    # sold_saleonborad:str = ListField()
    # sold_positionInfo:str = ListField()
    # sold_dealcycle:str = ListField()


class anshan(Document):
    sold_unitPrice:str = ListField()
    sold_address:str = ListField()
    community_name:str = ListField()
    sold_dealDate:str = ListField()
    sold_totalPrice:str = ListField()
    sold_saleonborad:str = ListField()
    sold_positionInfo:str = ListField()
    sold_dealcycle:str = ListField()
