import re
from datetime import time

import openpyxl as openpyxl
import tushare as ts
import pandas as pd
import datetime as dt

from openpyxl.styles import Alignment,Font
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
    # path = r'X:\股票\君临计划.xlsx'
    path = r'C:\Users\scott\Desktop\invest\君临计划.xlsx'
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
    # path = r'X:\股票\君临计划.xlsx'
    path = r'C:\Users\scott\Desktop\invest\君临计划.xlsx'
    workbook = openpyxl.load_workbook(path)
    sheetnames = workbook.sheetnames
    print(sheetnames)
    sheet = workbook[sheetnames[0]]
    # print(sheet.title) # 输出表名

    base_columns = 13
    base_rows = 2

    old_data = read_code()[0]
    data_flag = old_data.columns[-1]
    if re.match('\d{8}',data_flag):
        print('有新数据的加入')
        old_data_length = len(old_data.columns) + 1
    else:
        print('只有基础数据')
        old_data_length = base_columns
    print(old_data.columns)


    print('旧数据的长度:%d'%old_data_length)
    # new_data = pd.read_csv('close_price.csv', index_col=0)
    new_data = pd.read_csv('close_price.csv', index_col=0)
    # print(new_data.index)
    new_data_length = len(new_data.columns)
    print('新数据的长度:%d'%new_data_length)

    max_row = len(old_data.index)+base_rows
    max_columns = old_data_length + new_data_length
    print('总数据的长度:%d'%max_columns)

    # 居中
    aligmentCenter = Alignment(horizontal='center', vertical='center')

    # 表题格式：黑体+14+加粗
    font_title = Font(u'黑体',size=10,bold=False,italic=False,strike=False,color='000000')

    # 正文格式：微软雅黑+10
    font_text = Font(u'微软雅黑',size=10,bold=False,italic=False,strike=False,color='000000')


    try:
        if old_data_length == base_columns:
            print('合并新数据')
            sheet.merge_cells(start_row=1, start_column=base_columns + 1, end_row=1, end_column=max_columns)

        else:
            print('附加新数据，先解除旧数据合并')
            sheet.unmerge_cells(start_row=1, start_column=base_columns + 1, end_row=1, end_column=old_data_length)
            sheet.merge_cells(start_row=1, start_column=14, end_row=1, end_column=max_columns)
            # 收盘价合并
            print('合并成功')
    except ValueError:
        print('合并失败')
    sheet['N1'].alignment = Alignment(horizontal='center', vertical='center')

    print('新数据从%d列开始'%(old_data_length+1))
    for row in sheet.iter_rows(min_row=base_rows, min_col=old_data_length + 1, max_col=max_columns,
                               max_row=max_row):
        code = sheet.cell(row=row[0].row, column=2)
        code_value = code.value
        # code = row[0]
        i = 0

        if code_value == '代码':
            for cell in row:
                cell.value = new_data.columns[i]
                cell.alignment = aligmentCenter
                cell.font = font_title
                i = i + 1
        else:
            print('写入%s的数据'%code_value)
            # print(new_data.loc[code_value,new_data.columns[i]])
            for cell in row:
                cell.value = new_data.loc[code_value,new_data.columns[i]]
                cell.alignment = aligmentCenter
                cell.font = font_text
                i = i + 1


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











