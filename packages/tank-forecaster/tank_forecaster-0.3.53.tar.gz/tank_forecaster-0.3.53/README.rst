===============
Tank Forecaster
===============

Small package for generating forecasts of fuel tank demand.


Features
--------

- tank_forecaster.validation
    - clean and format sales data
    - clean and format tank reading data
    - use sales data to impute missing values in tank readings
- tank_forecaster.decompositions
    - create seasonal decomposition curves (yearly / monthly / weekly)
    - generate generic decomposition curves for instances of no data
- tank_forecaster.forecaster
    - create short term forecasts with generalized additive models (fbprophet)
    - create long term forecasts with ARIMA type models
- tank_forecaster.events
    - define holidays and special events that effect fuel demand


Credits
-------

This package was created with Cookiecutter
