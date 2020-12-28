from zsxq.database.base import get_data
import pandas as pd

path1 = r'X:\股票\君临计划-消费.xlsx'
path2 = r'X:\股票\君临计划-科技.xlsx'
path3 = r'X:\股票\君临计划-医药.xlsx'
paths = [path1,path2,path3]


data = pd.read_excel(path1,sheet_name=0,header=1)
code = data['代码'].iloc[0]
d = data.iloc[:,-6:-1]
print(code)
print(d)
d.columns = ['trade_data','down','mid_01','mid_02','up']
d.index = pd.to_datetime(d['trade_data'],format='%Y%m%d')
d['mid'] = (d['mid_01']+d['mid_02'])/2
final_data = d[['down','mid','up']]
print(final_data)

# final = pd.concat([close,final_data],axis=1)
# final = final.fillna(method='ffill')
# final = final.dropna()
# print(final)
