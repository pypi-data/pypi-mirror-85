from datetime import datetime, timedelta
from typing import List

import numpy as np
import pandas as pd
from fbprophet import Prophet
from sparkles import trunc_date
from sparkles.fbprophet_hacks import suppress_stdout_stderr


def forecast_near(
    tank_history: pd.DataFrame = None,
    start_time=None,
    forecast_freq: str = None,
    forecast_length: int = None,
):

    if tank_history is None or len(tank_history) < 432:
        return

    if start_time is None:
        now = datetime.now()
        now_hh = now - (now - datetime.min) % timedelta(minutes=30)
        start_time = now_hh

    if forecast_freq is None:
        forecast_freq = "30min"

    if forecast_length is None:
        forecast_length = 144

    future = pd.date_range(
        start=start_time, freq=forecast_freq, periods=forecast_length
    )
    future = pd.DataFrame(future)
    future.rename(columns={0: "ds"}, inplace=True)

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
    )
    with suppress_stdout_stderr():
        m.fit(tank_history)
    forecast = m.predict(future)

    output = forecast.loc[:, ["ds", "yhat_lower", "yhat_upper", "yhat"]]
    output.rename(columns={"yhat_lower": "lower", "yhat_upper": "upper"}, inplace=True)

    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    return output


def forecast_near_approx(
    daily_lift_est: int,
    hh_seasonality: List,
    start_time=None,
    forecast_freq: str = None,
    forecast_length: int = None,
):
    if daily_lift_est is None:
        return None

    if hh_seasonality is None:
        return None

    if start_time is None:
        now = datetime.now()
        now_hh = now - (now - datetime.min) % timedelta(minutes=30)
        start_time = now_hh

    if forecast_freq is None:
        forecast_freq = "30min"

    if forecast_length is None:
        forecast_length = 144

    predictions = pd.DataFrame(columns=["ds", "ts", "base", "estimate"])
    predictions["ds"] = pd.date_range(
        pd.to_datetime(start_time), freq=forecast_freq, periods=forecast_length
    )

    predictions["ts"] = predictions.ds.dt.time
    predictions["base"] = daily_lift_est * (1 / 48)

    hh_multiplier = pd.DataFrame(columns=["ts", "value"])
    hh_multiplier["ts"] = pd.date_range("00:00", "23:30", freq="30min")
    hh_multiplier["ts"] = hh_multiplier.ts.dt.time
    hh_multiplier["value"] = hh_seasonality

    merged = pd.merge(left=predictions, right=hh_multiplier)

    merged["estimate"] = merged["base"] * merged["value"]

    output = merged[["ds", "estimate"]].copy()
    output.rename(columns={"estimate": "yhat"}, inplace=True)

    output["lower"] = output["yhat"] - 2 * output["yhat"].std()
    output["upper"] = output["yhat"] + 2 * output["yhat"].std()

    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    result = output.sort_values(by="ds")

    return result


def forecast_far(
    daily_lift_est: int,
    weekly_seasonality: List,
    yearly_seasonality: List = None,
    start_date=None,
    forecast_length: int = None,
):
    if daily_lift_est is None:
        return None

    if yearly_seasonality is None:
        yearly_seasonality = [1] * 53

    if weekly_seasonality is None:
        return None

    if start_date is None:
        start_date = trunc_date(datetime.now())

    if forecast_length is None:
        forecast_length = 90

    yearly_seasonality = pd.Series(yearly_seasonality)
    weekly_seasonality = pd.Series(weekly_seasonality)

    predictions = pd.DataFrame(columns=["woy", "dow", "base", "weekly", "daily"])
    predictions["woy"] = np.repeat(range(1, 54), 7)  # 52.14 'week of year' -> 53
    predictions["dow"] = [0, 1, 2, 3, 4, 5, 6] * 53  # 7 'day of week' each week of year
    predictions["base"] = daily_lift_est

    weekly = np.repeat(predictions.base.iloc[1] * 7 * yearly_seasonality, 7)
    weekly.index = range(0, 371)
    predictions["weekly"] = weekly

    weekly_seas_repeated = pd.concat([weekly_seasonality] * 53, ignore_index=True)
    predictions["daily"] = predictions.weekly * (1 / 7) * weekly_seas_repeated

    future = pd.date_range(start=start_date, freq="1D", periods=forecast_length)
    future = pd.DataFrame(future)
    future.rename(columns={0: "ds"}, inplace=True)

    future["dow"] = future.ds.dt.weekday  # future.ds.dt.dayofweek
    future["woy"] = future.ds.dt.week

    output = pd.merge(
        future, predictions, left_on=["woy", "dow"], right_on=["woy", "dow"]
    )

    output = output[["ds", "daily"]]
    output.rename(columns={"daily": "yhat"}, inplace=True)

    output["lower"] = output["yhat"] - 2 * output["yhat"].std()
    output["upper"] = output["yhat"] + 2 * output["yhat"].std()

    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    return output


if __name__ == "__main__":
    pass
