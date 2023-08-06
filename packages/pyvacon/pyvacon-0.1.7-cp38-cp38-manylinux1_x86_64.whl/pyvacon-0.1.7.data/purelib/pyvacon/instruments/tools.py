# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
import pandas as pd
import pyvacon.analytics as analytics
import pyvacon.tools.enums as enums
import pyvacon.tools.converter as converter

def create_wof_dop(refdate, udl_with_weights, days_to_maturity, barrier_level, strike, rebate, id = 'WOF_DOP', 
                   issuer = 'Test_Issuer', sec_lvl = enums.SecuritizationLevel.NONE, currency = 'EUR'):
    """
    Create a worst-of down&out put
    refdate reference date
    udl_with_weights list of tuples with weights (first) and underlying-ids
    days_to_maturity number of days to maturity (from refdate on)
    barrier_level absolut barier level
    strike absolute strike
    rebate amount paid at barrier hit
    """

    # the down&out barrier
    refdate = converter.getLTime(refdate)
    barrier_specs = analytics.vectorRainbowBarrierSpec(2)
    expiry = converter.getLTime(days_to_maturity,refdate)
    barrier_start = refdate
    barrier_end = expiry
    obs_dates = analytics.vectorPTime()
    lower_level = -100000
    upper_level = barrier_level
    udl_id = 0
    # switch of the final "payoff" barrier if barrier is hit
    barrier_num = analytics.vectorInt(1)
    barrier_num[0] = 1
    barrier_status = analytics.vectorBool(1)
    barrier_status[0] = False
    is_active = True
    hit_payoff_points = analytics.vectorDouble([0.0, 800000.0])
    hit_payoff_values = analytics.vectorDouble([rebate, rebate])
    no_hit_payoff_points = analytics.vectorDouble()
    no_hit_payoff_values = analytics.vectorDouble()
    paydate = analytics.ptime(2000,1,1,0,0,0) #if paydate < startdate, then payoff is at hit
    barrier_specs[0] = analytics.RainbowBarrierSpec(barrier_start, barrier_end, obs_dates, lower_level, upper_level, udl_id, 
                                                barrier_num, barrier_status, is_active, hit_payoff_points, hit_payoff_values, 
                                                  no_hit_payoff_points,  no_hit_payoff_values, paydate)
    # barrier for final payoff
    barrier_start = expiry
    barrier_end = expiry
    obs_dates = analytics.vectorPTime()
    lower_level = -10000000 #determine barrier levels so that barrier is hit with probability 1
    upper_level = 100000000
    udl_id = 0
    strike = 100
    barrier_num = analytics.vectorInt()
    barrier_status = analytics.vectorBool()
    hit_payoff_points = analytics.vectorDouble([0, strike, strike+1000000])
    hit_payoff_values = analytics.vectorDouble([0,0, 1000000])
    no_hit_payoff_points = analytics.vectorDouble()
    no_hit_payoff_values = analytics.vectorDouble()
    paydate = expiry
    barrier_specs[1] = analytics.RainbowBarrierSpec(barrier_start, barrier_end, obs_dates, lower_level, upper_level, udl_id, 
                                                barrier_num, barrier_status, is_active, hit_payoff_points, hit_payoff_values, 
                                                  no_hit_payoff_points,  no_hit_payoff_values, paydate)
    # basket specification
    udls = analytics.vectorRainbowUdlSpec(1)
    basket = analytics.vectorString(len(udl_with_weights))
    underlying_weights = analytics.vectorDouble(len(udl_with_weights))
    for i in range(len(udl_with_weights)):
        basket[i] = udl_with_weights[i][1]
        underlying_weights[i] = udl_with_weights[i][0]
    underlying_caps = analytics.vectorDouble()#[1000000,1000000])
    underlying_floors = analytics.vectorDouble()#[-10000,-100000])
    weights_after_sort = analytics.vectorDouble([1.0,0])
    basket_cap = analytics.getMaxDouble('');
    basket_floor = -analytics.getMaxDouble('');
    additive_offset = 0.0
    fixing_dates = analytics.vectorPTime()
    fwd_value_type = 'NONE' # set the fwd-start type (here: no fwd start), possible values: None, FwdStartSingle, FwdStartBasket, FloatingStrikeBasket
    fwd_time_agg_type = 'NONE' # set fwd start reference type, possible values: None, Min, Max, Mean
    type_str = 'WorstOf' # just for performance and validation, the type of basket: None, Basket, WorstOf, BestOf, General, BasketOfPerformances,
                        #PerformanceOfBasket, Asian, LookbackBestOf, LookbackWorstOf
    fwd_start_fixings = analytics.vectorPTime()
    time_agg_type = 'None'
    floating_strike = 0
    udls[0] = analytics.RainbowUnderlyingSpec(basket, underlying_weights, underlying_caps, underlying_floors, weights_after_sort, 
                                              basket_cap, basket_floor, additive_offset, fwd_value_type, fwd_time_agg_type, 
                                              fwd_start_fixings,floating_strike,time_agg_type, fixing_dates, type_str)

    spec = analytics.RainbowSpecification(id, issuer, sec_lvl, currency, expiry, barrier_specs, udls)
    return spec    



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
        refdate = utils.getLTime(refdate)
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
 
