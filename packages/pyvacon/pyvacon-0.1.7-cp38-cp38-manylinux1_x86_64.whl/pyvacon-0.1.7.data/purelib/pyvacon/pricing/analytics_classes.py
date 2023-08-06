# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
import pyvacon.analytics as _analytics
from pyvacon._converter import  _add_converter
from pyvacon._converter import  converter as _converter



#pricing data
BasePricingData =_add_converter(_analytics.BasePricingData)

ComboPricingData =_add_converter(_analytics.ComboPricingData)

Black76PricingData =_add_converter(_analytics.Black76PricingData)
LocalVolPdePricingData =_add_converter(_analytics.LocalVolPdePricingData)
AsianRiskControlPricingData =_add_converter(_analytics.AsianRiskControlPricingData)
LocalVolMonteCarloPricingData =_add_converter(_analytics.LocalVolMonteCarloPricingData)
StochasticVolMonteCarloPricingData =_add_converter(_analytics.StochasticVolMonteCarloPricingData)


InterestRateSwapLegPricingData =_add_converter(_analytics.InterestRateSwapLegPricingData)
InterestRateSwapFloatLegPricingData =_add_converter(_analytics.InterestRateSwapFloatLegPricingData)
InterestRateSwapPricingData =_add_converter(_analytics.InterestRateSwapPricingData)

BondPricingData =_add_converter(_analytics.BondPricingData)
InflationLinkedBondPricingData =_add_converter(_analytics.InflationLinkedBondPricingData)
CallableBondPdePricingData =_add_converter(_analytics.CallableBondPdePricingData)

#pricing parameter
BondPricingParameter = _add_converter(_analytics.BondPricingParameter)
CallableBondPdePricingParameter = _add_converter(_analytics.CallableBondPdePricingParameter)


PricingRequest = _add_converter(_analytics.PricingRequest)
getPricingData = _converter(_analytics.getPricingData)




