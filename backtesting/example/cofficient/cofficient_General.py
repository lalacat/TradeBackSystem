# coding=gbk

import tushare as ts
import pandas as pd
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
token = 'bfbf67e56f47ef62e570fc6595d57909f9fc516d3749458e2eb6186a'
ts.set_token(token)
pro = ts.pro_api()

# """
# 下载多只票
# 可以直接计算相关系数，也可以通过xls计算
# 以收盘价相关，或者收益率相关
# 图形表达
# """
path = 'C:\\Users\\scott\\Desktop\\invest\\收盘价.xlsx'
all_code = {
    '融捷股份':'002192.SZ','卫宁健康':'300253.SZ',
    '安井食品': '603345.SH', '天味食品': '603317.SH', '中宠股份': '002891.SZ',
    '五粮液': '000858.SZ', '百润股份': '002568.SZ', '新宝股份': '002705.SZ',
    '石头科技': '688169.SH', '珀莱雅': '603605.SH', '中公教育': '002607.SZ', '掌阅科技': '603533.SH',
    '立讯精密': '002475.SZ', '洁美科技': '002859.SZ', '顺络电子': '002138.SZ',
    '联创电子': '002036.SZ', '京东方A': '000725.SZ', '中新赛克': '002912.SZ',
    '用友网络': '600588.SH', '广联达': '002410.SZ', '长电科技': '600584.SH',
    '江化微': '603078.SH', '宁德时代': '300750.SZ', '先导智能': '300450.SZ',
    '恩捷股份': '002812.SZ', '星源材质': '300568.SZ', '人福医药': '600079.SH',
    '恒瑞医药': '600276.SH', '健康元': '600380.SH', '华兰生物': '002007.SZ',
    '凯利泰': '300326.SZ', '迈瑞医疗': '300760.SZ', '健帆生物': '300529.SZ',
    '药明康德': '603259.SH', '金域医学': '603882.SH', '益丰药房': '603939.SH',
    '华熙生物': '688363.SH'
}
class Coff_General(object):
    def __init__(self):
        pass

    # 下载个股，获得收盘价
    def download_price(self,codes, startday):
        """下载某合约的日K数据"""
        if not isinstance(codes,dict):
            print('传入字典类型的数据{name:code.SZ/SH}')
            return None
        result = dict()
        for name,code in codes.items():
            print(f"开始下载合约数据{code}")
            df = pro.daily_basic(ts_code=code, start_date=startday)
            df.sort_values(by='trade_date', ascending=True, inplace=True)
            print(f"下载合约数据{code}的数量是：{len(df)}")
            close_price = df[['close']]
            close_price.index = df['trade_date']
            result[code] = close_price
        return result

    # 写入文件
    def save_excel(self,datas,path,sheet_name:list=None):
        try:
            writer = pd.ExcelWriter(path)
            if isinstance(datas,dict):
                for name,value in datas.items():
                    value.to_excel(writer, sheet_name=name)
                    # result = self.download_price(c,startday,True,writer)
                    print('正在写入%s,共计%d条'%(name,len(value)))
            else:
                if sheet_name:
                    datas.to_excel(writer,sheet_name=sheet_name)
                else:
                    datas.to_excel(writer)
                print('写入成功')
            writer.save()
        except Exception as e :
            print(e)

    # 从文件读代码
    def read_excel(self,codes,path,period:set=None,sheet_name=None):
        if not isinstance(codes,dict):
            return
        else:
            if sheet_name:
                result = pd.read_excel(path, header=0, index_col=0,sheet_name=[sheet_name])[sheet_name]
            else:
                names = {}
                for name,code in codes.items():
                    names[code]=name
                datas = pd.read_excel(path, header=0, index_col=0, sheet_name=list(codes.values()))
                result = self.dict_dataframe(datas,period)
        return result

    def dict_dataframe(self,datas,period:set=None):
        result = None
        for code, close in datas.items():
            # 列名转换为代码
            close.columns = [code]
            # index转换为时间序列类型
            close.index = pd.to_datetime(close.index, format='%Y%m%d')
            if period is None:
                data = close
            else:
                try:
                    if period[0] == 0:
                        data = close[:period[1]]
                    elif period[1] == None or period[1] == 0:
                        data = close[period[0]:]
                    else:
                        data = close[period[0]:period[1]]
                except Exception:
                    print('perid的格式{yyyy}/{yyyy-mm}/{yyyy-mm-dd}')
                    return None
            if result is None:
                result = data
            else:
                result = pd.concat([result, data], axis=1, sort=False)
        return result

    def annualize(self,returns, period):
        if period == 1:
            return ((1 + returns).cumprod()[-1] ** (252 / len(returns)) - 1)
        if period == 30:
            return ((1 + returns).cumprod()[-1] ** (12 / len(returns)) - 1)
        if period == 90:
            return ((1 + returns).cumprod()[-1] ** (4 / len(returns)) - 1)
        if period == 180:
            return ((1 + returns).cumprod()[-1] ** (2 / len(returns)) - 1)
        if period == 360:
            return ((1 + returns).cumprod()[-1] ** (1 / len(returns)) - 1)

    def fillInfNaN(self,returns, method='ffill'):
        # returns = returns.fillna(method='bfill').round(4)
        returns = returns.dropna().round(4)
        returns = returns.replace([np.inf, -np.inf], np.NaN).fillna(method=method)
        return returns

    def getReturn(self,datas,peried=1):
        lagclose = datas.shift(peried)
        result = (datas - lagclose) / lagclose
        # returns = datas.close_price.pct_change().dropna()
        # print('%s: %f' % (code, annualize(returns, 1)))
        return self.fillInfNaN(result)

# new_path = 'X:\\股票\\stock.xlsx'
#
# cg = Coff_General()
# datas = cg.download_price(all_code,'20170101')
# cg.save_excel(datas,new_path)
#


# result_path  = 'C:\\Users\\scott\\Desktop\\invest\\test.xlsx'
# result = cg.download_price(all_code,'20201101')
# print(result)
# r = cg.dict_dataframe(result)
# ret = cg.getReturn(r,1)
# print(ret)
# for col in ret.iteritems():
#     print(col[0])
#     print(cg.annualize(col[1],360))
# corr = r.corr(method = 'pearson')
# cg.save_excel(corr,result_path,'corr')
# cg.save_excel(result,result_path)


# result = cg.read_excel(all_code,path,('2020-09','2020-10'))
# print(result)
# corr = result.corr(method = 'pearson')
#

# result = read_excel(['002192.SZ','300750.SZ','300450.SZ'],path,('2020-09','2020-10'))
# print(result)
#
# plt.scatter(result['002192.SZ'],result['300750.SZ'])
# plt.legend()
# plt.show()
