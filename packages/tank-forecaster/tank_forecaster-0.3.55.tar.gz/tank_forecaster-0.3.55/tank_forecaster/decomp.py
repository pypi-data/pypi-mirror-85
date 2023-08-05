import numpy as np
import pandas as pd
from fbprophet import Prophet
from sparkles.fbprophet_hacks import suppress_stdout_stderr

# declare variables for testing
store = "KT220"
tank = "7"
fc_url = "https://fc.bbdev.host3.capspire.com"


def decompose_sales(sales_data: pd.DataFrame):

    if sales_data is None or len(sales_data) < 7:
        return pd.Series([1] * 53), pd.Series([1] * 7)

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        seasonality_mode="multiplicative",
    )
    with suppress_stdout_stderr():
        m.fit(sales_data)

    future = m.make_future_dataframe(periods=1, freq="1D")
    forecast = m.predict(future)
    forecast_reduced = forecast.loc[:, ["ds", "yearly", "weekly"]]
    forecast_reduced["dow"] = forecast_reduced.ds.dt.weekday
    forecast_reduced["doy"] = forecast_reduced.ds.dt.dayofyear
    forecast_reduced["woy"] = forecast_reduced.ds.dt.week

    weekly_seasonality = forecast_reduced.groupby("dow")["weekly"].mean() + 1

    if len(weekly_seasonality) < 7:
        return pd.Series([1] * 53), pd.Series([1] * 7)

    if len(sales_data) < 350:
        return pd.Series([1] * 53), weekly_seasonality

    forecast_reduced = forecast_reduced.iloc[-366:]
    forecast_reduced.sort_values(by=["woy", "dow"], inplace=True)
    year_trend = forecast_reduced.groupby("woy").mean()
    year_trend = year_trend["yearly"] + 1

    yearly_seasonality = ensure_53_weeks(year_trend)

    if len(weekly_seasonality) == 7 and len(yearly_seasonality) == 53:
        return yearly_seasonality, weekly_seasonality

    return pd.Series([1] * 53), pd.Series([1] * 7)


def ensure_53_weeks(initial: pd.DataFrame) -> pd.DataFrame:
    """
    takes a shorter dataframe and ensures at least 53 rows by wrapping the first rows onto the end
    """
    extra_weeks_needed = 53 - len(initial)
    if extra_weeks_needed > 0:
        ret = pd.concat([initial, initial[:extra_weeks_needed]], ignore_index=True)
    else:
        ret = initial.copy()
    return ret


def decompose_seasonality(tank_history: pd.DataFrame):
    if tank_history is None or len(tank_history) < 48:
        return main_hh_seas, main_dow_seas

    m = Prophet(
        changepoint_prior_scale=0.05,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        seasonality_mode="multiplicative",
    )

    with suppress_stdout_stderr():
        m.fit(tank_history)

    future = m.make_future_dataframe(periods=1, freq="30min")
    forecast = m.predict(future)

    forecast_reduced = forecast.loc[:, ["ds", "daily", "weekly"]]
    forecast_reduced["time"] = forecast_reduced.ds.dt.time
    forecast_reduced["dow"] = forecast_reduced.ds.dt.weekday
    forecast_reduced.drop(columns="ds", inplace=True)

    day_seas = forecast_reduced.groupby("time").daily.mean()
    week_seas = forecast_reduced.groupby("dow").weekly.mean()

    day_seas.sort_index(inplace=True)
    week_seas.sort_index(inplace=True)

    if len(day_seas) != 48 and len(week_seas) != 7:
        return main_hh_seas, main_dow_seas

    if len(day_seas) != 48 or len(week_seas) != 7:
        if len(week_seas) != 7:
            return list(day_seas + 1), main_dow_seas
        if len(day_seas) != 48:
            return main_hh_seas, list(week_seas + 1)

    return list(day_seas + 1), list(week_seas + 1)


main_hh_seas = [
    1.17,
    0.94,
    0.74,
    0.57,
    0.45,
    0.37,
    0.32,
    0.30,
    0.28,
    0.25,
    0.21,
    0.16,
    0.11,
    0.05,
    0.02,
    0.01,
    0.03,
    0.08,
    0.17,
    0.28,
    0.41,
    0.54,
    0.68,
    0.81,
    0.92,
    1.04,
    1.15,
    1.25,
    1.35,
    1.44,
    1.51,
    1.57,
    1.62,
    1.65,
    1.67,
    1.69,
    1.72,
    1.75,
    1.80,
    1.86,
    1.93,
    1.98,
    2.00,
    1.98,
    1.91,
    1.79,
    1.61,
    1.40,
]

truck_hh_seas = [
    0.78,
    0.64,
    0.51,
    0.42,
    0.35,
    0.31,
    0.28,
    0.28,
    0.27,
    0.28,
    0.26,
    0.23,
    0.21,
    0.20,
    0.19,
    0.22,
    0.27,
    0.37,
    0.50,
    0.66,
    0.85,
    1.04,
    1.18,
    1.33,
    1.45,
    1.53,
    1.55,
    1.56,
    1.56,
    1.55,
    1.52,
    1.52,
    1.53,
    1.52,
    1.54,
    1.56,
    1.58,
    1.59,
    1.59,
    1.57,
    1.54,
    1.51,
    1.47,
    1.37,
    1.31,
    1.19,
    1.06,
    0.92,
]

main_dow_seas = [1.04, 0.98, 0.98, 1, 1.08, 1.01, 0.9]
truck_dow_seas = [1.11, 1.12, 1.09, 1.06, 1.03, 0.75, 0.72]


def get_tank_readings():
    import requests

    headers = {
        "accept": "application/json",
    }

    params = (
        ("start_date", "2020-10-01 00:00:00"),
        ("end_date", "2020-10-18 00:00:00"),
        ("store_number", "103"),
        ("tank_id", "1"),
        ("system_psk", "7636d15a00204b62c56da0d2311ce69ae52ef28cc5940545"),
    )

    response = requests.post(
        "https://ktdev.bb.gravitate.energy/service/ims/tank_inventory/readings",
        headers=headers,
        params=params,
    )
    return response.json()


if __name__ == "__main__":
    from tank_forecaster.validation import format_tank

    tr = get_tank_readings()
    val = format_tank(tr)
    day_seas, week_seas = decompose_seasonality(val)
    print(day_seas)
    print(week_seas)
