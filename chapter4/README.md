This repository contains Python code used to perform analysis for the results presented in Chapter 4: Hot spell trend correction across seasons in Canada: Downscaling, bias correction, and emergent constraints. The contents include:
- functions.py: contains functions used to compute several analyses, including trends and other pre-processing steps like slicing temporal and spatial extents. 
- compute_hotspells.ipynb: computes hot spell metrics on each dataset and saves for analysis.
- compute_trends_and_plots.ipynb: computes seasonal trends in hot spell days, mean temperature across datasets, and plots associated figures.
- surface_trends.ipynb: computes seasonal trends in flux and surface variables.
- emergent_constraints: performs emergent constraint analysis based on trends in temperature, flux, and surface variables, including final correction and plots.
- Fullfield_correlations.ipynb: performs emergent constraint correlations based on seasonal climatologies in temperature, flux, and surface variables
- mlr_correction.ipynb: performs multivariate linear regression-based correction using trends in temperature, albedo, and soil moisture for emergent constraints on hot spell changes.
