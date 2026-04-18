This repository contains Python code used to perform analysis for the results presented in Chapter 3: Northern Hemisphere Spring Hot Spells Increasing Faster Than Projected: An Assessment of Hot Spell Trend Seasonality. The codes include:
- cmip_regrid.sh: utilizes Climate Data Operators (CDO) to regrid CMIP6, ERA5, and Berkeley Earth datasets to a common grid size.
- functions.py: contains functions used to compute several analyses, including computing the hot spell metric, trends, and other pre-processing steps like slicing temporal and spatial extents. 
- compute_hotspells.ipynb: computes hot spell metrics on each dataset and saves for analysis.
- seasonal_trends.ipynb: computes seasonal trends in hot spell days, mean temperature, and 10-day temperature variability.
- doy_trends: computes trends for each day-of-year in hot spells and mean temperature.
- clusters_berkeley.ipynb: identifies clusters based on Berkeley hot spell trends across day-of-year and maps the equivalent temperature trends and 10-day temperature variability across day-of-year.
- clusters_era.ipynb: same as "clusters_berkeley.ipynb" but based on ERA5 hot spell trends across day-of-year.
- clusters_cmip6.ipynb: same as "clusters_berkeley.ipynb" but based on CMIP6 model mean hot spell trends across day-of-year.
- final_plots.ipynb: generates final figures included in the article.