class MoodysRatingDefinition:
    rating_classes = ['Aaa','Aa', 'A', 'Baa', 'Ba', 'B', 'Caa', 'Ca','C']
    has_default_class = False
    notches =['1', '2', '3']
    
class SandPRatingDefinition:
    rating_classes = ['AAA','AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC','C']
    rating_mappings = {}
    has_default_class = False
    notches =['+', '-'] 


class Rating:
    agency_conigurations = { 'Moodys': {
                                        'rating_map': {'Aaa':'AAA', 'Aa': 'AA', 'A': 'A', 'Baa': 'BBB', 'Ba':'BB', 'B':'B','Caa':'CCC', 'Ca':'CC','C':'C' }
                }
        }

    __analytics_ratings__ = ['AAA','AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC','C', 'D']
    
    
    def __init__(rating):
        '''
        Constructor
        rating must be string of rating given and must equal The rating is initialized with a rating ('AAA','AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC','C', 'D') and a notch, i.e. a floating number in intervall (-0.5, 0.5] 
        '''
        self.rating_index = __analytics_ratings__.index(rating)
        self.notch_string = notch
        self.notch_number = notch

    def get_notch_number():
        return 0


    def __get_notch__(rating_string):
        '''
        return the notch from the given string, i.e. it returns '+' for 'AA+'
        '''
        return 0

  
class Bond:
    def __init__(self, isin, issuer, sec_lvl, issuedate, expiry, coupon_freq, 
                 coupon, notional, 
                 currency, daycounter, floatingrate_underlying = None, spread_float = None,  liquidity_class = None):
        self.isin = isin
        self.issuer = issuer

        self.definition = {}
        self.definition['isin'] = isin
        self.definition['issuer'] = issuer
        self.definition['sec_lvl'] = sec_lvl
        self.definition['issuedate'] = issuedate
        self.definition['expiry'] = expiry
        self.definition['coupon_freq'] = coupon_freq
        self.definition['coupon'] = coupon
        self.definition['spread_float'] = spread_float
        self.definition['daycounter'] = daycounter
        if floatingrate_underlying is not None:
            self.definition['floatingrate_udl'] = floatingrate_underlying
        self.definition['notional'] = notional
        self.definition['currency'] = currency 
        self.definition['liquidity_class'] = liquidity_class
        self.definition['daycounter'] =  daycounter
        self.analytics_spec = None

    def isin(self):
        return self.definition['isin']

    def notional(self):
        return self.definition['notional'
        ]
    def issuer(self):
        return self.definition['issuer']
    def currency(self):
        return self.definition['currency']
    
    def expiry(self):
        return self.definition['expiry']
   
#    Issuers = {'EON': ['AAA', 'GER', 'UTILITY'],
#              'RWE' : ['AA', 'GER','UTILITY'],
#              'ENBW': ['A', 'GER','UTILITY']}
    SecLevels =[enums.SecuritizationLevel.COLLATERALIZED, enums.SecuritizationLevel.EQUITY, enums.SecuritizationLevel.MEZZANINE, enums.SecuritizationLevel.SENIOR_SECURED, enums.SecuritizationLevel.SENIOR_UNSECURED]
    BondExpiries=[10, 365, 5*365, 10*365]
    BondDayCounters = ['ACT365FIXED']
    CouponFrequencies = ['A', 'SA']
    
    def read_EUWAX_csv(filename):
        '''
        reads an EUWAX product data file together with quotes and rturns 
        '''


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


