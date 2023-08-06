# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
from datetime import datetime, timedelta
import math
import numpy as np
import pyvacon

from pyvacon import utils
import pyvacon.tools as tools
import pyvacon.tools.enums as analyticsEnums
#import pyvacon.tools.converter as utils

class Equity:
    equity_udls = {'DBK' : 'EUR' , 'EON':'EUR'}        
    def udls(env):
        for udlId, currency in Equity.equity_udls.items():
            udl = analytics.EquityUnderlying(udlId)
            udl.borrowKey = udlId+'_BC'
            udl.divKey = udlId+'_DIV'
            udl.fullName = udlId
            udl.issuerId = udlId
            udl.volDc = 'ACT365Fixed'
            udl.volKey = udlId + '_VOL'
            udl.quoteKey = udlId+'_SPOT'
            udl.setCurrency(currency)
            env.handler.env_cache.addObject(udl)
            
    udl_spots = {'DBK': 100, 'EON': 110}
    
    def spots(env):
        refdate = utils.getLTime(env.settings.refdate)
        for udl, spot in Equity.udl_spots.items():
            env.handler.spot_cache.addReferenceSpot(udl, refdate, spot)
        
    def __create_div__(udl, div, refdate):
        exDates = utils.relativeToAbsolute(refdate, div['exDates'])
        payDates = utils.relativeToAbsolute(refdate, div['payDates'])
        cashDivs = []
        for v in div['cashDivs']:
            cashDivs.append(Equity.udl_spots[udl] * v)
        yieldDivs = div['yieldDivs']
        taxFactors = div['taxFactors']
        return analytics.DividendTable(udl+'_DIV', refdate, exDates, yieldDivs, cashDivs, taxFactors, payDates) 
  
    div_tables = {'EON': {'exDates': [1, 365, 2*365, 3*365], 'payDates' : [1, 365, 2*365, 3*365],'cashDivs': [0.0, 0.0, 0.0, 0.0], 'yieldDivs':[0.05,0.05,0.05,0.05], 'taxFactors':[0,0,0,0]},
                  'DBK': {'exDates': [1, 365+100, 2*365+100, 3*365+100], 'payDates' : [1, 365+100, 2*365+100, 3*365+100],'cashDivs': [0.05, 0.05, 0.05, 0.5], 'yieldDivs':[0,0,0,0], 'taxFactors':[0,0,0,0]}}
    def div(env):
        for udl, div in Equity.div_tables.items():
            result = Equity.__create_div__(udl, div, env.settings.refdate)
            env.handler.mkt_cache.addObject(result)
            
    
    borrows = {'DBK': {'dates': [2, 5], 'rates': [0.03, 0.03] },
               'EON': {'dates': [2, 5], 'rates': [0.0, 0.0] }}
    def __create_borrow__(udl, bc, refdate, rates_key = 'rates', dates_key = 'dates'):
        daycounter = utils.DayCounter('ACT365Fixed')
        dates = utils.relativeToAbsolute(refdate, bc[dates_key])
        rates = bc[rates_key]
        values = []
        for i in range(len(dates)):
            values.append(math.exp(-rates[i]*daycounter.yf(refdate, dates[i])))
        result = analytics.DiscountCurve(udl+'_BC', refdate, dates, values,'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
        return result
    
            
    def borrow(env):
        refdate = utils.getLTime(env.settings.refdate)
        for udl, bc in Equity.borrows.items():
            borrow = Equity.__create_borrow__(udl, bc, refdate)
            env.handler.mkt_cache.addObject(borrow)
    
        
    vols = {'EON': {'expiries': [10, 100, 365, 730], 'atmVols': [0.2, 0.25, 0.28, 0.3], 'rho':-0.65, 'eta':0.8, 'gamma': 0.5} ,
                    'DBK': {'expiries': [10, 100, 365, 730], 'atmVols': [0.3, 0.3, 0.28, 0.27], 'rho':-0.65, 'eta':0.8, 'gamma': 0.4}}
            
    def __create_SSVI__(fwd, expiries, atmFVols, rho, eta, gamma, udl, refdate):
        key = udl + '_VOL'
        param = analytics.VolatilityParametrizationSSVI(expiries, atmFVols, rho, eta, gamma)
        vol = analytics.VolatilitySurface(key, refdate, fwd, 'ACT365Fixed', param)
        return vol 
     
    def vol(env):
        for udl, vol in Equity.vols.items():
            fwd = env.mktman.getForwardCurve(udl)
            yf = [x / 365.0 for x in vol['expiries']]
            result = Equity.__create_SSVI__(fwd, yf, vol['atmVols'], vol['rho'], vol['eta'], vol['gamma'], udl, env.settings.refdate)
            env.handler.mkt_cache.addObject(result)
            
    issuer_discount = {'DBK': [['COLLATERALIZED', 'EUR', 'EONIA', '']], 
                       'EON': [['COLLATERALIZED', 'EUR', 'EONIA', '']],
                        'EUREX': [['COLLATERALIZED', 'EUR', 'EONIA', '']]}
                        
    def issuer_to_discount(env):
        for udl, mapping in Equity.issuer_discount.items():
            for m in mapping:
                env.handler.mkt_cache.addDiscountMapping(udl, m[0], m[1], m[2], m[3])
                
    
    def __create_european_quote_table__(udl, issuer, currency, vol, discount_curve, refdate):

        quote_table_xstrikes = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        expiries = [30, 60, 180, 365, 2*365, 3*365, 4*365]
        refdate = utils.getLTime(refdate)
        fwd = vol.getForwardCurve()
        spot =  fwd.value(refdate, refdate)
        quoteTable = analytics.EquityOptionQuoteTable('QUOTE_TABLE:'+udl, refdate, spot, udl, issuer, "COLLATERALIZED", currency)
        daycounter = utils.DayCounter(analyticsEnums.DayCounter.ACT365_FIXED)
        ptimes = utils.createPTimeList(refdate, expiries)
        isCall = []
        for j in range(len(quote_table_xstrikes)):
            if quote_table_xstrikes[j] < 1.0:
                isCall.append(False)
            else:
                isCall.append(True)
        for i in range(len(ptimes)):
            bid =[]
            ask = []
            discount = discount_curve.value(refdate, ptimes[i])
            forward_value = fwd.value(refdate, ptimes[i])
            disc_future_cash_div = fwd.discountedFutureCashDivs(refdate, ptimes[i])
            maturity = daycounter.yf(refdate, ptimes[i])
            strikes = []
            for X in quote_table_xstrikes:
                strikes.append(analytics.computeRealStrike(X, forward_value, disc_future_cash_div))
            for j in range(len(quote_table_xstrikes)):
                price = 0
                impl_vol = vol.calcImpliedVol(refdate, ptimes[i], quote_table_xstrikes[j])
                if isCall[j]:
                    price = analytics.calcEuropeanCallPrice(strikes[j], maturity, discount, forward_value, impl_vol )  
                else:
                    price = analytics.calcEuropeanPutPrice(strikes[j], maturity, discount, forward_value, impl_vol ) 
                bid.append( 0.95 * price )
                ask.append( 1.05 * price )
            quoteTable.addQuotes(ptimes[i], True, strikes, isCall, bid, ask)
        return quoteTable
    
    def quote_tables(env):
        issuer = 'EUREX'
        securitization = analyticsEnums.SecuritizationLevel.COLLATERALIZED
        for udl, currency in Equity.equity_udls.items():
            discount_curve = env.mktman.getDiscountCurve(issuer, currency, securitization)
            vol = env.mktman.getVolatilitySurface(udl)
            quote_table = Equity.__create_european_quote_table__(udl, issuer, currency, vol, discount_curve, env.settings.refdate)
            env.handler.mkt_cache.addObject(quote_table)
    
    def all_data(env):
        Equity.udls(env)   
        Equity.spots(env)
        Equity.borrow(env)
        Equity.div(env)
        Equity.vol(env)
        Equity.issuer_to_discount(env)
        Equity.quote_tables(env)
               
        
class Credit:
    
    @staticmethod
    def create_transition_matrix(refDate, obj_id,  downgrade_prob = 0, upgrade_prob = 0, default_prob = 0.015):
        '''
        create a simple (tridiagonal + default) transition matrix for testing
        
        '''
        transition = analytics.RatingTransition(obj_id, refDate)
        #transition = analytics.TimeScaledRatingTransition(obj_id, refDate,1.0)
        
        ratings = analytics.Rating.getRatings();
        
        for i in range(len(ratings)-1):
            #diagonal part
            if i > 0:
                transition.setEntry(i,i, 1.0 - i*default_prob - upgrade_prob - downgrade_prob)
                transition.setEntry(i,i-1,upgrade_prob)
            else:
                 transition.setEntry(i,i, 1.0 - i*default_prob - downgrade_prob)
            if i+1 != len(ratings)-1:
                transition.setEntry(i,i+1, downgrade_prob)
                transition.setEntry(i,len(ratings)-1, i*default_prob)
            else:
                transition.setEntry(i,len(ratings)-1, i*default_prob + downgrade_prob)
                
        for i in range(len(ratings)-1):
            transition.setEntry(len(ratings)-1, i, 0.0)
        transition.setEntry(len(ratings)-1,len(ratings)-1,1.0)
        
        return transition
    
    @staticmethod
    def create_random_transition_matrix():
        n_ratings = len(analytics.Rating.getRatings())
        trans = np.zeros([n_ratings, n_ratings])
        len_default_prob = 1.0/n_ratings
        x = np.arange(-50.0,50.01,100.0/n_ratings)
        for i in range(n_ratings-1):
            default_prob = np.random.uniform(i*len_default_prob, (i+1)*len_default_prob)
            var = np.random.uniform(0.01, 0.10)
            sum_prob = 0
            for j in range(n_ratings-1):
                dist = (x[i]-x[j])*(x[i]-x[j])
                trans[i,j] = math.exp(-var*dist)
                sum_prob += trans[i,j]
            for j in range(n_ratings-1):
                trans[i,j] = (1.0 - default_prob)* trans[i,j]/sum_prob
            trans[i,n_ratings-1] = default_prob
        trans[n_ratings-1,n_ratings-1] = 1.0
        return trans


    TransitionMatrices = { 
            'Moodys95':[
                    [0.918970, 	0.073850, 	0.007180,	0.0, 	0.0, 	0.0,	0.0, 0.0],
                    [0.011310,	0.912640,	0.070910,	0.003080,	0.002060,	0.0,	0.0,	0.0],
                    [0.001020,	0.025610,	0.911890,	0.053280,	0.006150,	0.002050,	0.0, 0.0],
                    [0.0,	0.002060,	0.053610,	0.879380,	0.054640,	0.008250,	0.001030,	0.001030],
                    [0.0,	0.001060,	0.004250,	0.049950,	0.851220,	0.073330,	0.004250,	0.015940],
                    [0.0,	0.001090,	0.001090,	0.005420,	0.059720,	0.821930,	0.021720,	0.089030],
                    [0.0,	0.004370,	0.004370,	0.008730,	0.025110,	0.058950,	0.677950,	0.220520],
                    [0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	0.0,	1.0]
                    ]
            }
    
    @staticmethod
    def transtion_matrix(refdate, name):
        if name not in Credit.TransitionMatrices.keys():
            raise('Transition matrix with name ' + name + ' does not exist in testdata')
        transition = pyvacon.marketdata.RatingTransition(name, refdate)
        matrix = Credit.TransitionMatrices[name]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                transition.setEntry(i,j, matrix[i][j])
        return transition
    
    @staticmethod            
    def create_survival_curve(refdate, hazard_rate, obj_id):
        '''
        creates a survival curve with constant hazard rate
        '''
        dates = analytics.vectorPTime(2)
        dates[0] = utils.getLTime(refdate)
        utils.getLTime(refdate).addDays(dates[1], 30*365)
        values = analytics.vectorDouble(2)
        values[0] = hazard_rate
        values[1] = hazard_rate
        return analytics.SurvivalCurve(obj_id, refdate, dates, values, True)
        
    recoveries = {analyticsEnums.SecuritizationLevel.COLLATERALIZED: {'dates' : [1,2], 'recovery' : [1.0,1.0]},
                analyticsEnums.SecuritizationLevel.SENIOR_SECURED:  {'dates' : [1,2], 'recovery' : [0.8,0.8]},
                analyticsEnums.SecuritizationLevel.SENIOR_UNSECURED: {'dates' : [1,2], 'recovery' : [0.7,0.7]},
                analyticsEnums.SecuritizationLevel.SUBORDINATED: {'dates' : [1,2], 'recovery' : [0.5,0.5]},
                  analyticsEnums.SecuritizationLevel.MEZZANINE:  {'dates' : [1,2], 'recovery' : [0.4,0.4]},
                    analyticsEnums.SecuritizationLevel.EQUITY:    {'dates' : [1,2], 'recovery' : [0.3,0.3]}
                                      }
    @staticmethod
    def __create_recovery__(refdate, identifier, obj_id):
#        recoveries = {}
#        recoveries[analyticsEnums.SecuritizationLevel.COLLATERALIZED] = {'dates' : [1,2], 'recovery' : [0.9,0.9]}
#        recoveries[analyticsEnums.SecuritizationLevel.SENIOR_SECURED] = {'dates' : [1,2], 'recovery' : [0.8,0.8]}
#        recoveries[analyticsEnums.SecuritizationLevel.SENIOR_UNSECURED] = {'dates' : [1,2], 'recovery' : [0.7,0.7]}
#        recoveries[analyticsEnums.SecuritizationLevel.SUBORDINATED] = {'dates' : [1,2], 'recovery' : [0.5,0.5]}
#        recoveries[analyticsEnums.SecuritizationLevel.MEZZANINE] = {'dates' : [1,2], 'recovery' : [0.4,0.4]}
#        recoveries[analyticsEnums.SecuritizationLevel.EQUITY] = {'dates' : [1,2], 'recovery' : [0.3,0.3]}
        recovery = Credit.recoveries[identifier]
        dates = [refdate + timedelta(days=x) for x in recovery['dates']]
        values = recovery['recovery']
        dc = pyvacon.marketdata.DatedCurve(obj_id, utils.getLTime(refdate), dates, values,'ACT365Fixed', 'LINEAR', 'LINEAR')
        return dc

    @staticmethod
    def create_recovery(refdate, sec_lvl, obj_id):
       return Credit.__create_recovery__(refdate, sec_lvl, obj_id)
    
    @staticmethod
    def create_issuers(n_issuers, refdate):
        issuers = {}

        for i in range(n_issuers):
            r = analytics.Rating.getRatings()[np.random.randint(0, len(analytics.Rating.getRatings())-1)]
            rating = analytics.Rating('', refdate, r)
            issuers['Issuer_' + str(i)] = analytics.Issuer('Issuer_' + str(i), 'Issuer', rating, 'GER', 'UTILITIES')
        return issuers

    Issuers = {'EON': ['AAA', 'GER', 'UTILITY'],
              'RWE' : ['AA', 'GER','UTILITY'],
                'ENBW': ['A', 'GER','UTILITY'],
                'DBK' : ['B', 'GER', 'FINANCIALS'],
                'CBK' : ['BB', 'GER', 'FINANCIALS'],
                'KFW' : ['AAA', 'GER','FINANCIALS'],
                'EDF': ['B-','FRA','UTILITY'],
                'BMW' :['A','GER','INDUSTRIALS'],
                'COCA_COLA':['B','USA', 'INDUSTRIALS'],
                'GE':['AA','USA','INDUSTRIALS']
                }
   
    
    
    SecLevels =[analyticsEnums.SecuritizationLevel.COLLATERALIZED, analyticsEnums.SecuritizationLevel.EQUITY, analyticsEnums.SecuritizationLevel.MEZZANINE, analyticsEnums.SecuritizationLevel.SENIOR_SECURED, analyticsEnums.SecuritizationLevel.SENIOR_UNSECURED]
    BondExpiries=[10, 365, 5*365, 10*365]
    BondDayCounters = ['ACT365FIXED']
    CouponFrequencies = ['A', 'SA']

    @staticmethod
    def all_data(env):
        mapping = analytics.IssuerToCreditMapping()
        recov_ids = set()
        recov_ids
        refdate = env.settings.refdate
        # add issuer and transition
        for key, values in Credit.Issuers.items():
            rating = analytics.Rating(values[0],utils.getLTime(refdate),values[0])  
            issuer = analytics.Issuer(key, key, rating, values[1], values[2])
            env.handler.mkt_cache.addObject(issuer)
            transition_id = mapping.getTransitionId(issuer)
            #print(transition_id)
            transition = Credit.create_transition_matrix(refdate, 0, transition_id)
            env.handler.mkt_cache.addObject(transition)
            #survival_id = mapping.getSurvivalId(issuer)
            #survival = transition.computeSurvivalCurve(refdate, rating, survival_id)
            #env.handler.mkt_cache.addObject(survival)
            for sec_lvl in Credit.SecLevels:
                # add transitions and recoveries
                recovery_id = mapping.getRecoveryId(issuer, 'EUR', sec_lvl)
                recovery = Credit.__create_recovery__(refdate, sec_lvl, recovery_id)
                env.handler.mkt_cache.addObject(recovery)
            
        env.handler.mkt_cache.addObject(mapping)
 



class _MarktDataObjectGenerator:
    def __init__(self, creator_f, spec):
            self._spec = spec
            self.description = ''
            if 'description' in spec.keys():
                self.description = spec['description']
            else:
                self.description = 'No description available.'
            self._creator_f = creator_f

    def __call__(self, refdate):
        return self._creator_f(refdate, self._spec)

class _MarketDataGenerator:
    def __init__(self, creator_f, specs):
        for x in specs:
            tmp =  _MarktDataObjectGenerator(creator_f, x)
            if 'ID' not in x.keys():
                raise Exception('The market data objct specification does not contain a key.')
            setattr(self, x['ID'], tmp)
    
def _discount_curve_generator(refdate, spec):
    dates = [refdate + timedelta(days=x) for x in  spec['dates']]
    rates = spec['rates']
    values = [] 
    daycounter = utils.DayCounter('ACT365Fixed')
    for i in range(len(dates)):
        values.append(math.exp(-rates[i]*daycounter.yf(refdate, dates[i])))
    dc = pyvacon.marketdata.DiscountCurve(spec['ID'], refdate, dates, values,'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
    return dc
    

_ir_curves = [ {'ID': 'EONIA', 
                'dates': [1, 10*365], 
                'rates': [0.001, 0.0015]
                }, 
               {
                   'ID': 'EUR6M', 
                   'dates': [1, 10*365], 
                   'rates': [0.01, 0.015]
               },  
              {
                  'ID': 'EUR12M', 
                  'dates': [1, 10*365], 
                  'rates': [0.012, 0.02]
              },
              {
                  'ID': 'FLAT_ZERO', 
                  'dates': [1, 10*365], 
                  'rates': [0.0, 0.0]
              }
              ]


    
def _ir_udl_generator(refdate, spec):
    return pyvacon.analytics.IrUnderlying(spec['ID'], 
                                  spec['discount_curve'], 
                                  spec['period'], spec['daycounter'], 
                                  spec['rollconvention'])
    

_ir_udls = [{
       'ID':'EUR6M', 
       'discount_curve': 'EUR6M', 
       'period': analyticsEnums.Period.SA, 
       'daycounter': analyticsEnums.DayCounter.ACT365_FIXED, 
       'rollconvention': analyticsEnums.RollConvention.UNADJUSTED},
       {
       'ID':'EUR12M', 
       'discount_curve': 'EUR12M', 
       'period': analyticsEnums.Period.SA, 
       'daycounter': analyticsEnums.DayCounter.ACT365_FIXED, 
       'rollconvention': analyticsEnums.RollConvention.UNADJUSTED
       },
        {
       'ID':'EONIA', 
       'discount_curve': 'EONIA', 
       'period': analyticsEnums.Period.SA, 
       'daycounter': analyticsEnums.DayCounter.ACT365_FIXED, 
       'rollconvention': analyticsEnums.RollConvention.UNADJUSTED
       }
       ]


class _InterestRate:  
    @staticmethod
    def _get_curve(key, refdate):
        discountCurve = InterestRate.ir_curves[key]
        dates = [refdate + timedelta(days = x) for x in discountCurve['dates']]
        rates = discountCurve['rates']
        values = [] 
        daycounter = utils.DayCounter('ACT365Fixed')
        for i in range(len(dates)):
            values.append(math.exp(-rates[i]*daycounter.yf(refdate, dates[i])))
        if False:
            return _InterestRate.DiscountCurve(key, refdate, dates, values,'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
        else:
            return pyvacon.marketdata.DiscountCurve(key, refdate, dates, values,'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
        return dc
        
    CurrencyToIrUnderlying = {'EUR': 'EONIA'}
    
    def curves(env):
        daycounter = utils.DayCounter('ACT365Fixed')
        refdate = env.settings.refdate
        for key, value in InterestRate.ir_curves.items():
            discountCurve = value
            dates = utils.relativeToAbsolute(refdate, discountCurve['dates'])
            rates = discountCurve['rates']
            values = []
            for i in range(len(dates)):
                values.append(math.exp(-rates[i]*daycounter.yf(refdate, dates[i])))
            dc = analytics.DiscountCurve(key, refdate, dates, values,'ACT365Fixed', 'LINEARLOG', 'LINEARLOG')
            env.handler.mkt_cache.addObject(dc)
        mapping = analytics.DefaultCurrencyMapping()
        for key, value in InterestRate.CurrencyToIrUnderlying.items():
            mapping.addMapping(key,value)
        env.handler.mkt_cache.addObject(mapping)

    def udls(env):
        eur_6M = pyvacon.analytics.IrUnderlying('EUR6M', 'EUR6M', analyticsEnums.Period.SA, analyticsEnums.DayCounter.ACT365_FIXED, analyticsEnums.RollConvention.UNADJUSTED) 
        env.handler.mkt_cache.addObject(eur_6M)
        eur_12M = pyvacon.analytics.IrUnderlying('EUR12M', 'EUR12M', analyticsEnums.Period.SA, analyticsEnums.DayCounter.ACT365_FIXED, analyticsEnums.RollConvention.UNADJUSTED)
        env.handler.mkt_cache.addObject(eur_12M)
        eonia = pyvacon.analytics.IrUnderlying('EONIA', 'EONIA', analyticsEnums.Period.SA, analyticsEnums.DayCounter.ACT365_FIXED, analyticsEnums.RollConvention.UNADJUSTED) 
        env.handler.mkt_cache.addObject(eonia)    
        
    def all_data(env):
        InterestRate.curves(env)
        InterestRate.udls(env)
      
class InterestRate:
    Curves = _MarketDataGenerator(_discount_curve_generator, _ir_curves)
    Underlyings = _MarketDataGenerator(_ir_udl_generator, _ir_udls)



class _Inflation:
    _curves = {'CPI': {'start_index': 104.0, 'monthly_inflation_rate': 1.001, 'description' : 'Inflation curve with start index 104 and constant monthly inflation rate of 1.001'},
               'ZERO': {'start_index': 100.0, 'monthly_inflation_rate': 1.00, 'description' : 'Inflation curve with start index 100 and no inflation.'},
               'DEFLATION': {'start_index': 100.0, 'monthly_inflation_rate': 0.99},}

    class _InflationIndexForwardGenerator:
        def __init__(self, key, curve_definition):
            self._curve_definition = curve_definition
            self._key = key
            if 'description' in curve_definition.keys():
                self.description = curve_definition['description']

        def __call__(self, refdate):
            def get_next_month(any_day):
                return any_day.replace(day=28) + timedelta(days=4)
            if 'start_index' in  self._curve_definition.keys():
                dates=[refdate]
                values = [self._curve_definition['start_index']]
                for i in range(60):
                    dates.append(get_next_month(dates[-1]))
                    values.append(values[-1]*self._curve_definition['monthly_inflation_rate'])
                dates = utils.createPTimeList(refdate, dates)
                return pyvacon.marketdata.InflationIndexForwardCurve(self._key, dates[0], dates, values, 'GERMAN')
            raise Exception('Cannot create curve due to strange error.')
    
    def __init__(self):
        for k,v in _Inflation._curves.items():
            setattr(self, k, _Inflation._InflationIndexForwardGenerator(k,v))
    
Inflation = _Inflation()

class Parameter: 
    def all_data(env):
        param = analytics.BondPricingParameter('BondPricingParameter')
        param.useJLT = True
        env.handler.param.addObject(param)
        env.params.setPricerType(analyticsEnums.ProductType.CALLABLE_BOND,analyticsEnums.PricerType.PDE)
        env.params.setPricerType(analyticsEnums.ProductType.BOND,analyticsEnums.PricerType.ANALYTIC)
        param_callable = analytics.CallableBondPdePricingParameter()
        env.handler.param.addObject(param_callable)
    
    
def all_data(env):
    InterestRate.all_data(env)
    Equity.all_data(env)
    #Credit.all_data(env)   
    Parameter.all_data(env)
    