# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
import pandas as pd
import pyvacon.analytics as analytics
import pyvacon.tools.enums as enums
import pyvacon.tools.converter as converter
import pyvacon.marketdata.testdata as mkt_testdata

def multi_memory_express_from_dict(ins_dict, fixing_table):
    obj_id = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    basket = ins_dict['BASKET']
    if isinstance(basket,pd.DataFrame):
        basket = basket.to_dict()
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    payoff = analytics.PayoffStructure(ins_dict['PAYOFF']['SPOT'], ins_dict['PAYOFF']['VALUE'])
    share_ratio = 1.0
    if 'SHARE_RATIO' in ins_dict:
        share_ratio = ins_dict['SHARE_RATIO']
    coupon_desc = ins_dict['COUPONS']
    if isinstance(coupon_desc,pd.DataFrame):
        coupon_desc = coupon_desc.to_dict()                   
    redemption_price = coupon_desc['REDEMPTION_PRICE']
    redemption_levels =  analytics.vectorDouble(coupon_desc['REDEMPTION_LEVEL'])
    redemption_up = coupon_desc['REDEMPTION_UP']
    coupon = coupon_desc['COUPON']
    coupon_levels = analytics.vectorDouble(coupon_desc['LEVELS'])
    coupon_up = coupon_desc['UP']
    coupon_dates = converter.createPTimeList(None,coupon_desc['OBSERVATION_DATES'])
    coupon_payment_dates = converter.createPTimeList(None,coupon_desc['PAYMENT_DATES'])
    underlyings = analytics.vectorString(basket['UNDERLYINGS'])
    spec_analytics = analytics.MultiMemoryExpressSpecification(obj_id, issuer, 
                                                 enums.SecuritizationLevel.NONE, 
                                                 currency, 
                                                 underlyings, 
                                                 analytics.vectorDouble(basket['WEIGHTS']), 
                                                 ins_dict['TYPE'], 
                                                 expiry, payoff, redemption_price, 
                                                 redemption_levels, 
                                                 redemption_up, coupon, 
                                                 coupon_levels, 
                                                 coupon_up,
                                                 coupon_dates, 
                                                 coupon_payment_dates,
                                                 share_ratio)
    return spec_analytics.convertIntoRainbowSpecification(fixing_table)

def memory_express_from_dict(ins_dict, fixing_table, rainbow_flag):
    obj_id = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    payoff = analytics.PayoffStructure(ins_dict['PAYOFF']['SPOT'], ins_dict['PAYOFF']['VALUE'])
    share_ratio = ins_dict['SHARE_RATIO']
    coupon_desc = ins_dict['COUPONS']
    if isinstance(coupon_desc,pd.DataFrame):
        coupon_desc = coupon_desc.to_dict()                   
    redemption_price = coupon_desc['REDEMPTION_PRICE']
    redemption_levels =  analytics.vectorDouble(coupon_desc['REDEMPTION_LEVEL'])
    redemption_up = coupon_desc['REDEMPTION_UP']
    coupon = coupon_desc['COUPON']
    coupon_levels = analytics.vectorDouble(coupon_desc['LEVELS'])
    coupon_up = coupon_desc['UP']
    coupon_dates = converter.createPTimeList(None,coupon_desc['OBSERVATION_DATES'])
    coupon_payment_dates = converter.createPTimeList(None,coupon_desc['PAYMENT_DATES'])
    spec_analytics = analytics.MemoryExpressSpecification(obj_id, 
                                                 issuer, 
                                                 enums.SecuritizationLevel.NONE, 
                                                 currency, 
                                                 underlying, 
                                                 expiry, payoff, redemption_price, 
                                                 redemption_levels, 
                                                 redemption_up, coupon, 
                                                 coupon_levels, 
                                                 coupon_up,
                                                 coupon_dates, 
                                                 coupon_payment_dates,
                                                 share_ratio)
    if rainbow_flag==1:
        return spec_analytics.convertIntoRainbowSpecification(fixing_table)
    else:
        return spec_analytics.convertIntoComboSpecification(fixing_table)

def create_vanilla_payoff(strike, isCall, factor = 1.0):
    xPoints = analytics.vectorDouble(3)
    pPoints = analytics.vectorDouble(3)
    xPoints[0] = -1.e10
    xPoints[1] = strike
    xPoints[2] = strike + 1.e10
    if isCall:
        pPoints[0] = 0
        pPoints[1] = 0
        pPoints[2] = factor * 1.e10
    else:       
        pPoints[0] = factor * 1.e10
        pPoints[1] = 0
        pPoints[2] = 0
    return analytics.PayoffStructure(xPoints, pPoints)

