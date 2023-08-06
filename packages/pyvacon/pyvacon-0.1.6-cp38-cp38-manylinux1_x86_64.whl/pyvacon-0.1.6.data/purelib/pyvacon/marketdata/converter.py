# -*- coding: utf-8 -*-
"""


Spyder Editor

This is a temporary script file.
"""
import datetime as dt
import math
import pandas as pd
import pyvacon.analytics as analytics
import pyvacon.tools.converter as converter
import pyvacon.tools.enums as enums

def dividend_from_dict(udl_key, div_dict, refdate):
	div_tmp = div_dict.to_dict()
	ex_dates = None
	pay_dates = None
	tax_factors = None
	div_yield = None
	div_cash = None
	if isinstance(div_dict,pd.DataFrame):
		ex_dates = converter.createPTimeList(refdate, [x.to_pydatetime() for x in div_dict['EXDATES'].tolist()])
		pay_dates = converter.createPTimeList(refdate, [x.to_pydatetime() for x in div_dict['PAYDATES'].tolist()])
		tax_factors = analytics.vectorDouble(div_dict['TAX'].tolist())
		div_yield = analytics.vectorDouble(div_dict['YIELD'].tolist())
		div_cash = analytics.vectorDouble(div_dict['CASH'].tolist())
	else:
		ex_dates = converter.createPTimeList(refdate,div_dict['EXDATES'])
		pay_dates = converter.createPTimeList(refdate, div_dict['PAYDATES'])
		tax_factors = analytics.vectorDouble(div_dict['TAX'])
		div_yield = analytics.vectorDouble(div_dict['YIELD'])
		div_cash = analytics.vectorDouble(div_dict['CASH'])
	return analytics.DividendTable(udl_key+'_DIV', refdate, ex_dates, div_yield, 
                                      div_cash, tax_factors, pay_dates)

def volparam_from_dict(volparam, refdate):
    if volparam['TYPE'] == 'SSVI':
        
            expiries = volparam['EXPIRIES']
            atmFVols = analytics.vectorDouble(volparam['ATMVOLS'])
    
            param = analytics.VolatilityParametrizationSSVI(expiries, atmFVols, volparam['RHO'], 
                                                            volparam['ETA'], volparam['GAMMA'])
            return param
    if volparam['TYPE'] == 'GRID':

            expiries = volparam['EXPIRIES']
            strikes = volparam['STRIKES']
            volas = volparam['VOLAS']

            param = analytics.VolatilityParametrizationTimeSlice(expiries, strikes, volas, 'MONOTONE')
            
            return param
    if volparam['TYPE'] == 'FLAT':

            flatVol = volparam['VOLA']

            param = analytics.VolatilityParametrizationFlat(flatVol)
            
            return param

    
    raise Exception('Volparametrization not yet implemented.')


def borrow_from_dict(udl_key, bc_dict, refdate):
    daycounter = analytics.DayCounter('ACT365Fixed')
    dates = converter.createPTimeList(refdate, bc_dict['DATES'])
    rates = bc_dict['RATES']
    values = []
    for i in range(len(dates)):
        values.append(math.exp(-rates[i]*daycounter.yf(refdate, dates[i])))
    result = analytics.DiscountCurve(udl_key+'_BC', refdate, dates, values,
                                     'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
    return result
    
def discount_from_dict(yc_key, yc_dict, refdate):
	daycounter = analytics.DayCounter('ACT365Fixed')
	dates = converter.createPTimeList(refdate, yc_dict['DATES'])
	rates = yc_dict['RATES']
	values = []
	for i in range(len(dates)):
		values.append(math.exp(-rates[i]*daycounter.yf(refdate, dates[i])))
	result = analytics.DiscountCurve(yc_key, refdate, dates, values,
                                     'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
	return result

def fwd_from_dict(udl, udl_key, yc_dict, yc_key, refdate):
    bc = borrow_from_dict(udl_key, udl['BORROW'], refdate)
    dc = discount_from_dict(yc_key, yc_dict[yc_key], refdate)
    div = dividend_from_dict(udl_key, udl['DIVIDENDS'], refdate)
    spot = udl['SPOT']
    forward_curve = analytics.EquityForwardCurve(refdate, spot, dc, bc, div)
    return forward_curve

def vol_from_dict(udl_dict, yc_dict, udl_key, yc_key, refdate):
    fwd = fwd_from_dict(udl_dict[udl_key], udl_key, yc_dict, yc_key, refdate)
    vol_param = volparam_from_dict(udl_dict[udl_key]['VOLATILITY'], refdate)
    vol_surf = analytics.VolatilitySurface(udl_key+'_VOL', refdate, fwd, enums.DayCounter.ACT365_FIXED, vol_param)
    return vol_surf
