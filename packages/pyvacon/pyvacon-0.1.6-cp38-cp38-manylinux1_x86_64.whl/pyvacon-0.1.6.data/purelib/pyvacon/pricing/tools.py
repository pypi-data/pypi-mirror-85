import pylab as pl
import pyvacon.analytics as analytics
import numpy as np
import pyvacon.tools.enums as analytics_enums
import pyvacon.tools.converter as converter
from scipy import optimize



def create_vega_bucket_report(pricing_data, x_strikes, expiries, shiftsize, scale_x, scale_t, bucket_type = 'RBF', price_diffs = False):
    '''
    create vega bucket report
    pricing_data the pricing data object (must be of type Black76PricingData, LocalVolPdePricingData or ComboPricingData with LocalVolPdePricingData constituents
    x_strikes[] the x strikes for the bucket report
    expiries[] the time to maturity in year fractions
    shiftsize the bucket shift size
    scale_x bucket parametrization
    scale_t bucket parametrization
    bucket_type 'RBF' or 'LOCAL_RBF'
    price_diffs if True the output is simply the price difference and the price_diff divided by the shift_size otherwise
    vol_scenarios list of volatility scenarios (including spot or dividend shifts)
    hedge_ins list of dictionaries of the hedge instruments, strike (absolut terms), expiry (in number of days), flag if Call 'C' or Put 'P' 
    '''
    
    # this is the special case for a combo instrument: we call the regular report recursively
    if isinstance(pricing_data, analytics.ComboPricingData):
        weights = pricing_data.spec.getMemberWeights()
        p_data = pricing_data.getLocalVolPdePricingData()
        bucket_vegas = np.zeros( shape=(len(expiries), len(x_strikes)) )
        for i in range(len(weights)):
            tmp = create_vega_bucket_report(p_data[i], x_strikes, expiries, shiftsize, scale_x, scale_t, bucket_type, price_diffs)
            bucket_vegas += weights[i]*tmp
        return bucket_vegas

    # save the original vol and pricing request
    if isinstance(pricing_data, analytics.LocalVolMonteCarloPricingData):
        orig = pricing_data.vols[0]
    else:
        orig = pricing_data.vol
    orig_pricing_request = pricing_data.pricingRequest

    # use a simple pricing request and determin the base price
    pricing_data.pricingRequest = analytics.PricingRequest()
    price_orig = analytics.price(pricing_data).getPrice()

    # create a bucket volatility surface of given type
    vol_bucket_surface = analytics.VolatilitySurfaceBucketShifted(orig, x_strikes, expiries, shiftsize)
    if bucket_type == 'RBF':
        vol_bucket_surface.setRBF(scale_x, scale_t)
    else:
        vol_bucket_surface.setSimpleExponentialLocalSupport(scale_x, scale_t)
    
    # set the shifted vol into the pricing request
    if isinstance(pricing_data, analytics.LocalVolMonteCarloPricingData):
        pricing_data.vols[0] =  vol_bucket_surface
    else:
        pricing_data.vol = vol_bucket_surface

    # loop over all the buckets and determine the price differences
    bucket_vegas = np.zeros( shape=(len(expiries), len(x_strikes)) )
    for i in range(len(x_strikes)):
        for j in range(len(expiries)):
            vol_bucket_surface.setBucket(i, j)
            pr = analytics.price(pricing_data)
            if price_diffs:
                bucket_vegas[j,i] = pr.getPrice() - price_orig
            else:
                bucket_vegas[j,i] = (pr.getPrice() - price_orig)/shiftsize

    # restore the original values for vol and pricing request 
    if isinstance(pricing_data, analytics.LocalVolMonteCarloPricingData):
        pricing_data.vols[0] =  orig
    else:
        pricing_data.vol = orig
    pricing_data.pricingRequest = orig_pricing_request

    return bucket_vegas