def create_digital_payoff(strike, isCall):
    xPoints = analytics.vectorDouble(4)
    pPoints = analytics.vectorDouble(4)
    xPoints[0] = 0
    xPoints[1] = strike - 1.e-8
    xPoints[2] = strike + 1.e-8
    xPoints[3] = 1.e8
    if isCall:
        pPoints[0] = 0
        pPoints[1] = 0
        pPoints[2] = 1
        pPoints[3] = 1
    else:       
        pPoints[0] = 1
        pPoints[1] = 1
        pPoints[2] = 0
        pPoints[3] = 0
    return analytics.PayoffStructure(xPoints, pPoints)

def create_zero_payoff():
    xPoints = analytics.vectorDouble(2)
    pPoints = analytics.vectorDouble(2)
    xPoints[0] = -1000000000
    xPoints[1] = 1000000000
    pPoints[0] = 0
    pPoints[1] = 0
    return analytics.PayoffStructure(xPoints, pPoints)


def barrier_option_from_dict(ins_dict):
    obj_id = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    strike = ins_dict['STRIKE']
    level = ins_dict['LEVEL']
    start = converter.getLTime(ins_dict['START'])
    end = converter.getLTime(ins_dict['END'])
    
    if (ins_dict['PAYOFF'].upper() == 'CALL'):
        isCall = True
    elif (ins_dict['PAYOFF'].upper() == 'PUT'):
        isCall = False
    else:
        raise ValueError('Invalid value for PAYOFF: ' + ins_dict['PAYOFF'] + ', allowed values: CALL or PUT')
    if (ins_dict['TYPE'].upper() == 'IN'):
        isIn = True
    elif (ins_dict['TYPE'].upper() == 'OUT'):
        isIn = False
    else:
        raise ValueError('Invalid value for TYPE: ' + ins_dict['TYPE'] + ', allowed values: IN or OUT')
    if (ins_dict['DIRECTION'].upper() == 'UP'):
        isUp = True
    elif (ins_dict['DIRECTION'].upper() == 'DOWN'):
        isUp = False
    else:
        raise ValueError('Invalid value for DIRECTION: ' + ins_dict['DIRECTION'] + ', allowed values: UP or DOWN')

    if isIn:
        finalPayoff = create_zero_payoff()
        barrierPayoff = create_vanilla_payoff(strike, isCall)
    else:
        finalPayoff = create_vanilla_payoff(strike, isCall)
        barrierPayoff = create_zero_payoff()

    bPayoff = analytics.BarrierPayoff('', expiry, barrierPayoff)

    barrierDefinition = analytics.BarrierDefinition(start, end, bPayoff, level, True)

    schedule = analytics.BarrierSchedule()
    if isUp:
        schedule.addUpBarrier(barrierDefinition)
    else:
        schedule.addDownBarrier(barrierDefinition)

    
    return analytics.BarrierSpecification(obj_id,
                                          issuer,
                                          enums.SecuritizationLevel.NONE, 
                                          currency,
                                          underlying,
                                          expiry,
                                          schedule,
                                          finalPayoff)


