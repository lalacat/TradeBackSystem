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
# ���ض�ֻƱ
# ����ֱ�Ӽ������ϵ����Ҳ����ͨ��xls����
# �����̼���أ��������������
# ͼ�α��
# """
path = 'C:\\Users\\scott\\Desktop\\invest\\���̼�.xlsx'
all_code = {
    '�ڽݹɷ�':'002192.SZ','��������':'300253.SZ',
    '����ʳƷ': '603345.SH', '��ζʳƷ': '603317.SH', '�г�ɷ�': '002891.SZ',
    '����Һ': '000858.SZ', '����ɷ�': '002568.SZ', '�±��ɷ�': '002705.SZ',
    'ʯͷ�Ƽ�': '688169.SH', '������': '603605.SH', '�й�����': '002607.SZ', '���ĿƼ�': '603533.SH',
    '��Ѷ����': '002475.SZ', '�����Ƽ�': '002859.SZ', '˳�����': '002138.SZ',
    '��������': '002036.SZ', '������A': '000725.SZ', '��������': '002912.SZ',
    '��������': '600588.SH', '������': '002410.SZ', '����Ƽ�': '600584.SH',
    '����΢': '603078.SH', '����ʱ��': '300750.SZ', '�ȵ�����': '300450.SZ',
    '���ݹɷ�': '002812.SZ', '��Դ����': '300568.SZ', '�˸�ҽҩ': '600079.SH',
    '����ҽҩ': '600276.SH', '����Ԫ': '600380.SH', '��������': '002007.SZ',
    '����̩': '300326.SZ', '����ҽ��': '300760.SZ', '��������': '300529.SZ',
    'ҩ������': '603259.SH', '����ҽѧ': '603882.SH', '���ҩ��': '603939.SH',
    '��������': '688363.SH'
}
class Coff_General(object):
    def __init__(self):
        pass

    # ���ظ��ɣ�������̼�
    def download_price(self,codes, startday):
        """����ĳ��Լ����K����"""
        if not isinstance(codes,dict):
            print('�����ֵ����͵�����{name:code.SZ/SH}')
            return None
        result = dict()
        for name,code in codes.items():
            print(f"��ʼ���غ�Լ����{code}")
            df = pro.daily_basic(ts_code=code, start_date=startday)
            df.sort_values(by='trade_date', ascending=True, inplace=True)
            print(f"���غ�Լ����{code}�������ǣ�{len(df)}")
            close_price = df[['close']]
            close_price.index = df['trade_date']
            result[code] = close_price
        return result

    # д���ļ�
    def save_excel(self,datas,path,sheet_name:list=None):
        try:
            writer = pd.ExcelWriter(path)
            if isinstance(datas,dict):
                for name,value in datas.items():
                    value.to_excel(writer, sheet_name=name)
                    # result = self.download_price(c,startday,True,writer)
                    print('����д��%s,����%d��'%(name,len(value)))
            else:
                if sheet_name:
                    datas.to_excel(writer,sheet_name=sheet_name)
                else:
                    datas.to_excel(writer)
                print('д��ɹ�')
            writer.save()
        except Exception as e :
            print(e)

    # ���ļ�������
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
            # ����ת��Ϊ����
            close.columns = [code]
            # indexת��Ϊʱ����������
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
                    print('perid�ĸ�ʽ{yyyy}/{yyyy-mm}/{yyyy-mm-dd}')
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

# new_path = 'X:\\��Ʊ\\stock.xlsx'
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
