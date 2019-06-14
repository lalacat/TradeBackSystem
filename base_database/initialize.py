from base_database.database import BaseDatabaseManager, Driver
from base_database.database_mongo import init
from settings.setting import Settings




# def init(settings: dict) -> BaseDatabaseManager:
#     driver = Driver(settings["driver"])
#     if driver is Driver.MONGODB:
#         return init_nosql(driver=driver, settings=settings)
#     # else:
#     #     return init_sql(driver=driver, settings=settings)
#
#
# def init_nosql(driver: Driver, settings: dict):
#     from .database_mongo import init
#     _database_manager = init(driver, settings=settings)
#     return _database_manager


settings = Settings()
database_manager: "BaseDatabaseManager" = init('_',settings=settings)