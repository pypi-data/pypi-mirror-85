# -*- coding: utf-8 -*-
"""


Spyder Editor

This is a temporary script file.
"""
import pyvacon.analytics as analytics
import pyvacon.tools.converter as converter
import pyvacon.tools.enums as enums

def heston_from_dict(dict, refdate):
    return analytics.HestonModel(dict['OBJ_ID'], refdate, dict['S0'], dict['V0'], dict['THETA'], dict['KAPPA'], dict['ALPHA'], dict['RHO'])

def scott_chesney_from_dict(dict, refdate):
    return analytics.ScottChesneyModel(dict['OBJ_ID'], refdate, dict['S0'], dict['V0'], dict['KAPPA'], dict['THETA'], dict['ALPHA'], dict['RHO'])

def stochvolmodel_from_dict(model_dict, refdate):
    if model_dict['TYPE'] == 'HESTON':
        return heston_from_dict(model_dict, refdate)
    else:
       if model_dict['TYPE'] == 'SCOTT_CHESNEY':
            return scott_chesney_from_dict(model_dict, refdate) 

def stochvolmodel_to_dict(model, dict):
    model_type = model.getModelType();
    result = {}
    model_param = analytics.vectorDouble();
    model.getParameters(model_param)
    if model_type == 'HESTON':
        dict['V0'] = model_param[0]
        dict['THETA'] = model_param[1]
        dict['KAPPA'] = model_param[2]
        dict['ALPHA'] = model_param[3]
        dict['RHO'] = model_param[4]
        return
    if model_type == 'SCOTT_CHESNEY':
        dict['V0'] = model_param[0]
        dict['THETA'] = model_param[3]
        dict['KAPPA'] = model_param[2]
        dict['ALPHA'] = model_param[1]
        dict['RHO'] = model_param[4]
        return