def barrier_option_mc_from_dict(ins_dict):
    objId = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    strike = ins_dict['STRIKE']
    level = ins_dict['LEVEL']
    start = converter.getLTime(ins_dict['START'])
    end = converter.getLTime(ins_dict['END'])
    
    if (ins_dict['PAYOFF'].upper() == 'CALL'):
        isCall = True
    elif (ins_dict['PAYOFF'].upper() == 'PUT'):
        isCall = False
    else:
        raise ValueError('Invalid value for PAYOFF: ' + ins_dict['PAYOFF'] + ', allowed values: CALL or PUT')
    if (ins_dict['TYPE'].upper() == 'IN'):
        isIn = True
    elif (ins_dict['TYPE'].upper() == 'OUT'):
        isIn = False
    else:
        raise ValueError('Invalid value for TYPE: ' + ins_dict['TYPE'] + ', allowed values: IN or OUT')
    if (ins_dict['DIRECTION'].upper() == 'UP'):
        isUp = True
        levelUp = analytics.getMaxDouble('')
        levelDown = level
    elif (ins_dict['DIRECTION'].upper() == 'DOWN'):
        isUp = False
        levelUp = level
        levelDown = -analytics.getMaxDouble('')
    else:
        raise ValueError('Invalid value for DIRECTION: ' + ins_dict['DIRECTION'] + ', allowed values: UP or DOWN')

    if isIn:
        noHitPayoff = create_zero_payoff()
        hitPayoff = create_vanilla_payoff(strike, isCall)
    else:
        hitPayoff = create_zero_payoff()
        noHitPayoff = create_vanilla_payoff(strike, isCall)

    hitPayoffPoints = [x for x in hitPayoff.getPayoffSpots()]
    hitPayoffValues = [x for x in hitPayoff.getPayoffValues()]
    noHitPayoffPoints = [x for x in noHitPayoff.getPayoffSpots()]
    noHitPayoffValues = [x for x in noHitPayoff.getPayoffValues()]

    udls = analytics.vectorRainbowUdlSpec(1)
    
    udls[0] = analytics.RainbowUnderlyingSpec(
        analytics.vectorString([underlying]), # udl basket
        analytics.vectorDouble([1.0]),        # udl weights
        analytics.vectorDouble(),             # udl caps
        analytics.vectorDouble(),             # udl floors
        analytics.vectorDouble([1.0]),        # udl weights before sort
        analytics.vectorDouble([1.0]),        # udl weights after sort
        analytics.getMaxDouble(''),           # basket cap
        -analytics.getMaxDouble(''),          # basket floor
        0.0,                                  # add. offset,
        'NONE',                               # ref type
        'NONE',                               # fwd time aggr
        analytics.vectorPTime(),              # ref dates
        0.0,                                  # ref strike
        'NONE',                               # time aggr
        analytics.vectorPTime(),
        'NONE')
        

    barrierSpecs = analytics.vectorRainbowBarrierSpec(1)

    barrierSpecs[0] = analytics.RainbowBarrierSpec(
        start,                                # barrier start
        expiry,                               # barrier end
        analytics.vectorPTime(),              # obs. dates
        levelDown,                            # lower level
        levelUp,                              # upper level
        0,                                    # udl id
        analytics.vectorInt(),
        analytics.vectorBool(),
        True,
        hitPayoffPoints,
        hitPayoffValues,
        noHitPayoffPoints,
        noHitPayoffValues,
        expiry)

    return analytics.RainbowSpecification(
        objId,
        issuer,
        'NONE',
        currency,
        expiry,
        barrierSpecs,
        udls
    )
    


def digital_option_from_dict(ins_dict):
    obj_id = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    strike = ins_dict['STRIKE']
    
    if (ins_dict['PAYOFF'].upper() == 'CALL'):
        isCall = True
    elif (ins_dict['PAYOFF'].upper() == 'PUT'):
        isCall = False
    else:
        raise ValueError('Invalid value for PAYOFF: ' + ins_dict['PAYOFF'] + ', allowed values: CALL or PUT')

    finalPayoff = create_digital_payoff(strike, isCall)
    barrierPayoff = create_zero_payoff()

    bPayoff = analytics.BarrierPayoff('', expiry, barrierPayoff)

    barrierDefinition = analytics.BarrierDefinition(analytics.ptime(2000,1,1,0,0,0), expiry, bPayoff, -1.0, True) # never hit

    schedule = analytics.BarrierSchedule()
    schedule.addDownBarrier(barrierDefinition)
    
    return analytics.BarrierSpecification(obj_id,
                                          issuer,
                                          enums.SecuritizationLevel.NONE, 
                                          currency,
                                          underlying,
                                          expiry,
                                          schedule,
                                          finalPayoff)

def american_vanilla_from_dict(ins_dict):
    objId = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    strike = ins_dict['STRIKE']
    payoff = ins_dict['PAYOFF']

    return analytics.AmericanVanillaSpecification(objId,
                                                  issuer,
                                                  "NONE",
                                                  currency,
                                                  underlying,
                                                  payoff,
                                                  expiry,
                                                  strike)


