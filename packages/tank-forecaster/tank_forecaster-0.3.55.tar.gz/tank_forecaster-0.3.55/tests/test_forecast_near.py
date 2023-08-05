import numpy as np
import pandas as pd

from tank_forecaster import forecaster
from tank_forecaster.decomp import generic_hh_seasonality


def is_a_valid_forecast_dataframe(df):
    return (
        type(df) is pd.core.frame.DataFrame
        and len(df) == 144
        and "ds" in df
        and "yhat" in df
        and type(df.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
        and type(df.yhat.iloc[-1]) is np.float64
    )


def test_near_approx_returns_a_valid_dataframe():
    x = forecaster.forecast_near_approx(
        daily_lift_est=0, hh_seasonality=generic_hh_seasonality
    )
    assert is_a_valid_forecast_dataframe(x)


def test_near_approx_returns_none():
    assert (
        forecaster.forecast_near_approx(daily_lift_est=None, hh_seasonality=None)
        is None
    )


def test_near_returns_none():
    assert forecaster.forecast_near(None) is None


def test_near_full_data_returns_a_valid_dataframe(tank_full_data):
    x = forecaster.forecast_near(tank_history=tank_full_data)
    assert is_a_valid_forecast_dataframe(x)


def test_near_approx_start_date():
    x = forecaster.forecast_near_approx(
        daily_lift_est=0, hh_seasonality=generic_hh_seasonality, start_time="2020-01-01"
    )
    assert is_a_valid_forecast_dataframe(x)


def test_near_start_date(tank_full_data):
    x = forecaster.forecast_near(tank_history=tank_full_data, start_time="2020-01-01")
    assert is_a_valid_forecast_dataframe(x)
    assert str(x.ds.iloc[0]) == "2020-01-01 00:00:00"
