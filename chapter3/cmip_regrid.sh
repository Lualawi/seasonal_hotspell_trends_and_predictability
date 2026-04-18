#!/bin/bash

declare -a model=('ACCESS-CM2' 'AWI-CM-1-1-MR' 'BCC-CSM2-MR'  'CanESM5' 'CESM2' 'CMCC-ESM2' 'CNRM-ESM2-1' 'EC-Earth3-CC' 'GFDL-ESM4' 'IITM-ESM' 'INM-CM5-0' 'KIOST-ESM' 'MIROC6' 'MPI-ESM1-2-LR' 'MRI-ESM2-0' 'NESM3' 'NorESM2-MM' 'TaiESM1' 'CESM2-WACCM'  'CMCC-CM2-SR5'  'CNRM-CM6-1' 'INM-CM4-8' 'IPSL-CM6A-LR'  'MIROC-ES2L' 'CNRM-CM6-1-HR' )

for i in "${model[@]}"
do
  cdo remapcon,grid25 tas_day_"$i"_hist_ssp_full.nc tas_day_"$i"_hist_ssp_regridcon.nc
  cdo remapcon,grid25 tas_day_"$i"_fut_ssp5_full.nc tas_day_"$i"_fut_ssp5_regridcon.nc
done

