#!/usr/bin/env python
import numpy as np
import xarray as xr
from scipy import stats,signal
import scipy.fftpack as fftpack
from scipy.interpolate import interp1d,CubicSpline

rearth= 6.37122e6    #! radius of earth ~ m

def fourier_Hilbert_3D_for(indata,nlons,peak_freq=0,ndegs=360):
    
    X_fft = fftpack.fft(indata)
    f_s = nlons
    freqs = fftpack.fftfreq(nlons) * f_s
    t = np.linspace(0, ndegs, f_s, endpoint=False)

    filt_fft = X_fft.copy()
    if peak_freq != 0:
        filt_fft[:,:,:,np.abs(freqs) > peak_freq] = 0
    
    # Hilbert transform: set negatives = 0
    filt_fft[:,:,:,freqs<0] = 0
    filtered_sig = fftpack.ifft(filt_fft)
    return(filtered_sig,t)




def fourier_Tukey_hilow_3D_for(indata,nlons,s1,s2,ndegs=360):
    try:
        ntimes = len(indata.times)
    except AttributeError:
        ntimes = 1
    
    X_fft = fftpack.fft(indata)

    f_s = nlons
    freqs = fftpack.fftfreq(nlons) * f_s
    t = np.linspace(0, ndegs, f_s, endpoint=False)

    filt_fft = X_fft.copy()
    filt_fft[:,:,:,np.abs(freqs) > s2] = 0
    filt_fft[:,:,:,np.abs(freqs) < s1] = 0
    filtered_sig = fftpack.ifft(filt_fft)

    # create Tukey window to smooth the wavenumbers removed (so no exact cutoff at any particular wavenumber, 
    # which will change at different latitudes)
    # Window is 2 wavenumbers more than the peak, but multiplied by 2 because the Tukey window is symmetric
    limit1 = np.amax([0,s1 - 1.5])
    limit2 = s2 + 1.5

    diff = limit2-limit1
    M = 100

    tukeymax = int(np.amax([limit1,limit2])) + 10

    tukeydata = signal.tukey(M, alpha=0.3, sym=True)

    # Add zeros at front and back of window for interpolation
    tukeydata = np.insert(tukeydata,0,np.zeros(40))
    tukeydata = np.append(tukeydata,np.zeros(40))

    # wavenumber values for Tukey window with added zeros
    xs = np.arange(limit1-40.0*diff/M,limit2+ 39.999*diff/M,diff/M)

    # model tukey window with cubic splines
    wn_cs = np.linspace(0,tukeymax-1,tukeymax)
    CS = CubicSpline(xs,tukeydata)

    tukeyWin = CS(wn_cs)
    turfilt_fft = X_fft.copy()
    n = len(turfilt_fft[0,0,0,:])
    turfilt_fft[:,:,:,0:tukeymax] = turfilt_fft[:,:,:,0:tukeymax]*tukeyWin
    turfilt_fft[:,:,:,tukeymax:n-tukeymax] = 0
    turfilt_fft[:,:,:,n-tukeymax:n] = turfilt_fft[:,:,:,n-tukeymax:n]*tukeyWin[::-1]
    tur_filtered_sig = fftpack.ifft(turfilt_fft)

    return(tur_filtered_sig,filtered_sig,t)


def calc_wavepacket_3D_for(datain,len_min,len_max):
    # Subtract zonal mean
    test_data = datain - datain.mean(dim='longitude')
    lats = test_data.latitude
    lons = test_data.longitude
    times = test_data.time

#     wavepacket = xr.DataArray(np.zeros([len(times),len(lats),len(lons)]),
#                               coords={'time':times,'latitude':lats,'longitude':lons},
#                               dims = ('time','latitude','longitude'))
    wavepacket = xr.zeros_like(datain)

    templats = lats.sel(latitude=slice(85,20))
    ilatstart = np.where(lats == templats[0])[0]
    ilatend = np.where(lats == templats[-1])[0]

    for latsel in np.arange(ilatstart,ilatend+1):
        # Find wavenumbers for km values at given latitude
        # include 0.001 factor to convert rearth from m to km
        rearth=6.37122e6    #radius of earth ~ m
        circum = (2.0 * np.pi * (0.001 * rearth * np.cos(np.deg2rad(lats.isel(latitude=latsel)))))
        s2 = (circum/len_min).values
        s1 = (circum/len_max).values

        indata = test_data.isel(latitude=latsel)
        inlat = indata.latitude.values

        # Tukey transform the data
        nlons = len(indata.longitude)

        indata2=indata.values
        tukey_transform, std_transform,t = fourier_Tukey_hilow_3D_for(indata2,nlons,s1,s2,ndegs=360)
        # Now hilbert transfrom (For now, ignoring the semi-geostrophic filter)
        
        hilbert_transform,t = fourier_Hilbert_3D_for(tukey_transform,nlons)
        print(np.abs(hilbert_transform))
        print(np.shape(hilbert_transform))
        #print(np.shape(wavepacket[:,latsel,:]))
        wavepacket[:,:,:,latsel,:] = 2.0 *np.abs(hilbert_transform)
        
    return wavepacket