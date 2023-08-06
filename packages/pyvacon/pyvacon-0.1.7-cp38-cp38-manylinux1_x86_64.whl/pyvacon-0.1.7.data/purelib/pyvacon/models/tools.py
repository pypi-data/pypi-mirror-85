# -*- coding: utf-8 -*-
"""


Spyder Editor

This is a temporary script file.
"""
import pylab as pl
import matplotlib.pyplot as plt
import logging
import pyvacon.analytics as analytics
import pyvacon.tools.converter as converter
import pyvacon.tools.enums as enums
import math
import numpy as np

from scipy import optimize

logger = logging.getLogger('model.tools')

def getRefDate():
    refDate = analytics.ptime(2016,1,1,23,0,0)
    return refDate

def relativeToAbsolute(refDate, dateVec):
    result = []
    for i in dateVec:
        tmp = analytics.ptime()
        refDate.addDays(tmp, i)
        result.append(tmp)
    return result


def compute_yieldcurve(model, refdate, dates = None, key = None, dc = 'ACT365Fixed'):
    ''' Compute a discount curve for the given model via the method calcZeroBond provided by each models
        model the ShortRateModel1D used to comput the df, if model is not of his type, ane exception is thrown
        refdate reference date used to compute the curve
        dates list of dates used to compute discount factors. If no dates are given, a simple list is constructed (refdate+6 months for th next 20 years)
        key the key of the curve, if empty DC+model->id is used
        dc strin describin the daycounter used, defalt is ACT365Fixed
    '''
    #if not isinstance(model, analytics.ShortRateModel1D):
    #    raise Exception('Method up to now only implemenetd for 1D-Short rate models.')
    if key is None:
        key = 'DC_' + model.getObjectId()
    analytics_refdate = converter.getLTime(refdate)
    if dates is None:
        days = []
        for i in range(40):
            days.append((i+1)*180)
        dates = converter.relativeToAbsolute(analytics_refdate, days)

    analytics_dates = converter.createPTimeList(analytics_refdate, dates)
    daycounter = analytics.DayCounter(dc)
    df = []    
    for d in analytics_dates:
        df.append(model.calcZeroBond(d, analytics_refdate))
    dc = analytics.DiscountCurve(key, analytics_refdate, analytics_dates, df,dc, 'LINEARLOG', 'LINEARLOG')
    return dc

def compute_realized_vol_var(model_lab, expiry, n_component = 0):
    '''
    computes \sum_i ln(S_i+1/S_i) for each simulated spot path S_i
    '''
    result = [0] * model_lab.getNumSims();
    result_vol = [0] * model_lab.getNumSims();
    sims_prev = analytics.vectorDouble()
    sims_curr = analytics.vectorDouble()
    for i in range(1,expiry):
        model_lab.getTimeSlice(sims_prev, i-1, n_component)
        model_lab.getTimeSlice(sims_curr, i, n_component)
        for j in range(len(result)):
            tmp = math.log(sims_curr[j]/sims_prev[j])
            result[j] += tmp*tmp
    for j in range(len(result)):
        result_vol[j] = math.sqrt(result[j])    
    return result, result_vol
    
def compute_intertemporal_statistics(model_lab, y, expiries, n_components, f, statistics = np.mean):
    '''
    compute E(f([x1,x2,...] ,y)) where x=[xi] are the simulated values at times expiries = [expiry1,...]  (of n_component_1 and n_component_2) and y are just a range of parameters
    '''
    result = []
    sims = []
    sims_tmp = analytics.vectorDouble()
    model_lab.getTimeSlice(sims_tmp, expiries[0], n_components[0])
    for x in sims_tmp:
        sims.append([x])
    for i in range(1, len(expiries)-1):
        model_lab.getTimeSlice(sims_tmp, expiries[i], n_components[i])
        for x in sims_tmp:
            sims[i].append(x)  
    for yy in y:
        tmp = []
        for x in sims:
            tmp.append(f(x,yy))
        result.append(statistics(tmp))
    return result

