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
    token='f6b511d8d4529f19319e1861edadda749e64a5b8573102deec80cfd8'
    pro=ts.pro_api(token)
    return pro




    