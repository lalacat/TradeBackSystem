import os

import pandas as pd

os.chdir("C:\\MyDocument\\Python Quant Book\\part 2")
penn = pd.read_excel('.\\017\\Penn World Table.xlsx',2)
# print(penn.iloc[:,5:].head(3))
# model = sm.OLS(np.log(penn.rgdpe),sm.add_constant(penn.iloc[:,5:])).fit()
# print(model.summary())

print(penn.iloc[:,-6:].corr())