def compute_statistics(model_lab, y, expiry_index, n_component, f, statistics = np.mean):
    '''

    '''
    
    result = []
    sims = analytics.vectorDouble()
    model_lab.getTimeSlice(sims, expiry_index, n_component)
  
    for yy in y:
        tmp = []
        for x in sims:
            tmp.append(f(x,yy))
        result.append(statistics(tmp))
    return result


def compute_implieds(expiries, model, nSims, nTimes, x_strikes, refDate, max_num_threads = 1, tol = 0.0001):
    ptimes = converter.createPTimeList(refDate, expiries)
    lab = analytics.ModelLab(model, refDate)
    lab.simulate(ptimes, nSims, nTimes, max_num_threads)
    result = np.empty([len(expiries), len(x_strikes)])
    for i in range(0,len(expiries)) :
        call_prices = compute_statistics(lab, x_strikes, i, 0, lambda x, y: max(x-y,0.0))
        expiry_yf = expiries[i] / 365.0
        for j in range(len(x_strikes)):
            result[i,j] = analytics.calcImpliedVol(call_prices[j], x_strikes[j], expiry_yf, 1.0, 1.0, 'C', tol)
    return result


def compute_stoch_vol_correlations(models, correlation_param_indices, stock_correlations, 
                                   default_stock_vol_corr, default_vol_vol_corr, 
                                   max_iter = 10000, min_eigenvalue = 0.0001):
    """
    This method computes an overall correlation matrix for stochstic volatility models, i.e. the correlations between 
    the variances of the different stoch vol models and the correlations between the stock and variances of the different models
    models: array of given stochastic vol models
    correlation_param: array of indices of the parameters of stock-vol correlation wihin each model, i.e. correlation_param[i] gives the index of the parameter of the i-th model describing the correlation
    stock_correlations: matrix of stock correlations
    default_stock_vol_corr: default value the algorithm starts with for correlations between the stock of one model and vol of other model
    default_vol_vol_corr: default value the algorithm starts with for correlations between the voltilities
    min_eigenvalue: minimum eigenvalue the resulting overall correlation matrix should have (due to numerical reasons it should be greater then 0)
    max_iter: maximum number of iterations used by the algorithm
    returns thre matrices: the hole correlation matrix, matrix with the stock-vol correlations (i-th row contains all correlations from stock i to variances) 
                and the matrix with the vol-vol correlations
    """
    # setup a correlation dictionary
    correlations = {}
    factors = []
    for i in range(len(models)):
        factors.append('S_'+str(i))
        factors.append('V_'+str(i))
        for j in  range(len(models)):
            correlations[('S_'+str(i),'S_'+ str(j))] = stock_correlations[i][j]
        param = analytics.vectorDouble()
        models[i].getParameters(param)
        correlations[('S_'+str(i),'V_'+str(i))] = param[correlation_param_indices[i]]
    
    #setup start matrix for algorithm
    corr_mat = converter.np_matrix_from_correlation_dictionary(correlations, factors, -1.0)
    #set the values for stock-vol and vol-vol correlations
    for i in range(len(models)):
        for j in range(len(models)):
            if i != j:
                corr_mat[2*i][2*j+1] = default_stock_vol_corr
                corr_mat[2*j+1][2*i] = default_stock_vol_corr
                corr_mat[2*i+1][2*j+1] = default_vol_vol_corr
                corr_mat[2*j+1][2*i+1] = default_vol_vol_corr
    # set the row and column indices of entries which will be untouched by the projection
    row_indices = [] 
    col_indices = []
    for i in range(len(models)):
        row_indices.append(2*i)
        col_indices.append(2*i+1)
        for j in range(i+1, len(models)):
            row_indices.append(2*i)
            col_indices.append(2*j)

    correlation_proj = converter.to_np_matrix(analytics.ProjectToCorrelation.projectToCorrelationMatrix(corr_mat,row_indices, col_indices,max_iter,min_eigenvalue))
    correlation_sV = np.empty([len(models), len(models)]) #stock-variance-correlations where i-th row contains all correlations to i-th stock
    correlation_vV = np.empty([len(models), len(models)]) #variance-variance correlations

    for i in range(len(models)):
        for j in range(len(models)):
            correlation_sV[i][j] = correlation_proj[2*i][2*j+1]
            correlation_vV[i][j] = correlation_proj[2*i+1][2*j+1]

    return correlation_proj, correlation_sV, correlation_vV

