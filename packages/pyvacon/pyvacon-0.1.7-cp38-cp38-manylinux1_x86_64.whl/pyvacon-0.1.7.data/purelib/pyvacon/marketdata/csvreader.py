import datetime as dt
import pandas as pd
import os

def curve_from_csv(dirName, fileName, dateFormat='%Y/%m/%d'):

    rawData = pd.read_csv(dirName + fileName, sep= ";", decimal =".", skiprows=[], header=None)
    dict = {'DATES' : [dt.datetime.strptime(d, dateFormat) for d in rawData[0]],
            'RATES' : [i for i in rawData[1]]}
    return dict

def vola_from_csv(dirName, fileName, dateFormat='%Y/%m/%d'):
    
    rawData = pd.read_csv(dirName + fileName, sep= ";", decimal =".", skiprows=[], header=None)
    dict = {'EXPIRIES' : [dt.datetime.strptime(d, dateFormat) for d in rawData[0][1:]],
            'STRIKES' : [k for k in rawData.iloc[0][1:]],
            'VOLAS' : [[v for v in rawData.iloc[i][1:]] for i in range(1, rawData.shape[0])]}
    
    return dict

def divs_from_csv(dirName, fileName, dateFormat='%Y/%m/%d'):
    
    path = dirName + fileName
    if os.path.getsize(path) == 0:
        exDates = []
        payDates = []
        cash = []
        dYield = []
        tax = []
    else:
        rawData = pd.read_csv(path, sep= ";", decimal =".", skiprows=[], header=None)
        exDates = [dt.datetime.strptime(d, dateFormat) for d in rawData[0]]
        payDates = [dt.datetime.strptime(d, dateFormat) for d in rawData[1]]
        cash =  [k for k in rawData[2]]
        dYield = [k for k in rawData[3]]
        tax = [k for k in rawData[4]]

        
    return pd.DataFrame({
        'EXDATES'  : exDates,
        'PAYDATES' : payDates,
        'CASH'     : cash,
        'YIELD'    : dYield,
        'TAX'      : tax
        })
