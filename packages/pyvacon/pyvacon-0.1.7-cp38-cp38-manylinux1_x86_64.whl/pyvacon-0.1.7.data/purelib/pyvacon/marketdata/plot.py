# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np



import pyvacon.analytics as analytics
import pyvacon.tools.enums as enums
import pyvacon.tools.converter as converter
import logging


        
"""
provides plotting tools around market data objects
"""
def transition_matrix_pd(trans_matrix, ratings, legend_prefix = ''):
    """
    plot all default probability curves for a given transition matrix
        
    trans_matrix transition matrix used to compute the pd
    ratings list of ratings for which default probs are computed
    legend_prefix prefix for legend label (neede id one wants to make plots for different matrices in the same figure)
    """
    dates = [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.0]
    #dates = [0,  5.0, 20.0, 30.0, 50.0]
    for i in range(len(ratings)):
        rating = ratings[i]
        r = analytics.Rating('test', analytics.ptime(2000,1,1,0,0,0), rating)
        tmp = converter.convertToVector(dates)
        pdTmp = analytics.vectorDouble()
        trans_matrix.computeDefaultProb(pdTmp,r,tmp)
        pd = converter.convertFromVector(pdTmp)
        #print(rating + " : " + str(pd))
        plt.plot(dates, pd, '-x', label=legend_prefix + rating)
    plt.title('default probabilities')
    plt.xlabel('ttm')
    plt.ylabel('probability of default')
    plt.legend()
        
def transition_matrix_heatmap(trans_matrix, time_to_maturity, title = True):
    """
    plot the transition matrix for a certain horizon
        
    trans_matrix transition matrix used to compute the transition for a certain horizon
    time_to_maturity time horizon
    title if True a title is plotted, otherwise no title will be generated
    """
    matrix = analytics.vectorDouble()
    trans_matrix.computeTransition(matrix, time_to_maturity)
    tmp = []
    for i in range(analytics.Rating.nRatings()):
        tmp1 = []
        for j in range(analytics.Rating.nRatings()):
            tmp1.append(matrix[i*analytics.Rating.nRatings() + j])
        tmp.append(tmp1)
    plot_matrix = np.matrix(tmp)
    #plt.imshow(plot_matrix)
    #plt.imshow(plot_matrix, vmin=0.0, vmax = 1.05, interpolation='none')
    plt.matshow(plot_matrix, cmap='hot')
    plt.colorbar()
    return tmp
        
     
def curve(curve, dates, refDate, rates = False, legend_prefix = '', legend = True, label = None):
    """
    plot a curve
        
    dates: a list where each entry may either be an integer (interpreted as days to maturity starting from refDate, datetimes or ptime-objects)
    refDate: reference date (datetime or ptime)   
    rates: if True, the values from the curve are transtormed to zero rates via r=-ln(value)/t which makes only sense for discoutn curves
    legend: if true, a legend is ploted, otherwise not
    """
    values = []
    refdate = converter.getLTime(refDate)
    ptimes = converter.createPTimeList(refdate, dates)
    for i in range(len(ptimes)):          
        values.append(curve.value(refdate, ptimes[i]))
    daycounter = 'Act365Fixed'
    try:
        daycounter = curve.getDayCounterType()
    except:
        logging.info('Curve does not implement getDayCounterType. using Act365Fixed')
    dc = analytics.DayCounter(daycounter)
    yfValues = analytics.vectorDouble(len(dates))
    dc.yf(yfValues, refdate, ptimes)
    if rates:
        for i in range(len(values)):
            values[i] = -np.log(values[i])/yfValues[i]
    if label is None:
        label = legend_prefix + curve.getObjectId()
    plt.plot(yfValues, values, '-x', label=label)
    plt.title('curves')
    plt.xlabel('ttm')
    plt.ylabel('value')
    if legend:
        plt.legend()
    