class BuehlerStochVolCalibrator:
    'class to calibrate buehler stoch volatility models and analyze the calibration errors'
    def __init__(self, refDate, expiries, xStrikes, vol, model, udl, nSims = 1000,  nTimeStepsPerYear = 50, maxNumThreads = 1):
        """refDate: reference date used to calibrate model
        expiries: list of days to expiry (w.r.t. the given reference Date)
        xStrikes: list of xStrikes used for calibration (all expiries having the same strike)
        target_prices: list of  target prices at given expiries and strikes, i.e. target_prices[i][j] = price of call at expiry[i] and xStrikes[j] (vols at a expiry for all xStrikes)"""
        self.xStrikes = xStrikes
        self.xStrikesCall = [x for x in xStrikes if x >=1.0 ]
        self.xStrikesPut = [x for x in xStrikes if x < 1.0 ]
        self.expiries = converter.createPTimeList(refDate, expiries)  #relativeToAbsolute(refDate, expiries)
        self.target_prices = []
        self.target_prices_call = []
        self.target_prices_put = []
        self.model = model
        self.udl = udl
        self.refDate = refDate
        self.nSims = nSims
        self.maxNumThreads = maxNumThreads
        self.nTimeSteps = nTimeStepsPerYear
        dc = analytics.DayCounter(enums.DayCounter.ACT365_FIXED)
        for i in range(len(expiries)):
            tc = []
            target_call = []
            target_put = []
            T = dc.yf(refDate, converter.getLTime(expiries[i], refDate))
            for j in range(len(xStrikes)):
                v = vol.calcImpliedVol(refDate, converter.getLTime(expiries[i], refDate), xStrikes[j])
                price = analytics.calcEuropeanCallPrice(xStrikes[j], T, 1.0, 1.0, v)
                tc.append(price)
                if xStrikes[j] >= 1.0:
                    target_call.append(analytics.calcEuropeanCallPrice(xStrikes[j], T, 1.0, 1.0, v))
                else:
                    target_put.append(analytics.calcEuropeanPutPrice(xStrikes[j], T, 1.0, 1.0, v))
            self.target_prices.append(tc)
            self.target_prices_call.append(target_call)
            self.target_prices_put.append(target_put)


    def __calc_implied_vols__(self, expiry_index, lab):
        call_prices = compute_statistics(lab, self.xStrikes, expiry_index, 0, lambda x, y: max(x-y,0.0))
        dc = analytics.DayCounter(enums.DayCounter.ACT365_FIXED)
        expiry = dc.yf(self.refDate, self.expiries[expiry_index])
        vols = []
        for i in range(len(call_prices)):
            vols.append(analytics.calcImpliedVol(call_prices[i],  self.xStrikes[i], expiry, 1.0, 1.0, 'C'))
        return vols
    
    def __set_model_params__(self, x):
        x_tp = analytics.vectorDouble(x)
        self.model.getParameters(x_tp)
        self.mapping(x_tp, x)
        self.model.setParameters(x_tp)
        
    def __calibrationErrorFunction__(self, x): #, refDate, model, expiries, targetVols, udl):
        logger.debug('Entering calibration error function.')
        self.__set_model_params__(x)
        lab = analytics.ModelLab(self.model, self.refDate)
        lab.simulate(self.expiries, self.nSims, self.nTimeSteps, self.maxNumThreads)
        error = 0
        for i in range(len(self.expiries)) :
            #vols = self.__calc_implied_vols__(i, lab)
            call_prices = compute_statistics(lab, self.xStrikesCall, i, 0, lambda x, y: max(x-y,0.0))
            put_prices = compute_statistics(lab, self.xStrikesPut, i, 0, lambda x, y: max(y-x,0.0))
            for j in range(len(self.xStrikesCall)):
                error  += ((self.target_prices_call[i][j] - call_prices[j]) / self.target_prices_call[i][j])**2
            for j in range(len(self.xStrikesPut)):
                error  += ((self.target_prices_put[i][j] - put_prices[j]) /self.target_prices_put[i][j]) **2
        #print(error)
        logger.debug('Leaving calibration error function, error = ' + str(error))
        return error
    
    def calibrate(self, x, mapping, optimMethod='Powell', optimOptions = {'xtol': 1e-3, 'ftol': 1e-3, 'maxiter': 20, 'maxfev': 200, 'disp': True}):
        """
        Calibrate the model using the chosen optimization method
        mapping: function to map the given x vector to the model parameters  
        optimMethod: optimization method used (from SciPy) may be Powell, BFGS, nelder-mead
        optimOptions: options for the optimizers (see SciPy docu for more information)
        """
        #'nelder-mead'
        #'BFGS'
        #'Powell'
        logger.info('Start calibration of stochastic volatility model with optimizer ' + optimMethod)
        self.mapping = mapping
        logger.info('Start parameter : ' + str(x))
        result= optimize.minimize(self.__calibrationErrorFunction__, x, method=optimMethod,
              options=optimOptions)  
        self.__set_model_params__(result['x'])
        logger.info('Finsihed calibration of stochastic volatility model.')

        #x = optimize.leastsq(self.calibrationErrorFunction, x, ) # args=(y_meas, x))
        
    def create_option_quote_table(self, xStrikes = None, spot = 1.0, issuer = 'DUMMY', secLevel = 'COLLATERALIZED', currency = 'EUR'):
        """
        Create an option quote table from the model
        """
        if xStrikes is None:
            xStrikes = self.xStrikes
        lab = analytics.ModelLab(self.model, self.refDate)
        lab.simulate(self.expiries, self.nSims, self.nTimeSteps, self.maxNumThreads)
        quoteTable = analytics.EquityOptionQuoteTable('QUOTE_TABLE:'+self.udl, self.refDate, spot, self.udl, issuer, secLevel, currency)
        isCall=[]        
        for j in range(len(xStrikes)):
            if xStrikes[j] < 1.0:
                isCall.append(False)
            else:
                isCall.append(True)
        for i in range(len(self.expiries)):
            vols = lab.getImpliedVolTimeSlice(self.udl, xStrikes, i, self.nSims)
            quoteTable.addQuotes(self.expiries[i], True, xStrikes, isCall, vols, vols)
        return quoteTable
        
    def plot_error_prices(self, expiry_indices = None):
        """
        Plot the calibration error        
        expiry_indices: indices specifying the expiries which shall be plottet, if not set, all expiries will be plottet
        """
        lab = analytics.ModelLab(self.model, self.refDate)
        lab.simulate(self.expiries, self.nSims, self.nTimeSteps, self.maxNumThreads)
        xStrikesPlot = pl.frange(0.5,1.5,0.1)
        if expiry_indices is None:
            expiry_indices = range(len(self.expiries))
        for i in expiry_indices:
            call_prices = compute_statistics(lab, self.xStrikes, i, 0, lambda x, y: max(x-y,0.0))
            plt.plot(self.xStrikes, self.target_prices[i], 'x', label='target for ' + self.expiries[i].to_string())
            plt.plot(self.xStrikes, call_prices, 'x', label='calibrated model for ' + self.expiries[i].to_string())
        plt.legend()

    def plot_error_vols(self, expiry_indices = None, diff = True):
        """
        Plot the calibration error w.r.t. implied vols    
        expiry_indices: indices specifying the expiries which shall be plottet, if not set, all expiries will be plottet
        """
        lab = analytics.ModelLab(self.model, self.refDate)
        lab.simulate(self.expiries, self.nSims, self.nTimeSteps, self.maxNumThreads)
        xStrikesPlot = pl.frange(0.5,1.5,0.1)
        dc = analytics.DayCounter(enums.DayCounter.ACT365_FIXED)
        if expiry_indices is None:
            expiry_indices = range(len(self.expiries))
        for i in expiry_indices:
            call_prices = compute_statistics(lab, self.xStrikes, i, 0, lambda x, y: max(x-y,0.0))
            target_vols = []
            model_vols = []
            vol_diff = []
            T = dc.yf(self.refDate, self.expiries[i])
            for j in range(len(self.xStrikes)):
                target_vols.append(analytics.calcImpliedVol(self.target_prices[i][j], self.xStrikes[j],T,1.0,1.0, 'C'))
                model_vols.append( analytics.calcImpliedVol(call_prices[j], self.xStrikes[j],T,1.0,1.0, 'C'))
                vol_diff.append(target_vols[-1] - model_vols[-1])
            if diff:
                plt.plot(self.xStrikes, vol_diff, '-x', label=  self.expiries[i].to_string())
            else:
                plt.plot(self.xStrikes, target_vols, '-x', label='target for ' + self.expiries[i].to_string())
                plt.plot(self.xStrikes, model_vols, '-o', label='calibrated model for ' + self.expiries[i].to_string())
        plt.legend()

    def get_calibration_expiries(self):
        return self.expiries

    def get_calibration_strikes(self):
        return self.xStrikes
        
    def getTargetVols(self):
        return self.targetVols
        
    def getModel(self):
        return self.Model


