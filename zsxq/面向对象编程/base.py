# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:27:12 2019

@author: zjy
"""

from sqlalchemy import create_engine

filename='sqlite:///c:\\zjy\\db_stock\\'
db_name='stock_data.db'

def sql_engine(file=filename,db=db_name):
    path=file+db
    engine = create_engine(path)
    return engine

def ts_pro():
    import tushare as ts 
    token='使用你在tushare上的token'
    pro=ts.pro_api(token)
    return pro



    