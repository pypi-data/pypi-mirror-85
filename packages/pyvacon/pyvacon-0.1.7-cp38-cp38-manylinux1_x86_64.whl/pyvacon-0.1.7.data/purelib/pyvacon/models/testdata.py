# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
from datetime import datetime
import pyvacon.analytics as analytics
import math
import analyticsEnums
import analyticsUtils as utils

def all_data(env):
    cir = analytics.CIRModel(1.0,1.0,0.1,0.05)
    env.calibstore.add('EUR6M', cir)
    cir = analytics.CIRModel(1.0,1.0,0.01,0.005)
    env.calibstore.add('EONIA', cir)
    
    