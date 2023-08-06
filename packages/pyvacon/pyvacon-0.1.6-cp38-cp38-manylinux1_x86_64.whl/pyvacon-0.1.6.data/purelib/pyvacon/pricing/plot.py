import matplotlib.pyplot as plt
import pylab as pl
import pyvacon.pricing.tools as pricing_tools

def project_model_param(pricing_data, model_ref, model_param, param_start, param_end, param_step):
    """
    project price by a certain model parameter (using tools.poject_model_param) and plot the result
    pricing_data: the pricing_data used for pricing
    model_ref: the model which will be projected (and which must be included in the pricing data so that it will be used for pricing)
    model_param: name of model parameter (as defined in the parameer description of the model) or just the number in the models parameter vector
    param_start: start value of model
    param_end: end value of model
    param_step: stepwidth between start and end values
    """
    prices, proj_x, index = pricing_tools.project_model_param(pricing_data, model_ref, model_param, param_start, param_end, param_step)
    x_label = model_ref.getParameterDescription()[index]
    plt.plot(proj_x, prices, '-x')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

def cashflow_profile(pricing_results):
    """
    plots the cashflow profiles for the pricing data
    pricing_results: pricing results returned by a price call
    """
    cashflows = pricing_results.getCashflowSlices()
    result = []
    for i in range(cashflows.cashflowSlices.size()):
        tmp = []
        for j in range(cashflows.cashflowSlices.size()):
            if j == i:
                for x in cashflows.cashflowSlices[j]:
                    tmp.append(x)
            else:
                for k in range(cashflows.cashflowSlices[j].size()):
                    tmp[k] += cashflows.cashflowSlices[j]
        result.append(tmp)
    return result
#plt.plot(np.mean