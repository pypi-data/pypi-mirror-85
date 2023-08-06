import numpy as np
import copy
import pandas as pd

import pyvacon.analytics as analytics
import pyvacon.marketdata.converter as mkt_converter
import pyvacon.tools.converter as converter
import pyvacon.tools.enums as enums

# transform vola surface from "spot dividend" model
# into Buehler model specified by fwd curve
def transformVola(refDate, volaBS, fwd, dsc):
    dc = analytics.DayCounter(enums.DayCounter.ACT365_FIXED)
    bStrikes = []
    bVolas = []
    bExpiries = []
    for i in range(0, len(volaBS['EXPIRIES'])):
        bStrikes.append([])
        bVolas.append([])
        expiry = mkt_converter.converter.getLTime(volaBS['EXPIRIES'][i])
        bExpiries.append(dc.yf(refDate, expiry))
        f = fwd.value(refDate, expiry)
        df = dsc.value(refDate, expiry)
        discDivs = fwd.discountedFutureCashDivs(refDate, expiry)
        for j in range(0, len(volaBS['STRIKES'])):
            strike = volaBS['STRIKES'][j]
            vola = volaBS['VOLAS'][i][j]
            
            xStrikeSpotDiv = analytics.computeXStrike(strike, f, 0)
            callPriceXSpotDiv = analytics.calcEuropeanCallPrice(xStrikeSpotDiv, dc.yf(refDate, expiry), 1, 1, vola)

            callPriceXBuehlerDiv = callPriceXSpotDiv * f / (f - discDivs)
            xStrikeBuehlerDiv = analytics.computeXStrike(
                                    strike,
                                    fwd.value(refDate, expiry),
                                    discDivs)
            if xStrikeBuehlerDiv > 0 and callPriceXBuehlerDiv > (1. - xStrikeBuehlerDiv):
                volaB = analytics.calcImpliedVol(
                    callPriceXBuehlerDiv, xStrikeBuehlerDiv, dc.yf(refDate, expiry), 1, 1, "CALL", 1.e-8)
                bVolas[i].append(volaB)
                bStrikes[i].append(xStrikeBuehlerDiv)
    return {
        'TYPE' : 'GRID',
        'EXPIRIES' : bExpiries,
        'STRIKES' : bStrikes,
        'VOLAS' : bVolas
    }



# transform dividends from "spot dividend" model with absolute dividends
# into Buehler model with
#   - absolute dividends before <start>
#   - proportional dividends after <end>
#   - a mixture of absolute/proportional dividends between
#       <start> and <end>
def transformDividends(refDate, underlying, discount, start, end):
    dc = analytics.DayCounter(enums.DayCounter.ACT365_FIXED)

    udlCopy = copy.deepcopy(underlying)
    for udl in underlying.keys():
        udlAggrDiv = copy.deepcopy(underlying[udl])
        divsByDate = {}
        bDivAbs = []
        bDivRel = []
        exDates = []
        payDates = []
        tFactors = []
        absDivs = []
        relDivs = []
        for i in range(0, len(underlying[udl]['DIVIDENDS']['EXDATES'])):
            exDate = underlying[udl]['DIVIDENDS']['EXDATES'][i]
            if exDate not in divsByDate:
                divsByDate[exDate] = []
            divsByDate[exDate].append([underlying[udl]['DIVIDENDS']['CASH'][i],
                                       underlying[udl]['DIVIDENDS']['TAX'][i],
                                       underlying[udl]['DIVIDENDS']['PAYDATES'][i]]
            )
        for exDate in sorted(divsByDate.keys()):
            cashDivs = [d[0] for d in divsByDate[exDate]]
            taxFactors = [d[1] for d in divsByDate[exDate]]
            totalDiv = 0
            netDiv = 0
            for i in range(0, len(cashDivs)):
                totalDiv += cashDivs[i]
                netDiv += cashDivs[i] * taxFactors[i]
            averageTaxFactor = netDiv / totalDiv
            exDates.append(exDate)
            tFactors.append(averageTaxFactor)
            payDates.append(divsByDate[exDate][0][2])
            absDivs.append(totalDiv)
            relDivs.append(0.0)
            
        udlAggrDiv['DIVIDENDS'] = pd.DataFrame({
            'EXDATES'  : exDates,
            'PAYDATES' : payDates,
            'YIELD'    : relDivs,
            'CASH'     : absDivs,
            'TAX'      : tFactors
            })
        fwd = mkt_converter.fwd_from_dict(udlAggrDiv, udl, discount, 'EUR', refDate)
        
        for exDate in sorted(divsByDate.keys()):
            yf = dc.yf(refDate, converter.getLTime(exDate.to_pydatetime()))
            if yf < start:
                g = 0.0
            elif yf < end:
                g = (yf - start) / (end - start)
            else:
                g = 1.0
            f = fwd.value(refDate, converter.getLTime(exDate.to_pydatetime()))
            cashDivs = [d[0] for d in divsByDate[exDate]]
            taxFactors = [d[1] for d in divsByDate[exDate]]
            totalDiv = 0
            netDiv = 0
            for i in range(0, len(cashDivs)):
                totalDiv += cashDivs[i]
                netDiv += cashDivs[i] * taxFactors[i]
            bDivAbs.append((1-g) * totalDiv)
            bDivRel.append(g * totalDiv / (f + netDiv))

        udlCopy[udl]['DIVIDENDS'] = pd.DataFrame({
            'EXDATES'  : exDates,
            'PAYDATES' : payDates,
            'YIELD'    : bDivRel,
            'CASH'     : bDivAbs,
            'TAX'      : tFactors
            })
    return udlCopy
