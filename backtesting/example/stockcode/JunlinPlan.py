from datetime import time

import openpyxl as openpyxl
import tushare as ts
import pandas as pd
import datetime as dt

from win32com.client import Dispatch

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

# 固定的表头
# A->M 13列
# 3行

def read_code():
    sheets = ['5G科技']
        # ,'自主可控','医疗健康','周期消费']
    result = None
    path = r'X:\股票\君临计划.xlsx'
    # path = r'C:\Users\scott\Desktop\invest\君临计划.xlsx'
    for sheet in sheets:
        datas = pd.read_excel(path,sheet_name=sheet,skiprows=1,index_col=1)
    result = datas
    # print(result.columns)
    # print(len(result.columns))
    old_total_share = result.iloc[:,6]
    codes = result.index
    # print(old_total_share)
    date = result.columns[-1]
    return datas,codes,date


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
def just_open(filename):
    xlApp = Dispatch("Excel.Application")
    xlApp.Visible = False
    xlBook = xlApp.Workbooks.Open(filename)
    xlBook.Save()
    xlBook.Close()
def writer_data():
    path = r'X:\股票\君临计划.xlsx'
    # path = r'C:\Users\scott\Desktop\invest\君临计划.xlsx'
    workbook = openpyxl.load_workbook(path)
    sheetnames = workbook.sheetnames
    # print(sheetnames)
    sheet = workbook[sheetnames[0]]
    # print(sheet.title) # 输出表名
    # nrows = sheet.max_row # 获得行数
    # print(nrows)
    # ncolumns = sheet.max_row
    # print(ncolumns)
    for row in sheet.iter_rows():
        result = []
        for cell in row:
            if cell.value is not None:
                result.append(cell.value)
        print(result)
    base_columns = 13
    base_rows = 2

    old_data = read_code()[0]
    print(old_data)
    old_data_length = len(old_data.columns)
    print('旧数据的长度:%d'%old_data_length)
    new_data = pd.read_csv('close_price.csv', index_col=0)
    new_data_length = len(new_data.columns)
    print('新数据的长度:%d'%new_data_length)

    max_row = len(old_data.index)+base_rows
    max_columns = old_data_length + new_data_length
    print('总数据的长度:%d'%max_columns)


    # 合并收盘价
    start_row =1
    start_col = 14
    if old_data_length == base_columns:
            before_adjust_end_col = base_columns + 1
    else:
        before_adjust_end_col = old_data_length

    before_adjust_end_row = 2
    adjust_end_row = 2
    # try:
    #     if before_adjust_end_col == base_columns + 1 :
    #         print('不需要解除合并')
    #     else:
    #         print('不需要解除合并')
    #         sheet.unmerge_cells(start_row=1, start_column=14, end_row=1, end_column=before_adjust_end_col)
    # # sheet.merge_cells(start_row=1, start_column=14, end_row=2, end_column=17)
    # except ValueError:
    #     print('解除合并失败')
    # finally:
    #     # 收盘价合并
    #     print('合并成功')
    #     sheet.merge_cells(start_row=1, start_column=14, end_row=1, end_column=max_columns)

    # for row in sheet.iter_rows(min_row=base_rows, min_col=old_data_length+1, max_col=max_columns,max_row=max_row):
    #     code = sheet.cell(row=row[0].row,column=2)
    #     # code = row[0]
    #     if code.value == '代码':
    #         i = 0
    #         print(row)
    #         for cell in row:
    #             cell.value = new_data.columns[i]
    #             i = i + 1

        # print(row)
        # print(code.value)
        # if row[0].row == base_rows:
        #     # 写入日期
        #     for cell in row:
        #         cell.value = i
        #         i = i+1
        # else:e)
    # # for row in sheet.rows:  # 多行
    # #     print(row[13])
    # #     print(type(row[13]))
    # #     i = i+1
    workbook.save(path)
    just_open(path)
# read_code()
writer_data()



# datas,codes,date = read_code()
# print(codes)
# print(date)
# result = pd.DataFrame()
# for code in codes:
#     close_price = download_price(code,'20200608')
#     if result is None:
#         result = close_price
#     else:
#         result = pd.concat([result,close_price],axis=1,sort=False)
# result = result.swapaxes(0,1)
#
# result.to_csv('close_price.csv')
#
# final = datas.join(result,how='inner')

# print(result)

# print(result)











