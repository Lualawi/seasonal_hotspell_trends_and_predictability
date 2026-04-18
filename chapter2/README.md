This repository contains Python code used to perform analysis for the results presented in Chapter 2: Subseasonal Prediction Skill of Winter Quasi-Stationary Waves in the Northern Hemisphere. The contents include: 
  - preprocess.py used to concatenate the downloaded forecast database and compute model climatologies,
  - evaluation.ipynb used to restructure reanalysis data, calculate QSWs, compute evaluation metrics, and plot evaluation results
  - linkages.ipynb used to compute correlations between variables of interest and QSW (or QSW forecast skill); perform composite analysis and plot results
  - FDR.ipynb used to apply FDR correction to statistical significance (p-values) for correlations and composite analysis performed
  - funs_for.py contains functions used to calculate QSWs for forecast data with multiple ensembles
  - funs_for_nonum contains functions used to calculate QSWs on restructured reanalysis data (no ensembles)
