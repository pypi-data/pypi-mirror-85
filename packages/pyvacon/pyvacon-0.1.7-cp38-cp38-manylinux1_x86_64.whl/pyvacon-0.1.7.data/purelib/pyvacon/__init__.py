#import pyvacon.analytics as analytics
import pyvacon.version as version
import pyvacon.instruments as instruments
import pyvacon.pricing as pricing
import pyvacon.utils as utils
import pyvacon.analytics as analytics
import pyvacon.marketdata as marketdata

if version.is_beta:
    import warnings
    warnings.warn('Imported pyvacon is just beta version.')
