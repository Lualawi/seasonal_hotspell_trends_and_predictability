#!/usr/bin/env python
#import packages
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
import cartopy.crs as ccrs
import time
import matplotlib as mpl
from scipy.stats import linregress

from scipy.cluster.vq import vq, kmeans, whiten

def kmns_heat(heat_smlnd_doy,n):
    heat_uslnd_stack=heat_smlnd_doy.t2m.stack(z={'latitude','longitude'})


    heat_uslnd_stack_nan= heat_uslnd_stack.dropna(dim='z')
    
    data=heat_uslnd_stack_nan.T
    num_cl=n
    whitened = whiten(data)
    centroids, mean_value =kmeans(whitened,num_cl)

    clusters, distances = vq(whitened, centroids)

    clusters_stack=xr.full_like(heat_uslnd_stack_nan.isel(dayofyear=0).copy(deep=True),np.nan)
    clusters_stack.values=clusters

    cluster_stack2=xr.full_like(heat_uslnd_stack.isel(dayofyear=0).copy(deep=True),np.nan)

    cluster_stack2.loc[cluster_stack2.z.isin(clusters_stack.z)]=clusters_stack
    cluster_labels=cluster_stack2.unstack()

    cluster_out=xr.full_like(heat_smlnd_doy.t2m.isel(dayofyear=0).copy(deep=True),np.nan)
    cluster_out.values=cluster_labels.values
    
    return cluster_out,centroids

def kmns_glob(heat_doy,n):
    heat_gl_stack=heat_doy.t2m#.stack(z={'latitude','longitude'})

    data=heat_gl_stack.T
    num_cl=n
    whitened = whiten(data)
    centroids, mean_value =kmeans(whitened,num_cl)

    clusters, distances = vq(whitened, centroids)

    clusters_stack=xr.zeros_like(heat_gl_stack.isel(dayofyear=0).copy(deep=True))
    clusters_stack.values=clusters

    

    return clusters_stack,centroids

def unstack_nan(dat, heat_stack, heat_stack_na):

    gl_un=heat_stack.t2m.isel(dayofyear=0).copy(deep=True)
    gl_nan=heat_stack_na.t2m.isel(dayofyear=0).copy(deep=True)

    gl_nan.values=dat
    gl_un.loc[gl_un.z.isin(gl_nan.z)]=gl_nan
    
    out_stack=gl_un.unstack()
    
    out_stack=out_stack.transpose('latitude', 'longitude')
    return out_stack

def trend(dat):
    slope_td=xr.full_like(dat.isel(time=0),np.nan)
    pval_td=xr.full_like(dat.isel(year=0),np.nan)
    for i in range(len(dat.latitude)):
        for j in range(len(dat.longitude)):
            hcur=dat.t2m.isel(latitude=i,longitude=j).values
            if ~np.isnan(hcur).all() and np.where(~np.isnan(hcur),1,0).sum()>1:
                trend=mk.original_test(hcur)
                slope_td[i,j]=trend[-2]
                pval_td[i,j]=trend[2]
            else:
                slope_td[i,j]=0
                pval_td[i,j]=1
    return slope_td,pval_td

def slopmann(dat):
    if ~np.isnan(dat).all() and np.where(~np.isnan(dat),1,0).sum()>1:
        trend=mk.original_test(dat)
        slope_td=trend[-2]
    else:
        slope_td=0

    return slope_td

def pvmann(dat):
    if ~np.isnan(dat).all() and np.where(~np.isnan(dat),1,0).sum()>1:
        trend=mk.original_test(dat)
        pv_td=trend[2]
    else:
        pv_td=1

    return pv_td
    
def clim_difplot(dat,ax):
    dat1=dat.sel(time=dat.time.dt.year.isin(np.arange(1979,2002))).mean(dim='time')
    dat2=dat.sel(time=dat.time.dt.year.isin(np.arange(2002,2024))).mean(dim='time')
    (dat2-dat1).plot(ax=ax,cmap='Reds',transform=ccrs.PlateCarree(),cbar_kwargs={'orientation':'horizontal'})
    
