import re
from datetime import datetime

import pandas as pd
import numpy as np
from arch.unitroot import  ADF
import statsmodels.api as sm
from itertools import combinations

class PairTrading(object):
    """
    配对交易类
    包含最小距离法
    协整模型
    """
    def __init__(self):
        self.priceX = None
        self.priceY = None
        self.returnX= None
        self.returnY = None
        self.standardX= None
        self.standardY= None
        self.logPriceX = None
        self.logPriceY = None
        self.resultSSD = pd.DataFrame()
        self.resultCoint = pd.DataFrame()
        self.resultNotCoint = pd.DataFrame()
        self.debug = False

    def setStock(self,priceX,priceY):
        if priceX is None or priceY is None:
            return  None
        self.priceX = priceX
        self.priceY = priceY
        self.returnX= None
        self.returnY = None
        self.standardX= None
        self.standardY= None


    '''
    最小距离
    '''

    def SSD(self,timePeriod=None):
        formX,formY = self.getPeriodPrice(timePeriod)
        standardX = self.standardPrice(formX)
        standardY = self.standardPrice(formY)
        SSD = np.sum((standardX + standardY) ** 2)
        return SSD

    def SSDSpread(self,timePeriod=None):
        formX,formY = self.getPeriodPrice(timePeriod)
        standardX = self.standardPrice(formX)
        standardY = self.standardPrice(formY)
        spread = standardY - standardX
        return spread

    # 计算多个股票之间的SSD
    def calAllSSD(self,stocks:pd.DataFrame):
        if not isinstance(stocks,pd.DataFrame):
            raise TypeError('传入的格式不对，传入DataFrame格式的参数')
        # num = len(stocks)
        self.resultSSD = None
        results = []
        combins = [c for c in combinations(stocks.columns, 2)]
        for c in combins:
            # print(c)
            # 选出最小距离的股票对
            self.setStock(stocks[c[0]], stocks[c[1]])
            ssd = self.SSD()
            results.append([c[0]+':'+c[1],ssd])
        self.resultSSD = pd.DataFrame(results,columns=['name','ssd']).sort_values(by=['ssd'])
    '''
    协整模型
    '''
    # 形成期协整关系检验
    def checkLogPrice(self,price,name):
        adfprice = ADF(price)
        if adfprice.pvalue >= 0.05:
            if self.debug:
                print(
                    '''
                    %s 价格的对数序列不具有平稳性.
                    p-value of ADF test: %f
                    '''% (name,adfprice.pvalue)
                )
            return True
        else:
            if self.debug:
                print(
                    '''
                    %s 价格的对数序列具有平稳性
                    p-value of ADF test: %f
                    ''' % (name,adfprice.pvalue)
                )
            return False

    def checkDiffPrice(self,price,name):
        diffPrice = price.diff()[1:]
        adfDiff = ADF(diffPrice)
        if adfDiff.pvalue <= 0.05:
            if self.debug:
                print(
'''
%s 价格的对数序列具有平稳性            
p-value of ADF test: %f
''' %  (name,adfDiff.pvalue)
                )
            return True
        else:
            if self.debug:
                print(
'''
%s 价格的对数序列不具有平稳性
p-value of ADF test: %f
''' % (name,adfDiff.pvalue)
                )
            return False
    # 协整关系检验
    def cointegration(self,priceX=None,priceY=None):
        # 判断两支股票是否协整
        if priceX:
            logPriceX = np.log(priceX)
        else:
            logPriceX = self.priceX
        if priceY:
            logPriceY = np.log(priceY)
        else:
            logPriceY =self.priceY
        if self.checkLogPrice(logPriceX,'PriceX') or self.checkLogPrice(logPriceY,'PriceY'):
            if self.checkDiffPrice(logPriceX,'PriceX') or self.checkDiffPrice(logPriceY,'PriceY'):
                results = sm.OLS(logPriceY, sm.add_constant(logPriceX)).fit()
                resid = results.resid
                # 用单位根检验法，判断残差项是否平稳
                adfSpread = ADF(resid)
                if adfSpread.pvalue >= 0.05:
                    if self.debug:
                        print(
                            """
                            交易价格不具有协整关系。
                            p-value of ADF test: %f
                            回归系数：
                                截距：%f
                                系数：%f
                            """ % (adfSpread.pvalue, results.params[0], results.params[1])
                        )
                    return None, None
                else:
                    if self.debug:
                        print(
                            """
                            交易价格具有协整关系。
                            p-value of ADF test: %f
                            回归系数：
                                截距：%f
                                系数：%f
                            """ % (adfSpread.pvalue, results.params[0], results.params[1])
                        )
                    return results.params[0], results.params[1]
        return None,None



    def CointegrationSpread(self,formPeriod=None,tradePeriod=None):
        if self.priceX or self.priceY is None:
            raise Exception('先使用setStock（x,y）')
        formX,formY = self.getPeriodPrice(formPeriod)
        coefficiens = self.cointegration(formX,formY)

        if coefficiens is None :
            print('未形成协整关系')
            return  None
        else :
            if tradePeriod is None:
                tradePeriod = formPeriod
            formX, formY = self.getPeriodPrice(tradePeriod)
            logPriceX = np.log(formX)
            logPriceY = np.log(formX)
            spread = logPriceY - coefficiens[0]-coefficiens[1]*logPriceX
            return spread

    def calAllCointegration(self,stocks:pd.DataFrame):
        if not isinstance(stocks, pd.DataFrame):
            raise TypeError('传入的格式不对，传入DataFrame格式的参数')
        self.resultCoint = pd.DataFrame()
        self.resultNotCoint = pd.DataFrame()
        combins = [c for c in combinations(stocks.columns, 2)]
        for c in combins:
            # print(c)
            # 判断是否协整
            self.setStock(stocks[c[0]], stocks[c[1]])
            alpha,beta = self.cointegration()
            name = c[0] + ':' + c[1]
            if alpha:
                results = pd.DataFrame([[alpha,beta]],columns=['alpha', 'beta'],index=[name])
                self.resultCoint = self.resultCoint.append(results)
            else:
                self.resultNotCoint = self.resultNotCoint.append(pd.DataFrame([name],columns=['name']))



    def calBound(self,method,formPeriod=None,width=1.5):
        if method == 'SSD':
            spread = self.SSDSpread(formPeriod)
        elif method == 'Cointegation':
            spread = self.CointegrationSpread(formPeriod)
        else:
            raise Exception('不存在该方法，选择‘SSD’或者‘Cointegration’')
            return None,None
        mu = np.mean(spread)
        std = np.std(spread)
        UpBound = mu + width * std
        DownBound = mu - width * std
        return UpBound, DownBound

    def getDateIndex(self,date):
        result = date.split(':')
        # if isinstance(date, datetime):
        #     result = date
        # else:
        start = datetime.strptime(result[0], '%Y%m%d').date()
        end = datetime.strptime(result[1], '%Y%m%d').date()
        return start,end

    def getPeriodPrice(self,timePeriod):
        if timePeriod:
            form_start, form_end = self.getDateIndex(timePeriod)
            formX = self.priceX[self.getDateIndex(form_start):self.getDateIndex(form_end)]
            formY = self.priceY[self.getDateIndex(form_start):self.getDateIndex(form_end)]
        else:
            formX = self.priceX
            formY = self.priceY
        return  formX,formY

    def standardPrice(self,price):
        # 价格标准化
        ret = (price - price.shift(1)) / price.shift(1)[1:]
        standard= (ret + 1).cumprod()
        return standard

    def to_csv(self,csv_path=None):
        print(len(self.resultCoint))
        if len(self.resultSSD) > 0 :
            self.resultSSD.to_csv('resultSSD.csv',header=None,index=False)
        if len(self.resultCoint) > 0 :
            self.resultCoint.to_csv('resultCoint.csv')
        if len(self.resultNotCoint) > 0 :
            self.resultNotCoint.to_csv('resultNotCoint.csv',index=False)

