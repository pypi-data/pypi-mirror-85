import numpy as np
import pandas as pd

from tank_forecaster import forecaster
from tank_forecaster.decomp import (generic_weekly_seasonality,
                                    generic_yearly_seasonality)


def is_a_valid_forecast_dataframe(df):
    return (
        type(df) is pd.core.frame.DataFrame
        and len(df) == 90
        and "ds" in df
        and "yhat" in df
        and type(df.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
        and type(df.yhat.iloc[-1]) is np.float64
    )


def test_far_returns_a_valid_dataframe():
    x = forecaster.forecast_far(
        daily_lift_est=5000,
        yearly_seasonality=generic_yearly_seasonality,
        weekly_seasonality=generic_weekly_seasonality,
    )
    assert is_a_valid_forecast_dataframe(x)


def test_far_start_date_works():
    x = forecaster.forecast_far(
        daily_lift_est=5000,
        yearly_seasonality=generic_yearly_seasonality,
        weekly_seasonality=generic_weekly_seasonality,
        start_date="2020-01-01",
    )
    assert is_a_valid_forecast_dataframe(x)
    assert str(x.ds.iloc[0]) == "2020-01-01 00:00:00"
    assert str(x.ds.iloc[-1]) == "2020-03-30 00:00:00"


if __name__ == "__main__":
    pass
