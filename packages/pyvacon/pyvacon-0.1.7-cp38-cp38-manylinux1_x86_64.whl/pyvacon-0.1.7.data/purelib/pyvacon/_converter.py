# -*- coding: utf-8 -*-
"""
Created on Thu May 12 05:32:45 2016

@author: oeltz
"""
import numpy as np
from datetime import datetime
from datetime import timedelta
import pyvacon.analytics as analytics
#from . import enums

def date_range(start, end, delta = timedelta(days=1)):
    """
    generate a range of dates from start to end for a given timestep 
    
    start start date
    end end date
    delta timedelta, if not set, 1 day is used (datetime.timedelta(days=1))
    """
    date_list = []
    date_list.append(start)
    #if delta is None:
    #    delta = datetime.timedelta(days=1)
    while date_list[-1] < end:
        d = date_list[-1] + delta
        date_list.append(d)  
    return date_list        

def getLTime(d, refdate = None):
    #print(str(d))
    if type(d) is analytics.ptime:
        return d
          
    if type(d) is datetime:
        result = analytics.ptime(d.year, d.month, d.day, d.hour, d.minute, d.second)
        return result
    
    if refdate is None:
        Exception('Either reference date must be given or date must be of type datetime or ptime')
    
    refdate2 = getLTime(refdate)
    result = analytics.ptime()
    refdate2.addDays(result, d)
    return result
 


def _convert(x):
    if isinstance(x, datetime):
        return getLTime(x)
    if isinstance(x,list) and len(x)>0:
        if isinstance(x[0], datetime):
            return [getLTime(y) for y in x]
        if isinstance(x[0], analytics.CouponDescription):
            coupons = analytics.vectorCouponDescription()
            for coupon in x: 
                coupons.append(coupon)
            return coupons

    return x

def converter(f):
    def wrapper(*args, **kwargs):
        new_args = [_convert(x) for x in args]
        result = f(*new_args, **kwargs)        
        return result
    return wrapper

import inspect
from types import MethodType

def _get_dict_repr(obj):
    import json

    def cleanup_dict(d):
        if not isinstance(d, dict):
            return d;
        if len(d) == 1:
            for v in d.values():
                return v
        new_dict = {}
        for item, value in d.items():
            if item != 'cereal_class_version' and item != 'polymorphic_id' and item != 'UID_':
                if isinstance(value, dict):
                    if len(value) == 1:
                        for v in value.values():
                            new_dict[item] = v
                    else:
                        new_dict[item] = cleanup_dict(value)
                elif isinstance(value, list):
                    new_dict[item] = [cleanup_dict(vv) for vv in value]
                else:
                    new_dict[item] = value
        return new_dict
        
    repr = str(analytics.BaseObject.getString(obj)) + '}'
    d = json.loads(repr)
    return cleanup_dict(d['value0'])

def _get_string_rep(obj):
    d = _get_dict_repr(obj)
    return str(d)

import sys
if sys.version_info >= (3,0,):    
    def _add_converter(cls):
        for attr, item in inspect.getmembers(cls, inspect.isfunction): #for python 2 : ismethod
            setattr(cls, attr, converter(item))
        for name, method in inspect.getmembers(cls, lambda o: isinstance(o, property)):
            setattr(cls,name, property(converter(method.fget), converter(method.fset)))
        setattr(cls, '__str__', _get_string_rep)
        setattr(cls, 'get_dictionary', _get_dict_repr)
        return cls
else:
    def _add_converter(cls):
        for attr, item in inspect.getmembers(cls, inspect.ismethod): #for python 2 : ismethod
            setattr(cls, attr, converter(item))
        for name, method in inspect.getmembers(cls, lambda o: isinstance(o, property)):
            setattr(cls,name, property(converter(method.fget), converter(method.fset)))
        setattr(cls, '__str__', _get_string_rep)
        setattr(cls, 'get_dictionary', _get_dict_repr)
        return cls



def convertFromVector(x):
    result = []
    for i in x:
        result.append(i)
    return result
    
def convertToVector(x):
    result = analytics.vectorDouble(len(x))
    for i in range(len(x)):
        result[i] = x[i]
    return result        
    
def createPTimeList(refDate, dates):
    #ptimes = []
    #print(str(dates))
    ptimes = analytics.vectorPTime(len(dates))
    for i in range(len(dates)):
        ptimes[i] = getLTime(dates[i], refDate)
    return ptimes
    
def create_datetime(ptime):
    return datetime(ptime.year(), ptime.month(), ptime.day(), ptime.hours(), ptime.minutes(), ptime.seconds())

def create_datetime_list(ptimes):
    result = []
    for x in ptimes:
        result.append(create_datetime(x))
    return result

def relativeToAbsolute(refDate, dateVec):
    result = []
    for i in dateVec:
        tmp = analytics.ptime()
        refDate.addDays(tmp, i)
        result.append(tmp)
    return result

def np_matrix_from_correlation_dictionary(correlation_dict, factor_list, missing_value):
    """
    This method builds up a (correlation) matrix from a dictionary of single pairwise correlations and a list of factors included into the correlation list. It fills 
    the missing elements with the value specified as missing_value
    """
    result = np.full([len(factor_list),len(factor_list)], missing_value)
    for i in range(len(factor_list)):
        result[i,i] = 1.0
        for j in range(len(factor_list)):
            if (factor_list[i],factor_list[j]) in correlation_dict:
               result[i,j] = correlation_dict[(factor_list[i],factor_list[j])]
               result[j,i] = correlation_dict[(factor_list[i],factor_list[j])]
    return result