def quote_table(quoteTable, env, expiries =[], legendPrefix=''):
    """ 
    plot quotes of the option quote table
    quoteTable EquityOptionQUoteTable
    expiries expiries to plot (given as integer of all expiries), if empty, all expiries are plotted.
    legendPrefix prefix used within the legend
    """    
    quoteExpiries = analytics.vectorPTime()
    quoteTable.getExpiries(quoteExpiries)
    if len(expiries) == 0:
        expiries = range(quoteExpiries.size())
    analytics.calcImpliedVol
    table = dict()
    for i in expiries:
        if i < quoteExpiries.size():
            table[quoteExpiries[i].to_string()] = dict()
            table[quoteExpiries[i].to_string()]['callStrikes'] = []
            table[quoteExpiries[i].to_string()]['callBid'] = []
            table[quoteExpiries[i].to_string()]['callAsk'] = []
            table[quoteExpiries[i].to_string()]['putStrikes'] = []
            table[quoteExpiries[i].to_string()]['putBid'] = []
            table[quoteExpiries[i].to_string()]['putAsk'] = []
                
    strikes = analytics.vectorDouble()
    bid = analytics.vectorDouble()
    ask = analytics.vectorDouble()
    isCall = analytics.vectorBool()
    quoteTable.getQuotes(quoteExpiries, strikes, bid, ask, isCall)
    daycounter = analytics.DayCounter(enums.DayCounter.ACT365_FIXED)
    discount_curve = env.mktman.getDiscountCurve(quoteTable.getIssuer(),  quoteTable.getCurrency(), quoteTable.getSecLevel())
    fwd_curve = env.mktman.getForwardCurve(quoteTable.getUdlId())        
    for i in range(bid.size()):
        if quoteExpiries[i].to_string() in table:
            maturity = daycounter.yf(env.settings.refdate, quoteExpiries[i])
            df = discount_curve.value(env.settings.refdate, quoteExpiries[i])
            fwd = fwd_curve.value(env.settings.refdate, quoteExpiries[i])
            if isCall[i]:
                table[quoteExpiries[i].to_string()]['callStrikes'].append(strikes[i])
                vol_bid = analytics.calcImpliedVol(bid[i], strikes[i], maturity, df, fwd, 'Call')
                table[quoteExpiries[i].to_string()]['callBid'].append(vol_bid)
                vol_ask = analytics.calcImpliedVol(ask[i], strikes[i], maturity, df, fwd, 'Call')
                table[quoteExpiries[i].to_string()]['callAsk'].append(vol_ask)
            else:
                table[quoteExpiries[i].to_string()]['putStrikes'].append(strikes[i])
                vol_bid = analytics.calcImpliedVol(bid[i], strikes[i], maturity, df, fwd, 'Put')
                table[quoteExpiries[i].to_string()]['putBid'].append(vol_bid)
                vol_ask = analytics.calcImpliedVol(ask[i], strikes[i], maturity, df, fwd, 'Put')
                table[quoteExpiries[i].to_string()]['putAsk'].append(vol_ask)
            
    for x, values in table.items():
        plt.plot(values['callStrikes'], values['callBid'], '^', label = legendPrefix + x +':Call Bid')
        plt.plot(values['callStrikes'], values['callAsk'], 'v', label = legendPrefix + x +':Call Ask')
        plt.plot(values['putStrikes'], values['putBid'], '^', label = legendPrefix + x +':Put Bid')
        plt.plot(values['putStrikes'], values['putAsk'], 'v', label = legendPrefix + x +':Put Ask')
    plt.legend()
    plt.xlabel('strikes')
    plt.ylabel('vols')
    plt.title('option quotes')


def vol_series_values(values, value_ids = None, legend = True):
    """
    plots given series values
    values the given values of the vol series
    value_ids list of id of the values to plot (if None, all values are taken)
    """
    #if value_ids isinstance(str):
    #    values_id
    v = values.values
    if value_ids is None:
        value_ids = v.keys()
    for key in value_ids:
        plt.plot(values.values[key], '-x', label = key)
    if legend:
        plt.legend(loc=2,prop={'size':10})


def vol_series_values_returns(values, relative = False, value_ids = None, legend = True):
    """
    plots absolute returns of given series values
    values the given values of the vol series
    relative flag indicating if absolute returns (False or relative returns (True) are used)
    value_ids list of id of the values to plot (if None, all values are taken)
    """
    v = values.values
    if value_ids is None:
        value_ids = v.keys()
    for key in value_ids:
        value = []
        tmp = v[key]
        for i in range(len(tmp)-1):
            if relative:
                value.append(1.0-tmp[i+1]/tmp[i])
            else:
                value.append(tmp[i+1]-tmp[i])
        plt.plot(value,'-x',  label = key)
    if legend:
        plt.legend(loc=2,prop={'size':10})
   
def vol_series_values_hist_returns(values, key = None, relative = False, nBins = 10):
    """
    plot values as histogram
    values the values to be plotted as derived vom analyticsVolUtils.series_values
    relative flag indicating if absolute returns (False or relative returns (True) are used)
    key id of the specific value from the values object to be plotted, if empty, the first entry in values is used
    """
    if key is None:
        key = values.values.keys()[0]
    v = values.values
    value = []
    tmp = v[key]
    for i in range(len(tmp)-1):
        if relative:
            value.append(1.0-tmp[i+1]/tmp[i])
        else:
            value.append(tmp[i+1]-tmp[i])
    #for key, x in v.items():
    n, bins, patches = plt.hist(value, nBins, normed=1, facecolor='blue', alpha=0.75)
    #if legend:
        #   plt.legend()


def vol_series_values_hist(values, key = None, nBins = 10):
    """
    plot values as histogram
    values the values to be plotted as derived vom analyticsVolUtils.series_values
    key id of the specific value from the values object to be plotted, if empty, the first entry in values is used
    """
    if key is None:
        key = values.values.keys()[0]
    v = values.values
    #for key, x in v.items():
    n, bins, patches = plt.hist(v[key], nBins, normed=1, facecolor='blue', alpha=0.75)
 
           

