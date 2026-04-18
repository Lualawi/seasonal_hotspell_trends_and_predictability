# 2025_Admasu_White
This repository contains python codes used to perform analysis for the results presented in Admasu &amp; White, 2025, Investigating the subseasonal forecast skill of quasistationary waves in Northern Pacific Winter. The condes include: 
  - preprocess.py used to concatenate downloaded forecast database and compute model climatologies,
  - evaluation.ipynb used to restructure reanalysis data, calculate QSWs, compute evaluation metrics and plot evaluation results
  - linkages.ipynb used to compute correlations between variables of interest and QSW (or QSW forecast skill); perform composite analysis and plot results
  - FDR.ipynb used to apply FDR correction to statistical significance (p-values) for correlations and composite analysis performed
  - funs_for.py contains functions used to calculate QSWs for forecast data with multiple ensembles
  - funs_for_nonum contains functions used to calculate QSWs on restructured reanalysis data (no ensembles)
