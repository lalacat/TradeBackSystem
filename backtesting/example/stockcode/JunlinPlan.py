from datetime import time

import openpyxl as openpyxl
import tushare as ts
import pandas as pd
import datetime as dt

token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'
ts.set_token(token)
pro = ts.pro_api()
# 读取代码
'''
1.读取4个schema
2. 形成标准结果
3.读取估值
4.读取股价
'''

def read_code():
    sheets = ['5G科技']
        # ,'自主可控','医疗健康','周期消费']
    result = None
    # path = r'X:\股票\君临计划.xlsx'
    path = r'C:\Users\scott\Desktop\invest\君临计划.xlsx'
    for sheet in sheets:
        datas = pd.read_excel(path,sheet_name=sheet,skiprows=2,index_col=1)
    result = datas
    print(result.columns)
    print(len(result.columns))
    old_total_share = result.iloc[:,6]
    codes = result.index
    # print(old_total_share)
    date = result.columns[-1]
    # return datas,codes,date


    # last_day = result.columns[-2]
    # print(last_day)


# datas = pd.read_excel(r'C:\Users\scott\Desktop\invest\君临计划.xlsx', sheet_name=0, skiprows=2, index_col=0)
# print(datas)
# read_code()








'''
不同的schema的股价下载
结果规范
index=代码
colunms=日期
'''
# 下载代码
def download_price(code,startday):
    """下载某一合约的分钟线数据"""
    print(f"开始下载合约数据{code}")
    df = pro.daily_basic(ts_code=code, start_date=startday)
    df.sort_values(by='trade_date', ascending=True, inplace=True)
    new_total_share = df.loc[0,'total_share'] # 最新的股本数
    df_01 = df[['trade_date','close']].swapaxes(0,1)
    # df_01.index = [code,code]
    df_01.columns = df_01.iloc[0,:]
    result = df_01.iloc[1,:]
    result.index.name = code
    result.name = code
    # print(type(result))
    #
    # print(result)
    # return df

    return result
# 写入股价
'''
1.追加新的股价
2.对比估值变色
'''
def writer_data():
    # path = r'X:\股票\君临计划.xlsx'
    path = r'C:\Users\scott\Desktop\invest\君临计划.xlsx'
    workbook = openpyxl.load_workbook(path)
    sheetnames = workbook.sheetnames
    print(sheetnames)
    sheet = workbook[sheetnames[0]]
    # table = workbook.active
    print(sheet.title) # 输出表名
    nrows = sheet.max_row # 获得行数
    print(nrows)
    ncolumns = sheet.max_row
    print(ncolumns)
    for row in sheet.rows:  # 多行
        print(row[13].value)

read_code()
writer_data()



# datas,codes,date = read_code()
# print(codes)
# print(date)
# result = pd.DataFrame()
# for code in codes:
#     close_price = download_price(code,date)
#     if result is None:
#         result = close_price
#     else:
#         result = pd.concat([result,close_price],axis=1)
# result = result.swapaxes(0,1)
#
# final = datas.join(result,how='inner')
#
# print(final)












