# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:27:12 2019
#请把token换成你自己的，不然刷新后可能用不了
@author: zjy
"""
import sqlite3

from sqlalchemy import create_engine

# filename='sqlite:///X:\\股票\\db_stock\\'
# filename = 'C:\\Users\\scott\\Documents\\学习文档\\stock_db' + '\\'
# filename = 'W:\\stock_db'+ '\\'
filename = 'X:\\股票'+ '\\'
db_name='stock_data.db'

def sql_engine(file=filename,db=db_name):
    # path=file+db

    engine = sqlite3.connect(filename + db)
    return engine

def ts_pro():
    import tushare as ts 
    token='e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d'
    pro=ts.pro_api(token)
    return pro

def ts():
    import tushare as ts
    token = 'e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d'
    ts.set_token(token)
    return ts
    