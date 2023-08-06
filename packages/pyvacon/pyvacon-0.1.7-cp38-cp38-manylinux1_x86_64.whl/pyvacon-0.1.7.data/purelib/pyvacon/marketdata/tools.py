# -*- coding: utf-8 -*-
"""


Spyder Editor

This is a temporary script file.
"""
import datetime as _dt
import pyvacon.tools.converter as _converter
import pandas as _pd
    
class VolatilityStatistics:

    @staticmethod
    def _get_expiry(vol, expiry):
        if isinstance(expiry, int):
            refdate = _converter.create_datetime(vol.getRefDate())
            return refdate + _dt.timedelta(days=expiry)
        else:
            return expiry
            
    class Forward:
        def __init__(self,  expiry):
            """
            initialize object to compute a forward from the volatilitys forward curve
        
            
            expiry (int or _dt.datetime): Either number of days from volatilities reference date or fixed expiry as python _dt.datetime
            """
            self.expiry = expiry
            self.name = "FWD_"+str(expiry)            

        def compute(self, vol):
            fwd = vol.getForwardCurve()
            forward = fwd.value(vol.getRefDate(), VolatilityStatistics._get_expiry(vol, self.expiry))
            return forward
    
    class ImpliedVol:
        def __init__(self,  x_strike, expiry):
            """
            initialize object to compute a simple implied vol
        
            name: identifier
            x_strike: x-strike at which skew is computed
            expiry: number of days from volatilities reference date at which implied volatility is computed
            """
            self.name = "IV_"+str(x_strike)+'_' + str(expiry) 
            self.xstrike = x_strike
            self.expiry = expiry
       
        def compute(self, vol):
            impl = vol.calcImpliedVol(vol.getRefDate(), VolatilityStatistics._get_expiry(vol, self.expiry), self.xstrike)
            return impl
        

    class Skew:
        def __init__(self, x_strike, expiry, delta = 0.01):
            """
            initialize object to compute a skew
        
            name: identifier
            x_strike: x-strike at which skew is computed
            expiry: number of days from volatilities reference date at which skew is computed
            delta: delta used within finite difference formula to compute skew (first derivative)
            """
            self.name = 'SKEW_' + str(x_strike) + '_'+ str(expiry)
            self.xstrike = x_strike
            self.expiry = expiry
            self.delta = delta
    
        def compute(self, vol):
            expiry = VolatilityStatistics._get_expiry(vol, self.expiry)
            vol_up = vol.calcImpliedVol(vol.getRefDate(), expiry, self.xstrike + self.delta)
            vol_down = vol.calcImpliedVol(vol.getRefDate(), expiry, self.xstrike - self.delta)
            return (vol_up-vol_down) / (2.0*self.delta)
        
        
    class Smile:
        def __init__(self, x_strike, expiry, delta = 0.01):
            """
            initialize object to compute a smile
        
            name: identifier
            x_strike: x-strike at which skew is computed
            expiry: number of days from volatilities reference date at which smile is computed
            delta: delta used within finite difference formula to compute smile (second derivative)
            """
            self.name = 'SMILE_' + str(x_strike) + '_'+ str(expiry)
            self.xstrike = x_strike
            self.expiry = expiry
            self.delta = delta
    
        def compute(self, vol):
            expiry = VolatilityStatistics._get_expiry(vol, self.expiry)
            vol_up = vol.calcImpliedVol(vol.getRefDate(), expiry, self.xstrike + self.delta)
            vol_mid = vol.calcImpliedVol(vol.getRefDate(), expiry, self.xstrike)
            vol_down = vol.calcImpliedVol(vol.getRefDate(), expiry, self.xstrike - self.delta)
            return (vol_up -2.0*vol_mid + vol_down) / (self.delta*self.delta)
        
    @staticmethod
    def get_volatility_series(vols, statistics):
        """Return pandas DataFrame with the respective values
           
        """
        result = {}
        for stat in statistics:
            result[stat.name] = []
        
        calib_date = []
        for vol in vols:
            calib_date.append(_converter.create_datetime(vol.getCalibrationDate()))
            for stat in statistics:
                result[stat.name].append(stat.compute(vol))
        result['calib_date'] = calib_date
        result = _pd.DataFrame.from_dict(result)
        result.set_index('calib_date', inplace = True)
        return result