class EUWAX_BondReader:
    '''
    This class reads an EUWAX file and creates bonds and quotes from this files or some statistics from this file
    '''
    zinszusatzangabe_cash_flow={'B': 'Bonusanleihe', 'S': 'Zinsstruktur', 'C': 'Credit Linked Note', 
                                'W': 'Wandelanleihe', 'I': 'Inflationsindexierter Zins', 
                                'Z': 'Zero Bonds', '0': 'Default'}
    aktivkennzeichen = {'D': 'Kein Handel mehr', 'E': 'Kein Handel - aber Pricing', 'T': 'Handel', 'Z':'In Zeichnung', 'V':'In Vorbereitung'}    
    frequency={'Y':'A', 'S':'SA', 'M':'M', 'Q':'Q', 'D':'D'}   
    daycounter = {'ACT/360': 'Act360', '30/360': '30E360', 
    'ACT/ACT': 'ACT365FIXED', 'ACT/365':'Act365','ACTw252': 'ACT365FIXED', 'ACTw252': 'Act252'} 
    def __init__(self, filename):
        self.df = pd.read_table(filename, header=None, sep=';')
        columns = ['ISIN', 'WKN', 'Name der Anleihe', 'Zinssatz', 'Nominalwert', 
            'Nominalwährung', 'Kleinste handelbare Einheit', 'Name des Emittenten' , 
            'Name des Emittenten (Englisch)', 'URL des Emittenten', 
            'Zeichnungsstart', 'Zeichnungsende', 'Aktivkennzeichen', 
            'Emissionspreis', 'Emissionsvolumen',
            'Kennzeichen Emissionsstatus', 'Einführungsdatum', 'Erster Handelstag' ,
            'Fälligkeitstag', 'Datum nächste Zinszahlung', 'Datum nächste Zinsanpassung', 
            'Periodizität der Zinsanpassungen', 'Erster Kündigungstermin', 
            'Periodizität der Kündigungen', 'Produkthierarchie Code', 'Zinszusatzangaben Cash-Flow',
            'Zinsabhängigkeiten Cash-Flow', 'Zinsberechnungmethode', 'Notierungsart', 
            'Flatnotiz', 'Step-Up/Step-Down bei Ratingveränderung', 'Step-Up bei Emission festgesetzt',
            'Step-Down bei Emission festgesetzt',
            'Anleihe vom Emittent vorzeitig kündbar', 'Nachrangig', 'Zusatzinformationen', 
            'Handelssegment', 'Anzahl Ticks (Segment)', 'Market Maker 1', 'Handelszeit 1', 
            'Market Maker 2', 'Handelzeit 2', 'Handelsinitiative', 'Anzahl Ticks (Initiative)',
            'Market Maker 3', 'Handelszeit 3', 'Kennzeichen Kompensation',
            'Periodizität der Zinszahlungen', 
            'Datum Zinslauf ab (Zinslaufbeginn)', 'Datum erster Zinstermin', 'Marktsegment',
            'Ausgabeaufschlag', 'Preisattribut', 'Fiskalname des Emittenten', 
            'Aktie des Konzern (ISIN)']
        self.col_isin = 'ISIN'
        self.col_wkn = 'WKN'
        self.col_issuer = 'Name des Emittenten'
        self.col_notional = 'Nominalwert'
        self.col_currency = 'Nominalwährung'
        self.col_maturity = 'Fälligkeitstag'
        self.col_daycounter = 'Zinsberechnungmethode'
        self.col_coupon_freq = 'Periodizität der Zinszahlungen'
        self.col_issue_date = 'Datum Zinslauf ab (Zinslaufbeginn)'
        self.col_coupon = 'Zinssatz'
        self.col_subordinated = 'Nachrangig'
        self.df.columns = columns

    def extract_statistics(self):
        ''' 
        returns some statistics about the data read
        '''
        result = {}
        result['number of instrument'] = len(self.df.index)
        result['traded'] = {}
        traded_ins =  self.df[self.df['Aktivkennzeichen'] =='T']
        result['traded']['number of instruments'] =traded_ins.count()['Aktivkennzeichen']
        plain_vanilla = {}
        traded_simple = traded_ins[traded_ins['Zinszusatzangaben Cash-Flow'] == '0']
        self.pv_non_callable =  traded_simple[traded_simple['Anleihe vom Emittent vorzeitig kündbar'] =='N']
        daycounter = {}
        for i in range(len(self.pv_non_callable.index)):
            index = self.pv_non_callable.index[i]
            if self.pv_non_callable[self.col_daycounter][index] in daycounter:
                daycounter[self.pv_non_callable[self.col_daycounter][index]] += 1
            else:
                daycounter[self.pv_non_callable[self.col_daycounter][index]] = 1
        plain_vanilla['non-callable-daycounter'] = daycounter
        plain_vanilla['non-callable'] =self.pv_non_callable.count()['Zinszusatzangaben Cash-Flow']
        self.pv_callable = traded_simple[traded_simple['Anleihe vom Emittent vorzeitig kündbar'] =='J']
        plain_vanilla['callable'] = self.pv_callable.count()['Zinszusatzangaben Cash-Flow']
        daycounter = {}
        for i in range(len(self.pv_callable.index)):
            index = self.pv_callable.index[i]
            if self.pv_callable[self.col_daycounter][index] in daycounter:
                daycounter[self.pv_callable[self.col_daycounter][index]] += 1
            else:
                daycounter[self.pv_callable[self.col_daycounter][index]] = 1
        plain_vanilla['callable-daycounter'] = daycounter
        result['traded']['plain vanilla'] = plain_vanilla
        structured = {}
        structured['zero bonds'] = self.df[(self.df['Aktivkennzeichen'] =='T') & (self.df['Zinszusatzangaben Cash-Flow'] == 'Z')].count()['Aktivkennzeichen']
        structured['Bonusanleihen'] = self.df[(self.df['Aktivkennzeichen'] =='T') & (self.df['Zinszusatzangaben Cash-Flow'] == 'B')].count()['Aktivkennzeichen']
        structured['Zinsstrukturen'] = self.df[(self.df['Aktivkennzeichen'] =='T') & (self.df['Zinszusatzangaben Cash-Flow'] == 'S')].count()['Aktivkennzeichen']
        structured['Credit Linked Notes'] = self.df[(self.df['Aktivkennzeichen'] =='T') & (self.df['Zinszusatzangaben Cash-Flow'] == 'C')].count()['Aktivkennzeichen']
        structured['Wandelanleihen'] = self.df[(self.df['Aktivkennzeichen'] =='T') & (self.df['Zinszusatzangaben Cash-Flow'] == 'W')].count()['Aktivkennzeichen']
        structured['inflation linked bonds'] = self.df[(self.df['Aktivkennzeichen'] =='T') & (self.df['Zinszusatzangaben Cash-Flow'] == 'I')].count()['Aktivkennzeichen']
        result['traded']['structured'] = structured
        
        #simple_bonds_stat = {}
        #pivot = pd.pivot_table(traded_simple, index=["Periodizität der Zinszahlungen"], columns=['Zinsberechnungmethode'], values=['Emissionspreis'], aggfunc=np.count_nonzero)
        #print(pivot)
        return result
           
    def get_plain_vanilla_bonds(self, refdate):
        result = {}
        num_bonds = 0
        error_dc = 0
        error_issuer = 0
        error_freq = 0
        error_currency = 0
        error_notional = 0
        error_expiry = 0
        for i in range(len(self.pv_non_callable.index)):
            index = self.pv_non_callable.index[i]
            daycounter = self.pv_non_callable[self.col_daycounter][index]
            isin = self.pv_non_callable[self.col_isin][index]
            if daycounter in BondReader.daycounter:
                daycounter = BondReader.daycounter[daycounter]
            else:
                logging.debug(' %s is skipped due to unhandled daycounter %s', isin, str(daycounter))
                error_dc += 1
                continue                            
            issuer = self.pv_non_callable[self.col_issuer][index]
            if not isinstance(issuer, str):
                print(isin + ' is skipped due to undefined issuer:  ' + str(issuer))
                error_issuer += 1
                continue
            expiry = datetime.datetime.strptime(self.pv_non_callable[self.col_maturity][index], '%d.%m.%Y')
            if expiry > datetime.datetime(2500, 1,1):
                print(isin + ' is skipped due to expiry: ' + str(expiry))
                error_expiry += 1
                continue
            if(expiry < refdate):
                print(isin + ' is skipped since expiry in the past, expiry: ' + str(expiry))
                error_expiry += 1
                continue
            self.pv_non_callable[self.col_maturity][index]
            coupon_freq =self.pv_non_callable[self.col_coupon_freq][index]
            if coupon_freq in BondReader.frequency:
                coupon_freq = BondReader.frequency[coupon_freq]
            else:
                print(isin + ' is skipped due to unhandled coupon frequency ' + str(coupon_freq))
                error_freq += 1
                continue
            coupon = float(self.pv_non_callable[self.col_coupon][index])
            currency = self.pv_non_callable[self.col_currency][index]
            if currency == 'DEM':
                print(isin + ' is skipped: Deutsche Mark as currency ')
                error_currency += 1
                continue
            notional = self.pv_non_callable[self.col_notional][index]
            if notional <= 0:
                print(isin + ' is skipped, notional less or equal to 0, notional: ' + str(notional))
                error_notional += 1
                continue
            issue_date =  datetime.datetime.strptime(self.pv_non_callable[self.col_issue_date][index], '%d.%m.%Y')
            sec_lvl = 'COLLATERALIZED' # abhängig von subordinated-flag im file
                
            result[isin] = Bond(isin, issuer, sec_lvl, 
                                issue_date, expiry, coupon_freq, 
                                coupon, notional, currency, daycounter)
            num_bonds += 1
        logging.info('%d bonds were loaded and %d bonds skipped due to errors.', num_bonds, 
                     error_dc + error_issuer + error_freq +error_currency + error_notional+ error_expiry)
        logging.info('issuer errors: %d,  freq errors: %d,  curr errors: %d,  notional errors: %d,  expiry errors: %d',
                    error_issuer, error_freq, error_currency, error_notional, error_expiry)
        return result


def all_data(env):
    DOP.all_data(env)
    European.all_data(env)
    Bonds.all_data(env)