#!/usr/bin/env python
import xarray as xr
import cfgrib
import pandas as pd
from datetime import timedelta

import numpy as np
from scipy.signal import butter, filtfilt
#import xrscipy.other.signal as dsp
import xarray as xr

#Low pass filter
# Apply the filter to the data
def apply_low_pass_filter(data, cutoff = 1/15, nyquist=0.5, order=8):
    #cutoff = 1/15  in days^-1,  # Order of the filter = 2
    # Nyquist frequency,: is half of the sampling frequency (1 day^-1)    
    # Calculate the normalized cutoff frequency
    normalized_cutoff = cutoff / nyquist
    # Butterworth filter coefficients
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data


#concat ctl with ptbd
a = pd.to_datetime('2020-11-03')
dates = []
alldat = []
for i in range (34):
    print (a)
    da = a.strftime('%d')
    mo = a.strftime('%m')
    dat1 = xr.open_dataset('forecast_gribs_v2016full/v300_cf_'+str(mo)+'-'+str(da)+'.grib',engine = 'cfgrib')
    dat2 = xr.open_dataset('forecast_gribs_v2016full/v300_pf_'+str(mo)+'-'+str(da)+'.grib',engine = 'cfgrib')
    dat4 = xr.concat([dat1,dat2],dim = 'number')
    

    dat4.coords['longitude'] = (dat4.coords['longitude'] + 180) % 360 - 180
    dat4 = dat4.sortby(dat4.longitude)
    alldat.append(dat4)
    name = 'forecast_nc2/v300_'+str(mo)+'_'+str(da)+'.nc'
    dat4.to_netcdf(name)
    dates.append(a)
    if i%2==0:
        a=a+timedelta(4)
    else:
        a=a+timedelta(3)

middat = alldat[2:-2]
datesmid = dates[2:-2]
val = [1,2,3,4,5]
for i in range(len(alldat)):
    
    dest = alldat[i].copy()

    #dest_fin = dest.rolling(step=15, center=True).mean() #Roll for QSW befo mean over time
    dest_fin = xr.apply_ufunc(apply_low_pass_filter,dest,input_core_dims=[['step']],output_core_dims=[['step']])
    dest_fin = dest_fin.mean(dim = 'number')
    dest_fin = dest_fin.mean(dim = "time")

    da = dates[i].strftime('%d')
    mo = dates[i].strftime('%m')
    name = 'forecast_nc2/v300_'+str(mo)+'_'+str(da)+'_clim.nc'
    dest_fin.to_netcdf(name)


#avg across time perturbed