def forward_start_digital_from_dict(ins_dict):
    objId = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    relStrike = ins_dict['RELSTRIKE']
    start = converter.getLTime(ins_dict['START'])
    forwardStart = converter.getLTime(ins_dict['FORWARDSTART'])


    udls = analytics.vectorRainbowUdlSpec(1)
    
    udls[0] = analytics.RainbowUnderlyingSpec(
        analytics.vectorString([underlying]), # udl basket
        analytics.vectorDouble([1.0]),        # udl weights
        analytics.vectorDouble(),             # udl caps
        analytics.vectorDouble(),             # udl floors
        analytics.vectorDouble([1.0]),        # udl weights before sort
        analytics.vectorDouble([1.0]),        # udl weights after sort
        analytics.getMaxDouble(''),           # basket cap
        -analytics.getMaxDouble(''),          # basket floor
        0.0,                                  # add. offset,
        'FLOATINGSTRIKEBASKET',
        'NONE',                               # fwd time aggr
        analytics.vectorPTime([forwardStart]),
        relStrike,
        'NONE',                               # time aggr
        analytics.vectorPTime(),
        'NONE')
        

    barrierSpecs = analytics.vectorRainbowBarrierSpec(1)

    payoffPoints = analytics.vectorDouble([-1.e8, -1.e-10, 1.e-10, 1.e8])
    payoffValues = analytics.vectorDouble([0.0, 0.0, 1.0, 1.0])
    
    barrierSpecs[0] = analytics.RainbowBarrierSpec(
        expiry,                               # barrier start
        expiry,                               # barrier end
        analytics.vectorPTime(),              # obs. dates
        -analytics.getMaxDouble(''),          # lower level
        analytics.getMaxDouble(''),           # upper level
        0,                                    # udl id
        analytics.vectorInt(),
        analytics.vectorBool(),
        True,
        payoffPoints,
        payoffValues,
        analytics.vectorDouble(),
        analytics.vectorDouble(),
        expiry)
        
    return analytics.RainbowSpecification(
        objId,
        issuer,
        'NONE',
        currency,
        expiry,
        barrierSpecs,
        udls
        )



def lookback_from_dict(ins_dict):
    objId = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    currency = ins_dict['CURRENCY']
    underlying = ins_dict['UNDERLYING']
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    relStrike = ins_dict['RELSTRIKE']
    start = converter.getLTime(ins_dict['START'])
    forwardStart = converter.getLTime(ins_dict['FORWARDSTART'])
    avDates = converter.createPTimeList(None, ins_dict['PRICEDATES'])
    timeAvg = ins_dict['TIMEAVG']
    if (ins_dict['PAYOFF'].upper() == 'CALL'):
        isCall = True
    elif (ins_dict['PAYOFF'].upper() == 'PUT'):
        isCall = False
    else:
        raise ValueError('Invalid value for PAYOFF: ' + ins_dict['PAYOFF'] + ', allowed values: CALL or PUT')

    udls = analytics.vectorRainbowUdlSpec(1)
        
    udls[0] = analytics.RainbowUnderlyingSpec(
        analytics.vectorString([underlying]), # udl basket
        analytics.vectorDouble([1.0]),        # udl weights
        analytics.vectorDouble(),             # udl caps
        analytics.vectorDouble(),             # udl floors
        analytics.vectorDouble([1.0]),        # udl weights before sort
        analytics.vectorDouble([1.0]),        # udl weights after sort
        analytics.getMaxDouble(''),           # basket cap
        -analytics.getMaxDouble(''),          # basket floor
        0.0,                                  # add. offset,
        'FLOATINGSTRIKEBASKET',
        'NONE',                               # ref time aggr
        analytics.vectorPTime([forwardStart]),# ref date
        relStrike,                            # rel strike
        timeAvg,                              # time aggr
        avDates,
        'NONE')

    
    barrierSpecs = analytics.vectorRainbowBarrierSpec(1)

    payoff = create_vanilla_payoff(0.0, isCall)

    payoffPoints = [x for x in payoff.getPayoffSpots()]
    payoffValues = [x for x in payoff.getPayoffValues()]


    
    barrierSpecs[0] = analytics.RainbowBarrierSpec(
        expiry,                               # barrier start
        expiry,                               # barrier end
        analytics.vectorPTime(),              # obs. dates
        -analytics.getMaxDouble(''),          # lower level
        analytics.getMaxDouble(''),           # upper level
        0,                                    # udl id
        analytics.vectorInt(),
        analytics.vectorBool(),
        True,
        payoffPoints,
        payoffValues,
        analytics.vectorDouble(),
        analytics.vectorDouble(),
        expiry)
        
    return analytics.RainbowSpecification(
        objId,
        issuer,
        'NONE',
        currency,
        expiry,
        barrierSpecs,
        udls
        )