if __name__ == "__main__":
    v0 = math.log(0.3)
    theta = v0
    eta = 0.5
    rho = -0.5
    lam = 1.05
    udl = 'DBK'
    heston = analytics.SpotXHeston(v0, theta,eta, rho, lam, udl, getRefDate())
    
    
    dates =[ analytics.ptime(2016,4,2,23,0,0) ] #, analytics.ptime(2017,4,2,23,0,0) ]
    
    nSims = 1000
    nTimes = 50
    
    x =[v0, theta, eta, rho, lam] 
    model = analytics.SpotXScottChesney(v0, theta, eta, rho, lam, udl, getRefDate())
    expiries = [365]
    
    xStrikesCalib = [0.8, 1.0, 1.2]
    analytics.setLogLevel('VERBOSE')
    targetVols = [[0.35, 0.3, 0.27], [0.33, 0.33, 0.33]] 
    
    #for nSims in [1000, 2000, 4000, 8000, 16000]:
    calibrator = ModelCalibrator(getRefDate(), expiries, xStrikesCalib, targetVols, model, udl, nSims, 50)
    #model calibration
    x = calibrator.calibrateModel(x, 'nelder-mead')
    model.setParameter(x)
    print(x)
        
     
        
    xStrikesPlot = pl.frange(0.5,1.5,0.1)
    plt.figure()
    analyticsPlot.plotModelImpliedsByStrikes(calibrator.getCalibrationExpiries(), model, udl, nSims, nTimes, xStrikesPlot, getRefDate())
    for i in range(len(expiries)):
        plt.plot(xStrikesCalib, targetVols[i], 'x', label='target for ' + calibrator.getCalibrationExpiries()[i].to_string())
    plt.legend()
 
    plt.figure()
    analyticsPlot.plotModelSpotDistribution(calibrator.getCalibrationExpiries(), model, udl, nSims, nTimes, getRefDate())
 
    plt.figure()
    xStrikes = pl.frange(0.5,1.5,0.1)
    quoteTable = calibrator.createOptionQuoteTable(xStrikes)
    analyticsPlot.plotQuoteTable(quoteTable)
   
   #analyticsPlot.plotModelImpliedsByStrikes(dates, model, udl, nSims, 100, xStrikes, getRefDate())
    #rhos = [-0.9, -0.5, 0, 0.5, 0.9]
    #for rho in rhos:
    #    scottChesney = analytics.SpotXScottChesney(v0, theta, eta, rho, lam, udl, getRefDate())
    #    analyticsPlot.plotModelImpliedsByStrikes(dates, scottChesney, udl, nSims, 100, xStrikes, getRefDate(), str(eta) +': ')
    
    #plt.figure()
    #avPlot.plotModelSpotDistribution(dates, scottChesney, udl,nSims, 500, getRefDate(), 100)


