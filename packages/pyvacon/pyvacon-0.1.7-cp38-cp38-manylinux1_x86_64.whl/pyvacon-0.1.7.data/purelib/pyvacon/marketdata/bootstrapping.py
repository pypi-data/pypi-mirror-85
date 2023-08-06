# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 23:37:58 2017

@author: Anwender
"""
import pyvacon.analytics as analytics
from dateutil.relativedelta import relativedelta
import pyvacon.tools.converter as converter
import pyvacon.tools.enums as enums


def bootstrap_curve(inputData, outputSpec):
    refDate = outputSpec['refDate']
    refDate_p = converter.getLTime(refDate)
    n = len(inputData.index)
    instruments = analytics.vectorBaseSpecification(n)
    quotes = analytics.vectorDouble(n)
    holidays = outputSpec['calendar']
    for i in range(0,n):
        ins = InstrumentSpec(refDate,inputData.iloc[i,:], holidays)
        instruments[i] = ins.get_instrument()
        quotes[i] = ins.parRate #inputData.iloc[i,:]['Quote']
        
    if('discountCurve') in outputSpec:
        df = outputSpec['discountCurve']
    else:
        df = None
    
    if('basisCurve') in outputSpec:
        basisCurve = outputSpec['basisCurve']
    else:
        basisCurve = None
        
    curve = analytics.YieldCurveBootstrapper.compute(refDate_p, outputSpec['curveName'], outputSpec['dayCount'], 
                                                 instruments, quotes, df, basisCurve)
    return(curve)
    #return(instruments)

class Instrument:
    IRS = 'IRS'
    TBS = 'TBS'
    Deposit = 'DEPOSIT'
    OIS = 'OIS'
    FRA = 'FRA'
    

class InstrumentSpec:
    """
    Definition of input instruments for IR boostrapping
    """   
    
    def __init__(self, refDate, inputData, holidays):
        
        self.refDate = refDate
        self.refDate_p = converter.getLTime(refDate)
        self.instr = inputData['Instrument']
        self.fixDayCount = inputData['DayCountFixed']
        self.floatDayCount = inputData['DayCountFloat']
        self.basisDayCount = inputData['DayCountBasis']
        self.maturity = inputData['Maturity']
        self.tenor = inputData['UnderlyingTenor']
        self.underlyingPayFreq = inputData['UnderlyingPaymentFrequency']
        self.basisTenor = inputData['BasisTenor']
        self.basisPayFreq = inputData['BasisPaymentFrequency']
        self.fixPayFreq = inputData['PaymentFrequencyFixed']
        self.rollConvFloat = inputData['RollConventionFloat']
        self.rollConvFix = inputData['RollConventionFixed']
        self.rollConvBasis = inputData['RollConventionBasis']
        self.spotLag = inputData['SpotLag']
        self.label =  self.instr +'_' + self.maturity
        self.currency = inputData['Currency']
        self.holidays = holidays
        self.parRate = inputData['Quote']
        
    def get_instrument(self):
        """
        Instrument specification based on the "Instrument" field the input data
        """
        if (self.instr.upper() == Instrument.IRS):
            instrument = self.get_irs_spec()  
        elif (self.instr.upper() == Instrument.OIS):
              instrument = self.get_irs_spec() 
        elif (self.instr.upper() == Instrument.TBS):
            instrument = self.get_tbs_spec() 
        elif (self.instr.upper() == Instrument.Deposit):
            instrument = self.get_deposit_spec() 
        elif (self.instr.upper() == Instrument.FRA):
            instrument = self.get_fra_spec() 
        else:
            Exception('Unknown instrument type')  
        return(instrument)
    

    def get_irs_spec(self):
        """
        Specification for interest rate swaps
        """
        # get floating leg schedule
        floatleg = self.get_float_leg(self.underlyingPayFreq, self.tenor, self.rollConvFloat, self.spotLag)

        # get fix leg schedule
        fixedleg = self.get_fix_leg(self.fixPayFreq, self.rollConvFix, self.spotLag)
        
        # get expiry of swap (cannot be before last paydate of legs)
        spotDate = get_end_date(self.refDate, self.spotLag)
        expiry = get_end_date(spotDate, self.maturity)
        expiry_p = converter.getLTime(expiry)
    
        # SecuritizationLevel is not used in the bootstrapping algorithm
        ir_swap = analytics.InterestRateSwapSpecification(self.label, 'dummy_issuer', enums.SecuritizationLevel.COLLATERALIZED, 
                                                                 self.currency, expiry_p, fixedleg, floatleg)
        return(ir_swap)
    
    def get_tbs_spec(self):
        """
        Specification for tenor basis swaps
        """
        # get floating leg schedule
        floatleg = self.get_float_leg(self.underlyingPayFreq, self.tenor, self.rollConvFloat, self.spotLag)
        floatlegBasis = self.get_float_leg(self.basisPayFreq, self.basisTenor, self.rollConvBasis, self.spotLag)
        
        # get fix leg schedule
        fixedleg = self.get_fix_leg(self.fixPayFreq, self.rollConvFix, self.spotLag)
              
        
        # get expiry of swap (cannot be before last paydate of legs)
        spotDate = get_end_date(self.refDate, self.spotLag)
        expiry = get_end_date(spotDate, self.maturity)
        expiry_p = converter.getLTime(expiry)
        
        # the basis leg should be the pay leg
        basis_swap = analytics.InterestRateBasisSwapSpecification(self.label, 'dummy_issuer', enums.SecuritizationLevel.COLLATERALIZED, 
                                                   self.currency, expiry_p, floatlegBasis, floatleg, fixedleg)
        return(basis_swap)
    
    
    def get_deposit_spec(self):
        """
        Specification for deposits
        """
        
        # get spot date
        spotDate = get_end_date(self.refDate,  self.spotLag)
        
        # end date of the accrual period
        endDate = get_end_date(spotDate, self.maturity)
        endDate_p = converter.getLTime(endDate)
        
        # start date of FRA is endDate - tenor
        startDate = get_start_date(endDate, self.tenor)
        startDate_p = converter.getLTime(startDate)
        
        # specification of the deposit
        deposit = analytics.DepositSpecification(self.label, 'dummy_issuer', enums.SecuritizationLevel.NONE,
                                        self.currency, self.refDate_p, startDate_p, endDate_p, 100, self.parRate, self.floatDayCount)
                                                  
        return(deposit)

    
    def get_fra_spec(self):
        """
        Specification for FRAs/Futures
        """
        # get spot date
        spotDate = get_end_date(self.refDate,  self.spotLag)
        
        # end date of the accrual period
        endDate = get_end_date(spotDate, self.maturity)
        endDate_p = converter.getLTime(endDate)
        
        # start date of FRA is endDate - tenor
        startDate = get_start_date(endDate, self.tenor)
        startDate_p = converter.getLTime(startDate)
        
        # expiry of FRA is the fixing date 
        expiryDate = get_start_date(startDate, self.spotLag)
        expiryDate_p = converter.getLTime(expiryDate)
        
        # specification of the deposit
        fra = analytics.InterestRateFutureSpecification(self.label, 'dummy_issuer', enums.SecuritizationLevel.NONE,
                                        self.currency, 'dummy_udlId', expiryDate_p, 100, startDate_p, endDate_p, self.floatDayCount)
     
        return(fra)
    

    def get_float_leg(self, payFreq, resetFreq, rollConv, spotLag = '0D'):
        
        # get swap leg schedule
        fltSchedule = get_schedule(self.refDate, self.maturity,  payFreq,  rollConv, self.holidays, spotLag)
        
        # get start dates
        fltStartDates  = converter.createPTimeList(self.refDate, fltSchedule[:-1])
        
        # get end dates
        fltEndDates = converter.createPTimeList(self.refDate, fltSchedule[1:])
        fltPayDates = fltEndDates
       
        # get reset dates
        fltResetSchedule = get_schedule(self.refDate, self.maturity,  resetFreq,  rollConv, self.holidays, spotLag)
        fltResetDates = converter.createPTimeList(self.refDate, fltResetSchedule[:-1])
         
        fltNotionals = [1.0 for i in range(len(fltStartDates))] 
        floatleg = analytics.IrFloatLegSpecification(fltNotionals, fltResetDates, fltStartDates, fltEndDates, fltPayDates, 
                                                     self.currency, 'dummy_undrl', self.floatDayCount, 0.0)
        return(floatleg)


    def get_fix_leg(self, payFreq, rollConv, spotLag = '0D'):
        # get fix leg schedule
        fixSchedule = get_schedule(self.refDate, self.maturity,  payFreq,  rollConv, self.holidays, spotLag)
        
        # get start dates
        fixStartDates =  converter.createPTimeList(self.refDate, fixSchedule[:-1])
        
        # get end dates
        fixEndDates = converter.createPTimeList(self.refDate, fixSchedule[1:])
        fixPayDates = fixEndDates
        
        fixNotionals = [1.0 for i in range(len(fixStartDates))] 
        fixedleg = analytics.IrFixedLegSpecification(self.parRate, fixNotionals, fixStartDates, fixEndDates, fixPayDates, 
                                                     self.currency, self.fixDayCount)
        return(fixedleg)

def get_schedule(refDate, term, tenor, rollConv, holidays, spotLag = '0D', stubPeriod = False):
    """
    Generates a schedule starting with refDate + spotLag
    """
    # calc schedule start & end dates
    start = get_end_date(refDate, spotLag)
    end = get_end_date(start, term)
    start_p = converter.getLTime(start)
    end_p = converter.getLTime(end)
    
    # calc schedule period
    period = get_period(tenor)
    schedule_spec = analytics.ScheduleSpecification(start_p, end_p, period, stubPeriod, rollConv, holidays)
    schedule_p = schedule_spec.generate()
   # schedule = converter.create_datetime_list(schedule_p)
    return(schedule_p)

def get_period(tenor):
    t = tenor[-1]
    p = int(tenor[:-1])
    
    if (t.upper() == 'D'):
        result = analytics.Period(0,0,p)
    elif (t.upper() == 'M'):
        result = analytics.Period(0,p,0)
    elif (t.upper() == 'Y'):
        result = analytics.Period(p,0,0) 
    else:
        Exception('Unknown tenor')
    return result

def get_end_date(startDate, term):
    t = term[-1]
    p =  int(term[:-1])
    
    if (t.upper() == 'D'):
        result = startDate + relativedelta(days=+p)
    elif (t.upper() == 'M'):
        result = startDate + relativedelta(months=+p)
    elif (t.upper() == 'Y'):
        result = startDate + relativedelta(years=+p) 
    else:
        Exception('Unknown term')
    return result

def get_start_date(endDate, term):
    t = term[-1]
    p =  int(term[:-1])
    
    if (t.upper() == 'D'):
        result = endDate + relativedelta(days=-p)
    elif (t.upper() == 'M'):
        result = endDate + relativedelta(months=-p)
    elif (t.upper() == 'Y'):
        result = endDate + relativedelta(years=-p) 
    else:
        Exception('Unknown term')
    return result
