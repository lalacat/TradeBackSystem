import pandas as pd
import numpy as np
import xlrd
# 标：代码
stocks_TMT = {
    # 通讯
    '深南电路':('002916.SZ',"20181101"),
    '中兴通讯':('000063.SZ',"20181101"),
    '中际旭创':('300308.SZ',"20190129"),
    '通宇通讯':('002792.SZ',"20190222"),
    # 电子
    '立讯精密':('002475.SZ','20190716'),
    '洁美科技':('002859.SZ','20190322'),
    '歌尔股份':('002241.SZ','20190919'),
    '江化微'  :('603078.SH','20191107'),
    '和而泰'  :('002402.SZ','20191127'),
    '顺络电子':('002138.SZ','20191127'),
    '联创电子':('002036.SZ','20191127'),
    '信维通讯':('300136.SZ','20191127'),
    '光弘科技':('300735.SZ','20191127'),
    '长电科技':('600584.SH','20191127'),
    # 计算机
    '四维图新':('002405.SZ','20190424'),
    '用友网络':('600588.SH','20180918'),
    '广联达'  :('002410.SZ','20190716'),
    '宝信软件':('600845.SH','20191127'),
    '中新赛克':('002912.SZ','20191127'),
    '易华录'  :('300212.SZ','20191127')
}


"""
从东方财富导出的excel中读取代码
写入csv文件
重塑列名
"""
path = 'C:\\Users\\scott\\Desktop\\bank.xls'
csv_name = 'bankcode.csv'
datas = pd.read_excel(path,header=None)

codes = datas.iloc[2:,1:3]
result = []
for values in np.array(codes):
    code= values[0]
    name = values[1]
    if '.' not in code:
        num = int(code)
        if num < 600000:
            code = code + '.SZ'
        else:
            code = code + '.SH'
    result.append([name,code])

result = pd.DataFrame(result)
# print(result)
# result.to_csv(csv_name,header=None,index=False)

test = pd.read_csv('.\\'+csv_name)
test.columns = ['name','code']

for index,values in test.iterrows():
    print(values['code'])

