# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, timedelta
import sys
import sqlite3
from pandas.io.sql import DatabaseError

from zsxq.database.base import sql_engine, ts_pro,ts

token = 'e0eeb08befd1f07516df2cbf9cbd58663f77fd72f92a04f290291c9d'
db_name = 'stock_data.db'
starttime = '20150101'
endtime = ''  # endtime默认是最近的一个交易日，若未自定请保持''，引号内无空格


# def sqlo(dbname):
#     path = 'C:\\Users\\scott\\Documents\\学习文档\\stock_db'+ '\\'
#     # path = 'W:\\stock_db'+ '\\'
#     return sqlite3.connect(path + dbname)
#
#
# def ts_pro(Token):
#     return ts.pro_api(Token)

engine = sql_engine()
ts = ts()

# 获取股票代码列表
def get_code():
    stocklist = pro.stock_basic(list_status='L')
    codes = stocklist.ts_code.values
    stockcodes = stocklist.symbol.values
    names = stocklist.name.values
    return codes, stockcodes, names


# 获取股票交易日历
def get_cals():
    # 获取交易日历
    cals = pro.trade_cal(exchange='')
    cals = cals[cals.is_open == 1].cal_date.values
    return cals


class Data(object):
    def __init__(self, start, end=''):
        self.cals = get_cals()
        self.now = None
        self.start = None
        self.end = None
        self.get_trade_date(start, end)
        # self.fiter_code = ['300911.SZ', '300915.SZ', '300916.SZ', '605258.SH', '688557.SH', '688578.SH']
        self.fiter_code = []

        self.conn = engine
        self.cur = self.conn.cursor()

        self.all_tables = None
        self.null = None
        self.stocklist = get_code()
        self.codes = self.stocklist[0]  # 带'.sz'后缀的代码
        self.stockcodes = self.stocklist[1]  # 不带后缀的代码
        # self.names = self.stocklist[2]  # 股票名字

    # 检查数据库
    def checkdb(self):
        try:
            table_names = pd.read_sql(
                "select name from sqlite_master where type='table' order by name", self.conn).values
            # sqlite_sequence表也是SQLite的系统表。该表用来保存其他表的RowID的最大值。
            # 数据库被创建时，sqlite_sequence表会被自动创建。该表包括两列。
            # 第一列为name，用来存储表的名称。第二列为seq，用来保存表对应的RowID的最大值
            if 'sqlite_sequence' in table_names:
                table_names = table_names[:-1]
            self.all_tables = table_names
        except Exception as e:
            print(e)
            print('还没有检查到数据库存在，即将开始获取股票数据...')
            self.all_tables = []

    # 每日行情数据
    def get_daily_data(self,codes=None):
        if codes is not None:
            stockcodes = codes
        else:
            if self.null is not None:
                stockcodes = self.null
            else:
                stockcodes = self.codes
        nn = 0
        for stockcode in stockcodes:
            try:
                df = self._get_newdata(ts_code=stockcode, start_date=self.start, end_date=self.end)
                if df.empty:
                    print(f'数据获取失败或该股票在{self.end}后上市，现跳过其数据获取。')
                    nn += 1
                    self.fiter_code.append(stockcode)
                    continue
                # self._check_col(stockcode,df)
                df.to_sql(stockcode[:-3], self.conn, index=False, if_exists='append')
                nn += 1
                print(f"完成第{nn}/{len(stockcodes)}支股票支股票 {stockcode} 共计{len(df)}条的数据获取与保存，进度：{round(nn/len(stockcodes)*100, 2)}%")
            except Exception as e:
                print(stockcode)
                print(e)

    # 获取最新交易日期
    def get_trade_date(self, start_time, end_time, now_time=datetime.now()):
        while start_time not in self.cals:
            start_time1 = parse(start_time)
            start_time = (start_time1 + timedelta(1)).strftime('%Y%m%d')
        self.start = start_time

        # 获取当天日期时间
        if now_time.hour > 15:
            d = now_time.strftime('%Y%m%d')
        else:
            d = (now_time - timedelta(1)).strftime('%Y%m%d')
        while d not in self.cals:
            d1 = parse(d)
            d = (d1 - timedelta(1)).strftime('%Y%m%d')
        self.now = d

        if end_time == '':
            self.end = self.now
        else:
            self.end = end_time

    # 更新数据库数据
    def update_sql(self,codes=None):
        ns = 0
        if codes and len(codes) > 0:
            all_codes = codes
        else:
            all_codes = self.codes
        codes = []
        for sc in all_codes:
            ns += 1
            if sc in self.fiter_code:
                print(f'{sc}获取失败，现跳过其数据获取。')
                continue
            try:
                d0 = pd.read_sql(f"select max(trade_date) from '{sc[:-3]}' ", self.conn).values[0][0]
            except DatabaseError:
                print(f"[ERROR]第{ns}/{len(all_codes)}支股票{sc}:no such table: {sc}")
                if sc not in self.fiter_code:
                    self.get_daily_data([sc])
                    codes.append(sc)
                continue
            if d0 != self.end:
                if d0 is None:
                    d0 = self.start
                n0 = np.argwhere(self.cals == d0)[0][0] + 1
                n1 = np.argwhere(self.cals == self.end)[0][0] + 1
                dates = self.cals[n0:n1]
                df = self._get_newdata(ts_code=sc, start_date=dates[0], end_date=dates[-1])
                # self._check_col(sc,df)
                if df.empty:
                    print(f'股票{sc}已停牌，跳过其数据获取')
                    continue
                df.to_sql(sc[:-3], self.conn, index=False, if_exists='append')
                print(f'第{ns}/{len(all_codes)}支股票{sc}数据有更新，更新{len(df)}条数据，进度：{round(ns / len(self.stockcodes) * 100, 2)}%')
            else:
                print(f'第{ns}/{len(all_codes)}支股票{sc}数据无更新，跳过...，进度：{round(ns / len(self.stockcodes) * 100, 2)}%')
        if codes is not None and len(codes) > 0 :
            self.update_sql(codes)
        else:
            print('数据库更新完毕！')

    # 查询数据库信息
    def info_sql(self):
        if self.all_tables is None:
            self.checkdb()
        print(f'数据库包含股票个数：{len(self.all_tables)}')
        sql1=f'select min(trade_date) from "{self.all_tables[0][0]}"'
        sql2=f'select max(trade_date) from "{self.all_tables[0][0]}"'
        t0=pd.read_sql(sql1,self.conn).values[0][0]
        t1=pd.read_sql(sql2,self.conn).values[0][0]
        print(f'数据期间：{t0}——{t1}')

    # 中枢执行函数
    def executes(self):
        # ## 1 检查数据库
        self.checkdb()
        # ## 2 判断是否有股票退市/上市
        # 2.1 还没有获取股票数据
        if len(self.all_tables) == 0:
            print('开始获取股票数据，请稍候...')
            self.get_daily_data()
        # 2.2 有股票退市/上市
        elif len(self.all_tables) != 0 and len(self.stockcodes) != len(self.all_tables):
            print('股票列表有变动(或数据还未获取完整)，开始检查...')
            c = 0
            for tn in self.all_tables:
                if tn not in self.stockcodes:
                    self.cur.execute(f"drop table '{tn[0]}'")
                    print(f'股票{tn[0]}退市，现已将其数据从数据库中删除。')
                    c = 1
            if c == 1:  # 删除过数据库里面的列表，需要再更新一次列表
                # 退市处理
                all_tables = pd.read_sql("select name from sqlite_master where type='table' order by name",
                                         self.conn).values
                if 'sqlite_sequence' in all_tables:
                    all_tables = all_tables[:-1]
                self.all_tables = all_tables
            else:
                null = []
                # 新上市处理
                for sc in self.codes:
                    if sc[:-3] not in self.all_tables:
                        null.append(sc)
                if len(null) > 0:
                    print('股票数据有遗漏，开始查漏补缺...')
                    self.null = null
                    # print(self.null)
        # """
                    self.get_daily_data()
            self.update_sql()  # 最后再检查一下有没有更新

        # 2.3 数据库股票数量与股票列表一样，但不排除'退市股票==上市股票'
        else:
            c = 0
            for sc in range(len(self.stockcodes)):
                if self.stockcodes[sc] != self.all_tables[sc][0]:
                    c = 1
            # 2.3.1 退市的股票数刚好等于新上市的股票数
            if c == 1:
                # 2.3.1.1 删除退市的
                for tn in self.all_tables:
                    if tn not in self.stockcodes:
                        self.cur.execute(f"drop table '{tn[0]}'")
                        print(f'股票{tn[0]}退市，现已将其数据从数据库中删除。')

                table_name = pd.read_sql("select name from sqlite_master where type='table' order by name",
                                         self.conn).values
                if 'sqlite_sequence' in table_name:
                    table_name = table_name[:-1]
                self.all_tables = table_name
                # 2.3.1.2 获取新上市股票的数据
                null = []
                for sc in self.stockcodes:
                    if sc not in self.all_tables:
                        null.append(sc)
                print('股票数据有遗漏，开始查漏补缺...')
                self.null = null
                self.get_daily_data()
                table_name = pd.read_sql("select name from sqlite_master where type='table' order by name",
                                         self.conn).values
                if 'sqlite_sequence' in table_name:
                    table_name = table_name[:-1]
                self.all_tables = table_name
                # 2.3.1.2 最后再检查一下更新
                self.update_sql()
            # 2.3.2 没有退市/上市，检查有没有更新
            else:
                self.update_sql()

    def _get_newdata(self,ts_code, start_date, end_date):
        # df0 = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        try :
            df0 = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date ,adj='qfq', adjfactor=True)# 复权因子
        except IOError:
            df0 = pd.DataFrame()
        if df0.empty:
            return df0
        else:
            df1 = pro.daily_basic(ts_code=ts_code, start_date=start_date)
            del df1['close']
        df = pd.merge(df0, df1)
        return df

    def _check_col(self,ts_code,new_df):
        sql1 = f"PRAGMA  table_info('{ts_code}')"
        db_col = pd.read_sql(sql1,self.conn)['name'].values.tolist()
        new_col = new_df.columns.values.tolist()
        if len(db_col) != len(new_col):
            col = list(set(new_col).difference(set(db_col)))
            # print(f"{ts_code}有新列增加{col}")
            for c in col:
                add_col_sql = f'ALTER TABLE "{ts_code}" ADD COLUMN {c} real'
                engine.execute(add_col_sql)


# """

if __name__ == "__main__":
    pro = ts.pro_api()
    data = Data(starttime, endtime)
    # data.get_daily_data()
    data.executes()
    # data.info_sql()


    # # macos自动关机指令
    # import os
    # password = "锁屏密码输入到引号内"
    # command = "sudo shutdown -h now"
    # os.system('echo %s | sudo -S %s' % (password, command))

    # data.info_sql()
    # for tn in data.all_tables:
    #     data.cur.execute(f"drop table '{tn[0]}'")
    #     print(f'股票{tn[0]}退市，现已将其数据从数据库中删除。')