def to_np_matrix(mat):
    """
    Convert a vector<vector<double>> to a numpy matrix
    """
    if len(mat) == 0:
        return np.empty([0,0])
    result = np.empty([len(mat), len(mat[0])])
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            result[i][j] = mat[i][j]
    return result

def from_np_matrix(mat):
    rows, cols = mat.shape
    result = analytics.vectorVectorDouble(rows)
    for i in range(rows):
        tmp = analytics.vectorDouble(cols)
        for j in range(cols):
            tmp[j] = mat[i][j]
        result[i] = tmp
    return result

def np_matrix_from_transition(trans_matrix, time_to_maturity):
    """
    returns a numpy matrix form the given transition matrix and given time horizon
    
    trans_matrix transition matrix
    time_to_maturity time horizon for which transition matrix is created
    """
    matrix = analytics.vectorDouble()
    trans_matrix.computeTransition(matrix, time_to_maturity)
    tmp = []
    for i in range(analytics.Rating.nRatings()):
        tmp1 = []
        for j in range(analytics.Rating.nRatings()):
            tmp1.append(matrix[i*analytics.Rating.nRatings() + j])
        tmp.append(tmp1)
    plot_matrix = np.matrix(tmp)
    return plot_matrix
    
def transition_from_np_matrix(trans_matrix, np):
    """
    set the entries of the given transition matrix to the values of the numpy matrix
    
    
    """
    for i in range(analytics.Rating.nRatings()):
        for j in range(analytics.Rating.nRatings()):
            trans_matrix.setEntry(i,j,np[i,j])

def adjust_transition(name, trans_matrix_orig, ratings, factor, refdate):
    if isinstance(ratings, str):
        ratings = [ratings]
    np_matrix = np_matrix_from_transition(trans_matrix_orig, 1.0)
    transition_new = analytics.TimeScaledRatingTransition(name, refdate, 1.0)
    for rating in ratings:
        i = analytics.Rating.getRatings().index(rating)
        row_sum = 0
        for j in range(analytics.Rating.nRatings()-1):
            correction = factor*np_matrix[i,j] 
            row_sum += correction
            np_matrix[i,j] -= correction 
        #print(str(np_matrix[i,i]) + ' ' + str(np_matrix[i,i+1]))
        np_matrix[i,analytics.Rating.nRatings()-1] += row_sum
        transition_from_np_matrix(transition_new, np_matrix)
    return transition_new

def pricing_errors(spec_ids, bid, ask, theo):
     """
     Computes pricing errors for the givenspec ids between bid/ask and the theo
     """
     error = {}
     for key in spec_ids:
        error[key] = 0
        if key in bid:
            error[key] = -np.maximum(bid[key] - theo[key], 0) /np.maximum(1.0, bid[key]) 
        if key in ask:
            if error[key] == 0:
                error[key] = np.maximum(theo[key] - ask[key], 0)/np.maximum(1.0, ask[key])
     return error
    

def error_statistics_bonds(errors, spec_details, maturity_buckets = [1.0, 5.0, 7.0, 10.0, 15.0]):
    """
    assemble some statistics on the given pricing errors
    
    errors pricing errors as constructed from the method pricing_errors
    spec_details the details for the specifications as constructed from the environments specifications with get_details
    maturity_buckets list of time to maturities to group errors according to their expiry (given as ACT365 fixed yearfractions)    
    """
    result = { }
    
    by_maturity = {}
    for v in maturity_buckets:
        by_maturity[v] = []

    by_rating = {}
    for r in analytics.Rating.getRatings():
        by_rating[r] = []
        
    by_sec_lvl = {analyticsEnums.SecuritizationLevel.COLLATERALIZED : [], analyticsEnums.SecuritizationLevel.EQUITY : [],
                  analyticsEnums.SecuritizationLevel.MEZZANINE : [], analyticsEnums.SecuritizationLevel.SENIOR_SECURED : [],
                analyticsEnums.SecuritizationLevel.SENIOR_UNSECURED : [],  analyticsEnums.SecuritizationLevel.SUBORDINATED : []}
    by_sector = {}
    by_country = {}
    maturity_buckets.append(1000)
    n_errors = len(errors.items())
    all_errors = []
    for key, value in errors.items():
        all_errors.append(value)
        spec_detail = spec_details[key]
        maturity_bucket = next(v for v in maturity_buckets if v > spec_detail['maturity'])
        by_maturity[maturity_bucket].append(value) 
        by_rating[spec_detail['rating']].append(value)
        by_sec_lvl[spec_detail['sec_lvl']].append(value)
        if spec_detail['sector'] not in by_sector.keys():
            by_sector[spec_detail['sector']] = []
        by_sector[spec_detail['sector']].append(value)
        if spec_detail['country'] not in by_country.keys():
            by_country[spec_detail['country']] = []
        by_country[spec_detail['country']].append(value)
    result['maturity'] = by_maturity
    result['rating'] = by_rating
    result['sec_lvl'] = by_sec_lvl
    result['sector'] = by_sector
    result['country'] = by_country
    result['all'] = all_errors
    return result