def expressplus_from_dict(ins_dict):
    objId = ins_dict['ID']
    issuer ='UNDEF'
    if 'ISSUER' in ins_dict:
        issuer = ins_dict['ISSUER']
    secLvl ='NONE'
    if 'SECLVL' in ins_dict:
        secLvl = ins_dict['SECLVL']
    currency = ins_dict['CURRENCY']
    basket = analytics.vectorString(ins_dict['UNDERLYINGS'])
    weights = analytics.vectorDouble(ins_dict['WEIGHTS'])
    expiry = converter.getLTime(ins_dict['EXPIRY'])
    fwdStart = ins_dict['FWDSTART']
    fwdStartDate = converter.getLTime(ins_dict['FWDSTARTDATE'])
    cpnLevelLower = analytics.vectorDouble(ins_dict['COUPONLOWERLEVEL'])
    cpnLevelUpper = analytics.vectorDouble(ins_dict['COUPONUPPERLEVEL'])
    cpnStartDates = converter.createPTimeList(None, ins_dict['COUPONSTARTDATES'])
    cpnEndDates = converter.createPTimeList(None, ins_dict['COUPONENDDATES'])
    cpnPayDates = converter.createPTimeList(None, ins_dict['COUPONPAYDATES'])
    cpnObsDates = analytics.vectorVectorPTime([converter.createPTimeList(None, x) for x in ins_dict['COUPONOBSDATES']])

    cpnPayoffsX = analytics.vectorVectorDouble([analytics.vectorDouble(p[0]) for p in ins_dict['COUPONPAYOFFS']])
    cpnPayoffsY = analytics.vectorVectorDouble([analytics.vectorDouble(p[1]) for p in ins_dict['COUPONPAYOFFS']])
    
    cpnIn = analytics.vectorBool(ins_dict['COUPONIN'])
    
    redLevelLower = analytics.vectorDouble(ins_dict['REDEMPTIONLOWERLEVEL'])
    redLevelUpper = analytics.vectorDouble(ins_dict['REDEMPTIONUPPERLEVEL'])
    redStartDates = converter.createPTimeList(None, ins_dict['REDEMPTIONSTARTDATES'])
    redEndDates = converter.createPTimeList(None, ins_dict['REDEMPTIONENDDATES'])
    redPayDates = converter.createPTimeList(None, ins_dict['REDEMPTIONPAYDATES'])
    redObsDates = [converter.createPTimeList(None, x) for x in ins_dict['REDEMPTIONOBSDATES']]
    redPayoffsX = analytics.vectorVectorDouble([analytics.vectorDouble(p[0]) for p in ins_dict['REDEMPTIONPAYOFFS']])
    redPayoffsY = analytics.vectorVectorDouble([analytics.vectorDouble(p[1]) for p in ins_dict['REDEMPTIONPAYOFFS']])
    redIn = analytics.vectorBool(ins_dict['REDEMPTIONIN'])
    
    plus = ins_dict['PLUS']
    if plus:
        plusLevelLower = ins_dict['PLUSLOWERLEVEL']
        plusLevelUpper = ins_dict['PLUSUPPERLEVEL']
        plusStartDate = converter.getLTime(ins_dict['PLUSSTARTDATE'])
        plusEndDate = converter.getLTime(ins_dict['PLUSENDDATE'])
        plusPayDate = converter.getLTime(ins_dict['PLUSPAYDATE'])
        plusObsDates = converter.createPTimeList(None, ins_dict['PLUSOBSDATES'])
        plusPayoffX = analytics.vectorDouble(ins_dict['PLUSPAYOFF'][0])
        plusPayoffY = analytics.vectorDouble(ins_dict['PLUSPAYOFF'][1])
        plusIn = ins_dict['PLUSIN']
    else: # not plus feature -> set dummy values
        plusLevelLower = 0.0
        plusLevelUpper = 0.0
        plusStartDate = analytics.ptime(2001, 1, 1, 0, 0, 0)
        plusEndDate = analytics.ptime(2001, 1, 1, 0, 0, 0)
        plusPayDate = analytics.ptime(2001, 1, 1, 0, 0, 0)
        plusObsDates = analytics.vectorPTime(0)
        plusPayoffX = analytics.vectorDouble([])
        plusPayoffY = analytics.vectorDouble([])
        plusIn = False

        
    memory = ins_dict['MEMORY']
    floatCpnRelative = ins_dict['FLOATCPNRELATIVE']
    basketType = ins_dict['BASKETTYPE']

    return analytics.ExpressPlusSpecification(
        objId,
        issuer,
        secLvl,
        currency,
        basket,
        weights,
        expiry,
        fwdStart,
        fwdStartDate,

        cpnPayoffsX,
        cpnPayoffsY,
        cpnLevelLower,
        cpnLevelUpper,
        cpnStartDates,
        cpnEndDates,
        cpnPayDates,
        cpnObsDates,
        cpnIn,

        redPayoffsX,
        redPayoffsY,
        redLevelLower,
        redLevelUpper,
        redStartDates,
        redEndDates,
        redPayDates,
        redObsDates,
        redIn,

        plus,
        plusPayoffX,
        plusPayoffY,
        plusLevelLower,
        plusLevelUpper,
        plusStartDate,
        plusEndDate,
        plusPayDate,
        plusObsDates,
        plusIn,
        
        memory,
        floatCpnRelative,
        basketType)