def arbitrage_points(arb_strikes, arb_expiries, arb_type, min_strike, max_strike, max_expiry ):
    if len(arb_strikes) == 0:
        print('No arbitrage.')
        return
    tmp ={}
    for i in range(len(arb_strikes)):
        if arb_type[i] not in tmp.keys():
            tmp[arb_type[i]] = ([],[])
        tmp[arb_type[i]][0].append(arb_strikes[i])
        tmp[arb_type[i]][1].append(arb_expiries[i])
    for k, v in tmp.items():
        plt.plot(v[0], v[1], 'o', label = k)
    plt.xlim([min_strike, max_strike])
    plt.ylim([0.0, max_expiry])
    plt.legend()
    plt.xlabel('x-strikes')
    plt.ylabel('ttm')

def vol(vol, dates, strikes, refDate = None, is_x = True, legend = True, legendPrefix=''):
    """
    plot volatilities for certain strikes and expiries
        
    strikes: strikes where the volatility is evaluated (same for all expiries) can be either in X or in real spot (depending on argument is_x)
    dates: list containing ptimes or integer defininf the expiries (integer refer to days after referenceDate)
    refDate reference date used, if None, the reference date of the volatility surface is used
    i_x if False, the given strikes are interpreted as real strikes and transformed to x_strikes before put into volsurface
    legend true->lengend is ploted
    legendPrefix: will be added as prefix to the legend entries
    """
    if refDate is None:
        refDate = vol.getRefDate()
    refDate = converter.getLTime(refDate)
    ttm = analytics.vectorDouble(len(dates))
    #print(len(dates))
    ptimes = converter.createPTimeList(refDate, dates)
    #print(len(ptimes))
    dc = analytics.DayCounter(vol.getDayCounterType())
    dc.yf(ttm, refDate, ptimes) 
    fwd_curve = vol.getForwardCurve()
    for i in range(len(ptimes)):
        values = []
        x = []
        fwd = fwd_curve.value(refDate, ptimes[i])
        discount_cash_div = fwd_curve.discountedFutureCashDivs(refDate, ptimes[i])
        for j in range(len(strikes)):
            strike = strikes[j]
            xstrike = strikes[j]
            if is_x:
                strike = analytics.computeRealStrike(xstrike, fwd, discount_cash_div)
            else:
                xstrike = analytics.computeXStrike(strike, fwd, discount_cash_div)
            values.append(vol.calcImpliedVol(refDate, ptimes[i], xstrike)) #.append( curve.value(refDate, dates[i]) )
            x.append(strike)
        plt.plot(x, values,'-x', label = legendPrefix + 'ttm='+str(round(ttm[i],2)))
    plt.title('volatilities per expiry')
    plt.xlabel('strike')
    plt.ylabel('implied volatility')   
    if legend:
        plt.legend()
    #X,Y=np.meshgrid(x, values)
        

def vol_surface(vol, dates, xstrikes, refDate):
    """
    plot volatilities as a surface (3D)
        
    xStrikes: xstrikes where the volatility is evaluated (same for all expiries)
    dates: list containing ptimes or integer defining the expiries (integer refer to days after referenceDate)
    legendPrefix: will be added as prefix to the legend entries
    """
    #refDate = utils.getLTime(refDate)
    ttm = analytics.vectorDouble(len(dates))
    ptimes = converter.createPTimeList(refDate, dates)
    # print(len(ptimes))
    dc = analytics.DayCounter(vol.getDayCounterType())
    dc.yf(ttm, refDate, ptimes)
    times = []
    vol_surf = np.empty([len(ptimes), len(xstrikes)])
    for t in ttm:
        times.append(t)
    for i in range(len(ptimes)):
        values = []
        for j in range(len(xstrikes)):
            vol_surf[i,j] = vol.calcImpliedVol(refDate, ptimes[i], xstrikes[j]) 
    X,Y = np.meshgrid( xstrikes, times)
    plt.pcolor(X, Y, vol_surf)
    plt.colorbar()
    plt.xlabel('x-strike')
    plt.ylabel('ttm')
    return X, Y, vol_surf
    
    
def plotZSpread(trans_matrix, recovery, riskfree_df, instrument_factory, coupon, ratings):
    zero_bonds = []
    #ratings = analytics.Rating.getRatings()
    pricing_request = analytics.PricingRequest()
    ttms = []
    for ttm in range(20):
        zero_bonds.append(instrument_factory.createFixedBond('TestIssuer', 'COLLATERALIZED', 0, (ttm+1)*365, 'A', coupon, 100, 'EUR'))      
        ttms.append(ttm+1)
    refDate = instrument_factory.mktFactory.getRefDate()
    for i in range(len(ratings)):
        rating = ratings[i]
        r = analytics.Rating('test', analytics.ptime(2000,1,1,0,0,0), rating)
        zSpread = []
        for bond in zero_bonds:
            results = analytics.PricingResults()
            analytics.BondPricer.price(results, refDate, bond, riskfree_df, r, trans_matrix, recovery, pricing_request)
            zSpread.append(analytics.BondPricer.computeZSpread(refDate, bond, riskfree_df, results.getPrice(), False, 300))        
        plt.plot(ttms, zSpread, '-x', label=rating)
    plt.title('z spread')
    plt.xlabel('ttm')
    plt.ylabel('z spread')
    plt.legend()
               