def compute_vega_bucket_hedge(hedge_ins, ins_pricing_data, x_strikes, expiries, shiftsize, scale_x, scale_t, bucket_type = 'RBF', optimMethod='Powell', 
                       optimOptions = {'xtol': 1e-3, 'ftol': 1e-3, 'maxiter': 20, 'maxfev': 200, 'disp': True}):
    '''
    copute vega bucket hedge for given set of hedge instruments minimizing the sum of squared errors
    hedge_ins list of dictionaries of the hedge instruments, strike (absolut terms), expiry (in number of days), flag if Call 'C' or Put 'P' 
    ins_pricing_data the pricing data object (must be of type LocalVolPdePricingData or ComboPricingData with LocalVolPdePricingData constituents
    x_strikes[] the x strikes for the bucket report
    expiries[] the time to maturity as year fractions for the bucket report
    shiftsize the bucket shift size
    scale_x bucket parametrization
    scale_t bucket parametrization
    bucket_type 'RBF' or 'LOCAL_RBF
    optim_method the optimizer used to calculate the hedge ('Powell' as default)
    optim_options optimization parameter
    '''

    if isinstance(ins_pricing_data, analytics.ComboPricingData):
        pde_pricing_data = ins_pricing_data.getLocalVolPdePricingData()    
        orig_vol = pde_pricing_data[0].vol
        val_date = pde_pricing_data[0].valDate
        dsc = pde_pricing_data[0].dsc
    else:
        orig_vol = ins_pricing_data.vol
        val_date = ins_pricing_data.valDate
        dsc = ins_pricing_data.dsc

    # create the bucket report for the instrument to be hedged
    price_diffs_ins = create_vega_bucket_report(ins_pricing_data, x_strikes, expiries, shiftsize, scale_x, scale_t,  bucket_type, True)

    # create the bucket reports for the hedge instruments
    price_diffs_hedge = []
    pricing_data = analytics.Black76PricingData()
    pricing_data.valDate = val_date
    pricing_data.vol = orig_vol
    pricing_data.dsc = dsc
    pricing_data.param = analytics.PricingParameter()
    pricing_data.pricingRequest = analytics.PricingRequest()

    for i in range(len(hedge_ins)):
        pricing_data.spec = analytics.EuropeanVanillaSpecification('','', analytics_enums.SecuritizationLevel.NONE, 'EUR', 'dummy', hedge_ins[i]['PAYOFF'], 
                                                                   hedge_ins[i]['EXPIRY'], hedge_ins[i]['STRIKE'])
        price_diffs_hedge.append(create_vega_bucket_report(pricing_data, x_strikes, expiries, shiftsize, scale_x, scale_t,  bucket_type, True))

    # error function as sum of square errors
    def compute_error_function(weights):
        result = 0.0
        for i in range(price_diffs_hedge[0].shape[0]):
            for j in range(price_diffs_hedge[0].shape[1]):
                error = price_diffs_ins[i,j]
                for k in range(len(weights)):
                    error += weights[k]*price_diffs_hedge[k][i,j]
                result += error*error
        return result

    x = np.zeros([len(hedge_ins)])
    result = optimize.minimize(compute_error_function, x, method=optimMethod,
              options=optimOptions)

    return result


