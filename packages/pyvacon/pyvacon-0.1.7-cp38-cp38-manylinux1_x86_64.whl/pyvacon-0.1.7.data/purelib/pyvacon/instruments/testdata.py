# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
import pyvacon.analytics as analytics
import pyvacon.tools.enums as enums
import pyvacon.tools.converter as converter
import pyvacon.marketdata.testdata as mkt_testdata


    
class DOP:
    def __create_put_payoff__(strike):
        xPoints = analytics.vectorDouble(3)
        pPoints = analytics.vectorDouble(3)
        xPoints[0] = 0
        xPoints[1] = strike
        xPoints[2] = strike +1
        pPoints[0] = strike
        pPoints[1] = 0
        pPoints[2] = 0
        result = analytics.PayoffStructure(xPoints, pPoints)
        return result
    
    def __create_barrier_schedule__(expiry, level,rebate, refdate):
        refdate = converter.getLTime(refdate)
        rebatePayoff = analytics.PayoffStructure(rebate)
        barrierPayoff = analytics.BarrierPayoff('', analytics.ptime(), rebatePayoff)
        downBarrier = analytics.BarrierDefinition(refdate, expiry, barrierPayoff, level, True)
        result = analytics.BarrierSchedule()
        result.addDownBarrier(downBarrier)
        return result
       
    def __create_DOP__(spot, currency, rel_expiry, rel_level, rel_strike, rel_rebate, udl, refdate, barrierStart = 0):
        name = 'DOP:' + udl + ':' + str(rel_expiry) + ':' + str(rel_level) + ':' + str(rel_strike) + ':' +  str(rel_rebate)
        expiry = analytics.ptime()
        refdate.addDays(expiry, rel_expiry) 
        payoff = DOP.__create_put_payoff__(rel_strike*spot)
        barrierSchedule = DOP.__create_barrier_schedule__(expiry, rel_level*spot, rel_rebate*spot, refdate)
        result = analytics.BarrierSpecification(name, udl, "COLLATERALIZED", currency, udl, expiry, barrierSchedule, payoff)
        return result
    
    def all_data(env):
        pass
    
    
class European:
    rel_strikes = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
    rel_expiries =[5, 365, 4*365]
    
    def call(env):
        for udl, currency in mkt.Equity.equity_udls.items():
            for rel_strike in European.rel_strikes:
                for rel_expiry in European.rel_expiries:
                    expiry = analytics.ptime()
                    env.settings.refdate.addDays(expiry, rel_expiry)
                    spot = env.mktman.getSpot(udl)
                    name = 'CALL:' + udl +':' + str(rel_expiry) +':' + str(rel_strike)
                    result = analytics.EuropeanVanillaSpecification(name, udl, 'COLLATERALIZED', currency, udl, 'Call', expiry, spot*rel_strike)    
                    env.handler.specifications[name] = result
    def put(env):
        for udl, currency in mkt.Equity.equity_udls.items():
            for rel_strike in European.rel_strikes:
                for rel_expiry in European.rel_expiries:
                    expiry = analytics.ptime()
                    env.settings.refdate.addDays(expiry, rel_expiry)
                    spot = env.mktman.getSpot(udl)
                    name = 'PUT:' + udl +':' + str(rel_expiry) +':' + str(rel_strike)
                    result = analytics.EuropeanVanillaSpecification(name, udl, 'COLLATERALIZED', currency, udl, 'Put', expiry, spot*rel_strike)
                    env.handler.specifications[name] = result
                    
    def all_data(env):
        European.call(env)
        European.put(env)
        
        
class Bonds:      
#    Issuers = {'EON': ['AAA', 'GER', 'UTILITY'],
#              'RWE' : ['AA', 'GER','UTILITY'],
#              'ENBW': ['A', 'GER','UTILITY']}
    SecLevels =[enums.SecuritizationLevel.COLLATERALIZED, enums.SecuritizationLevel.EQUITY, enums.SecuritizationLevel.MEZZANINE, enums.SecuritizationLevel.SENIOR_SECURED, enums.SecuritizationLevel.SENIOR_UNSECURED]
    BondExpiries=[10, 365, 5*365, 10*365]
    BondDayCounters = ['ACT365FIXED']
    CouponFrequencies = ['A', 'SA']
    
    def plain_vanilla(env, as_callable = False):
        """
        add plain vanilla fixed coupon bonds (non-callable) either as Bonds or Callable Bonds
        
        env environment where instruments are added
        as_callable if true, instruments will be created as callable with no call dates
        """
        coupon = 0.05
        notional = 1.0
        refdate = env.settings.refdate
        issue_date = utils.getLTime(-180,refdate)
        tag = ':PV:'
        if as_callable == True:
            tag = ':PV_AS_CALLABLE:'
        for issuer, value in mkt.Credit.Issuers.items():
            for seclvl in Bonds.SecLevels:
                for daycounter in Bonds.BondDayCounters:
                    for coupon_freq in Bonds.CouponFrequencies:
                        for expiry in Bonds.BondExpiries:
                            spec_id = issuer+tag + seclvl +':' + str(expiry) + ':' + coupon_freq + ':' +daycounter
                            if as_callable == False:
                                env.handler.specifications[spec_id] = analytics.BondSpecification(spec_id, issuer, 
                                                 seclvl, 'EUR',
                                                 utils.getLTime(expiry,refdate),
                                                 issue_date,
                                                notional, daycounter, 
                                                coupon_freq, coupon)
                            else:
                                 env.handler.specifications[spec_id] = analytics.CallableBondSpecification(spec_id, issuer, 
                                                 seclvl, 'EUR',
                                                 utils.getLTime(expiry,refdate),
                                                 issue_date,
                                                notional, daycounter, 
                                                coupon_freq, coupon)
                                                
    def plain_vanilla_floater(env):
        spread = 0.05
        notional = 1.0
        refdate = env.settings.refdate
        issue_date = utils.getLTime(-180,refdate)
        for issuer, value in mkt.Credit.Issuers.items():
            for seclvl in Bonds.SecLevels:
                for daycounter in Bonds.BondDayCounters:
                    for coupon_freq in Bonds.CouponFrequencies:
                        for expiry in Bonds.BondExpiries:
                            spec_id = issuer+':FLOATER'+':' + seclvl +':' + str(expiry) + ':' + coupon_freq + ':' +daycounter
                            env.handler.specifications[spec_id] = analytics.BondSpecification(spec_id, issuer, 
                                                 seclvl, 'EUR',
                                                 utils.getLTime(expiry,refdate),
                                                 issue_date,
                                                notional, daycounter, 
                                                coupon_freq, 'EUR12M', spread)
                                        
    def all_data(env):
        Bonds.plain_vanilla(env, False)
        Bonds.plain_vanilla(env, True)
        Bonds.plain_vanilla_floater(env)

def all_data(env):
    DOP.all_data(env)
    European.all_data(env)
    Bonds.all_data(env)