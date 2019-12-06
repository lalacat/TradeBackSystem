import tushare as ts
from datetime import datetime

from scipy import  stats
from statsmodels.stats import anova

from base_database.database_mongo import init
from base_utils.constant import Interval, Exchange
from settings.setting import Settings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import os

os.chdir("C:\\MyDocument\\Python Quant Book\\part 2")
penn = pd.read_excel('.\\017\\Penn World Table.xlsx',2)
# print(penn.iloc[:,5:].head(3))
# model = sm.OLS(np.log(penn.rgdpe),sm.add_constant(penn.iloc[:,5:])).fit()
# print(model.summary())

print(penn.iloc[:,-6:].corr())