def compute_scenario_hedge(pricing_data, vol_scenarios, vol_scenario_weights, hedge_ins, optimMethod='Powell', 
                       optimOptions = {'xtol': 1e-3, 'ftol': 1e-3, 'maxiter': 20, 'maxfev': 200, 'disp': True}):
    '''
    compute hedge weights such that the hedge is optimal for the given scenarios.
    pricing_data pricing data for the instrument to be hedged in the base scenario
    vol_scenarios list of volatility scenarios (potentially including spot or dividend shifts)
    hedge_ins list of dictionaries of the hedge instruments, strike (absolut terms), expiry (in number of days), flag if Call 'C' or Put 'P' 
    '''

    # save the original volatility and pricing request
    if isinstance(pricing_data, analytics.ComboPricingData):
        pde_pricing_data = pricing_data.getLocalVolPdePricingData()    
        orig_vol = pde_pricing_data[0].vol
        orig_pricing_request = pde_pricing_data[0].pricingRequest
        val_date = pde_pricing_data[0].valDate
        dsc = pde_pricing_data[0].dsc
    else:
        orig_vol = pricing_data.vol
        orig_pricing_request = pricing_data.pricingRequest
        val_date = pricing_data.valDate
        dsc = pricing_data.dsc
    
    # calculate the base price
    base_price = analytics.price(pricing_data).getPrice()
    ins_price_diffs = np.full([len(vol_scenarios)], base_price)
    
    # run through all scenarios and determine the price differences for the instrument to be hedged
    for i in range(len(vol_scenarios)):
        if isinstance(pricing_data, analytics.ComboPricingData):
            pde_pricing_data = pricing_data.getLocalVolPdePricingData()
            
            for p_data in pde_pricing_data:
                p_data.vol = vol_scenarios[i]
                p_data.pricingRequest = analytics.PricingRequest()
        else:
            pricing_data.vol = vol_scenarios[i]
            pricing_data.pricingRequest = analytics.PricingRequest()
        ins_price_diffs[i] -= analytics.price(pricing_data).getPrice()

    # restore the original volatility and pricing request
    if isinstance(pricing_data, analytics.ComboPricingData):
        pde_pricing_data = pricing_data.getLocalVolPdePricingData()
            
        for p_data in pde_pricing_data:
            p_data.vol = orig_vol
            p_data.pricingRequest = orig_pricing_request
    else:
        pricing_data.vol = orig_vol
        pricing_data.pricingRequest = orig_pricing_request

    # now calculate the price differences for all scenarios for the different hedge instruments
    b76_pricing_data = analytics.Black76PricingData()
    b76_pricing_data.valDate = val_date
    b76_pricing_data.dsc = dsc
    b76_pricing_data.param = analytics.PricingParameter()
    b76_pricing_data.pricingRequest = analytics.PricingRequest()
    hedge_price_diffs = np.empty([len(hedge_ins), len(vol_scenarios)])
    for i in range(len(hedge_ins)):
        b76_pricing_data.spec = analytics.EuropeanVanillaSpecification('','', analytics_enums.SecuritizationLevel.NONE, 'EUR', 'dummy', hedge_ins[i]['PAYOFF'], 
                                                                   hedge_ins[i]['EXPIRY'], hedge_ins[i]['STRIKE'])
        b76_pricing_data.vol = orig_vol
        base_price = analytics.price(b76_pricing_data).getPrice()
        for j in range(len(vol_scenarios)):
            b76_pricing_data.vol = vol_scenarios[j]
            hedge_price_diffs[i,j] = base_price - analytics.price(b76_pricing_data).getPrice()
    
    # error function as sum of squared errors 
    def compute_error_function(weights):
        result = 0.0
        for i in range(len(vol_scenario_weights)):
            error = ins_price_diffs[i]
            for j in range(len(hedge_ins)):
                error += weights[j]*hedge_price_diffs[j,i]
            result += vol_scenario_weights[i]*error*error
        return result
    
    x = np.zeros([len(hedge_ins)])
    result = optimize.minimize(compute_error_function, x, method=optimMethod, options=optimOptions)
    return result
    
    
    
#def extract_simulated_cashflows(pricing_results):
def cashflow_profile(pricing_results):
    """
    plots the cashflow profiles for the pricing data
    pricing_results: pricing results returned by a price call
    """
    cashflows = pricing_results.getCashflowSlices()
    ntimes = cashflows.cashflowSlices.size()
    result = np.zeros( [ntimes, len(cashflows.cashflowSlices[0])])
    for i in range(ntimes):
        if i > 0:
            result[ntimes-1-i] += result[ntimes-i] 
        for j in range(result.shape[1]):
            result[ntimes-1-i][j] += cashflows.cashflowSlices[ntimes-1-i][j]     
    return result


def project_model_param(pricing_data, model_ref, model_param, param_start, param_end, param_step):
    """
    project price by a certain model parameter
    pricing_data: the pricing_data used for pricing
    model_ref: the model which will be projected (and which must be included in the pricing data so that it will be used for pricing)
    model_param: name of model parameter (as defined in the parameter description of the model) or just the number in the models parameter vector
    param_start: start value of model
    param_end: end value of model
    param_step: stepwidth between start and end values
    """
    index = model_param
    params = model_ref.getParameterDescripion()
        
    if type(model_param) is str:
        index = -1
        for i in range(len(params)):
            if params[i] == model_param:
                index = i
    if index <0 or index > len(params):
        raise('Invalid model parameter')
    param_v = pl.frange(param_start,param_end,param_step)
    param_vec = analytics.vectorDouble()
    model_ref.getParameters(param_vec)
    prices = []
    for p in param_v:
        param_vec[index] = p
        model_ref.setParameters(param_vec)
        pr = analytics.price(pricing_data)
        prices.append(pr.getPrice())
    return prices, param_v, index