def revlat(dat):
    dat=dat.reindex(latitude=list(reversed(dat.latitude)))
    return dat

def rotlon(dat):
    dat.coords['longitude'] = (dat.coords['longitude']) % 360 #- 180
    dat=  dat.sortby(dat.longitude)
    return dat

def rotlon_180(dat):
    dat.coords['longitude'] = (dat.coords['longitude']+180) % 360- 180
    dat=  dat.sortby(dat.longitude)
    return dat

era_land=xr.open_dataset('eralandmask_regid.nc').rename({'lat':'latitude','lon':'longitude'})

def landmask(dat,land=rotlon_180(era_land)):
    dat2=dat.where(era_land.lsm.isel(time=0)>=0.5)
    return(dat2)

def sorttime(dat):
    dat=dat.sortby(dat.time)
    return dat

def sd_doy(dat):
    #takes data
    dat_out=xr.full_like(dat.groupby('time.dayofyear').mean(dim='time'),np.nan)
    for i in range(1,365):
        if i<15:
            cur_dat1=dat.sel(time=(dat.time.dt.dayofyear<i+15)|(dat.time.dt.dayofyear>365-15+i))
            print('1-',i,cur_dat1.time)
        elif i>350:
            cur_dat1=dat.sel(time=(dat.time.dt.dayofyear>i-15)|(dat.time.dt.dayofyear<(365-i)+15))
            print('2-',i,cur_dat1.time)
        else:
            cur_dat1=dat.sel(time=(dat.time.dt.dayofyear>i-15)&(dat.time.dt.dayofyear<i+15))
            print('3-',i,cur_dat1.time)
            
        cur_doy=cur_dat1.std('time')
        print(i)
        dat_out[i-1,]=cur_doy
    return dat_out
    
def rev_doy(dat,num):
        dat.coords['dayofyear']=xr.where(dat['dayofyear']>185,dat['dayofyear']-num,dat['dayofyear'])
        dat_out=  dat.sortby(dat.dayofyear)
        return dat_out
    
def rerev_doy(dat,num):
        dat.coords['dayofyear']=xr.where(dat['dayofyear']<=0,dat['dayofyear']+num,dat['dayofyear'])
        dat_out=  dat.sortby(dat.dayofyear)
        return dat_out
    
def clim_smoother(dat_in,window_size):

    dat_out=dat_in.rolling(dayofyear=window_size,center=True).mean()
    #instead of creating cases reorient dayofyear to use .rolling
    dat2=dat_in.copy(deep=True)
    
    if dat_out.dayofyear[-1]==366:
        dat_o1=  rev_doy(dat2, 366)
        dat_o1_rol=dat_o1.rolling(dayofyear=window_size,center=True).mean()
        
        dat3=dat_o1_rol.copy(deep=True)
        dat_o2=rerev_doy(dat3, 366)
    else:
        dat_o1=  rev_doy(dat2,365)
        dat_o1_rol=dat_o1.rolling(dayofyear=window_size,center=True).mean()
        
        dat3=dat_o1_rol.copy(deep=True)
        dat_o2=rerev_doy(dat3,365)

    dat_out[0:window_size,]=dat_o2[0:window_size,]
    dat_out[365-window_size:366,]=dat_o2[365-window_size:366,]
    return dat_out

def cutmidlat(dat):

    datout=dat.sel(latitude=slice(30,80))

    return datout

def manntrend(dat):
    dat=np.asarray(dat)
    if not np.isnan(dat).all() and np.count_nonzero(~np.isnan(dat)) > 1:
        trend=mk.original_test(dat)
        slope=trend[-2]
        pval=trend[2]
#         slope_td[i,j]=trend[-2]
#         pval_td[i,j]=trend[2]
    else:
        slope=np.nan
        pval=np.nan
        #         slope_td[i,j]=0
#         pval_td[i,j]=1
    return slope,pval