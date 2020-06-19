from datetime import time

import pandas as pd


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
        datas = pd.read_excel(r'C:\Users\scott\Desktop\invest\君临计划.xlsx',sheet_name=sheet,skiprows=2,index_col=0)
        # orient = datas.to_dict(orient='record')
        # for o in orient:
        #     print(o)
        if result is None:
            result = datas
        else:
            result = pd.concat([result,datas],axis=0,sort=False)
    # # print(result.columns)
    codes = result['代码']
    print(codes)
    # for code  in codes:
    #     print(code)

    # last_day = result.columns[-2]
    # print(last_day)


# datas = pd.read_excel(r'C:\Users\scott\Desktop\invest\君临计划.xlsx', sheet_name=0, skiprows=2, index_col=0)
# print(datas)
read_code()





# 下载代码
def download_price(code,start_date, end_data=None, build_time=None, asset='E', adj=False):
    """下载某一合约的分钟线数据"""
    print(f"开始下载合约数据{code}")
    symbol, exchange = code.split(".")

    start = time()

    if not end_data:
        end_data = start_date

    if adj:
        # 前复权
        df = ts.pro_bar(ts_code=code, asset=asset, start_date=start_date, end_date=end_data, adj='qfq')
    else:
        # 不复权
        df = ts.pro_bar(ts_code=code, asset=asset, start_date=start_date, end_date=end_data)
    df.sort_values(by='trade_date', ascending=True, inplace=True)


'''
不同的schema的股价下载
结果规范
index=代码
colunms=日期
'''

# 写入股价
'''
1.追加新的股价
2.对比估值变色
'''

























