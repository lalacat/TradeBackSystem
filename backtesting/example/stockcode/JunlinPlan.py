from datetime import time
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
    for sheet in sheets:
        datas = pd.read_excel(r'X:\股票\君临计划.xlsx',sheet_name=sheet,skiprows=2,index_col=1)
    result = datas
    # print(result)
    # print(result.columns)
    old_total_share = result.iloc[:,6]
    codes = result.index
    print(old_total_share)
    date = result.columns[-1]
    return codes,date


    # last_day = result.columns[-2]
    # print(last_day)


# datas = pd.read_excel(r'C:\Users\scott\Desktop\invest\君临计划.xlsx', sheet_name=0, skiprows=2, index_col=0)
# print(datas)
read_code()








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

codes,date = read_code()
print(codes)
print(date)
result = pd.DataFrame()
for code in codes:
    close_price = download_price(code,date)
    if result is None:
        result = close_price
    else:
        result = pd.concat([result,close_price],axis=1)
print(result.swapaxes(0,1))

# result_01 = download_price(codes[0],date)
# result_02 = download_price(codes[1],date)
# result = pd.concat([result_01,result_02],axis=1).swapaxes(0,1)
# print(result)
# df = pro.daily_basic(ts_code='', trade_date='20180726', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
# print(df)
# old_date = '2020:12:19'
# new_date = dt.datetime.strptime(old_date,'%Y:%m:%d').date()
# print(new_date)


# TypeError ValueError










