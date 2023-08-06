# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""

import pyvacon.analytics as _analytics
from pyvacon._converter import _add_converter

BaseModel = _add_converter(_analytics.BaseModel)
RatesModel  = _add_converter(_analytics.RatesModel)
ShortRateModel1D = _add_converter(_analytics.ShortRateModel1D)
CIRModel = _add_converter(_analytics.CIRModel)
HullWhiteModel = _add_converter(_analytics.HullWhiteModel)
EquityFxModel = _add_converter(_analytics.EquityFxModel)
HestonModel = _add_converter(_analytics.HestonModel)
ScottChesneyModel = _add_converter(_analytics.ScottChesneyModel)
ExponentialOrnsteinUhlenbeck = _add_converter(_analytics.ExponentialOrnsteinUhlenbeck)
StochasticLocalVolatility = _add_converter(_analytics.StochasticLocalVolatility)
BuehlerLocalVolModel = _add_converter(_analytics.BuehlerLocalVolModel)

