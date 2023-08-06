# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
import numpy as np
import pyvacon.analytics as _analytics
import pyvacon._converter as _converter 

InflationIndexForwardCurve = _converter._add_converter(_analytics.InflationIndexForwardCurve)

ComboSpecification = _converter._add_converter(_analytics.ComboSpecification)
#Equity/FX
PayoffStructure = _converter._add_converter(_analytics.PayoffStructure)
ExerciseSchedule = _converter._add_converter(_analytics.ExerciseSchedule)
BarrierDefinition = _converter._add_converter(_analytics.BarrierDefinition)
BarrierSchedule = _converter._add_converter(_analytics.BarrierSchedule)
BarrierPayoff = _converter._add_converter(_analytics.BarrierPayoff)
BarrierSpecification = _converter._add_converter(_analytics.BarrierSpecification)
EuropeanVanillaSpecification = _converter._add_converter(_analytics.EuropeanVanillaSpecification)
AmericanVanillaSpecification = _converter._add_converter(_analytics.AmericanVanillaSpecification)
RainbowUnderlyingSpec = _converter._add_converter(_analytics.RainbowUnderlyingSpec)
RainbowBarrierSpec = _converter._add_converter(_analytics.RainbowBarrierSpec)
LocalVolMonteCarloSpecification = _converter._add_converter(_analytics.LocalVolMonteCarloSpecification)
RainbowSpecification = _converter._add_converter(_analytics.RainbowSpecification)
MultiMemoryExpressSpecification = _converter._add_converter(_analytics.MultiMemoryExpressSpecification)
MemoryExpressSpecification = _converter._add_converter(_analytics.MemoryExpressSpecification)
ExpressPlusSpecification = _converter._add_converter(_analytics.ExpressPlusSpecification)
AsianVanillaSpecification = _converter._add_converter(_analytics.AsianVanillaSpecification)
RiskControlStrategy = _converter._add_converter(_analytics.RiskControlStrategy)
AsianRiskControlSpecification = _converter._add_converter(_analytics.AsianRiskControlSpecification)


#Interest Rates
IrSwapLegSpecification = _converter._add_converter(_analytics.IrSwapLegSpecification)
IrFixedLegSpecification = _converter._add_converter(_analytics.IrFixedLegSpecification)
IrFloatLegSpecification = _converter._add_converter(_analytics.IrFloatLegSpecification)
InterestRateSwapSpecification = _converter._add_converter(_analytics.InterestRateSwapSpecification)
InterestRateBasisSwapSpecification = _converter._add_converter(_analytics.InterestRateBasisSwapSpecification)
DepositSpecification = _converter._add_converter(_analytics.DepositSpecification)
InterestRateFutureSpecification = _converter._add_converter(_analytics.InterestRateFutureSpecification)



#Bonds/Credit
CouponDescription = _converter._add_converter(_analytics.CouponDescription)
BondSpecification = _converter._add_converter(_analytics.BondSpecification)
InflationLinkedBondSpecification = _converter._add_converter(_analytics.InflationLinkedBondSpecification)
CallableBondSpecification = _converter._add_converter(_analytics.CallableBondSpecification)

GasStorageSpecification = _converter._add_converter(_analytics.GasStorageSpecification)

ScheduleSpecification = _converter._add_converter(_analytics.ScheduleSpecification)

SpecificationManager = _converter._add_converter(_analytics.SpecificationManager)

vectorCouponDescription = _analytics.vectorCouponDescription
vectorRainbowBarrierSpec = _analytics.vectorRainbowBarrierSpec
vectorRainbowUdlSpec = _analytics.vectorRainbowUdlSpec

#ProjectToCorrelation = _analytics.ProjectToCorrelation

