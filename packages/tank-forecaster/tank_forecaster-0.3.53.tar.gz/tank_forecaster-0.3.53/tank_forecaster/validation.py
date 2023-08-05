from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd


def format_tank(readings: List[Dict], freq: str = "30min") -> pd.DataFrame or None:

    if readings is None:
        return None

    validated = []

    for i in range(len(readings)):
        if "read_time" in readings[i] and "volume" in readings[i]:
            validated.append(readings[i])

    if not validated:
        return None

    validated = sorted(validated, key=lambda x: x["read_time"])
    validated = [d for d in validated if d["volume"]]

    df = pd.DataFrame(validated)
    df.read_time = pd.to_datetime(df.read_time)
    df["y"] = df.volume.diff() * -1
    df = df[["read_time", "y"]].rename(columns={"read_time": "ds"})
    df = df[df.y < 800].copy()
    df.y = df.y.clip(lower=0)
    df = df.set_index("ds").groupby(pd.Grouper(freq=freq)).sum()

    if len(df) == 2:
        return None

    df.reset_index(level=0, inplace=True)
    output = df.iloc[1:-1]

    return output


def format_sales(sales_input: List[Dict]) -> pd.DataFrame or None:

    if sales_input == [] or sales_input is None:
        return None

    sales_input = sorted(sales_input, key=lambda x: x["date"])
    sales_df = pd.DataFrame(sales_input)
    df = sales_df[["date", "sales"]]

    df2 = df.copy()
    df2["sales"] = df["sales"].clip(
        lower=df.sales.quantile(0.015), upper=df.sales.quantile(0.995)
    )

    df3 = df2.rename(columns={"date": "ds", "sales": "y"})

    result = df3.copy()
    result["ds"] = df3.loc[:, "ds"].astype("datetime64[ns]")

    return result


def gen_past(df: pd.DataFrame, freq: str = "30min", periods: int = 432) -> pd.DataFrame:

    if len(df) == 0 or df is None:
        now = datetime.now()
        end_0 = now - (now - datetime.min) % timedelta(minutes=30)

    else:
        end_0 = df.iloc[-1, 0]

    past = pd.date_range(end=end_0, freq=freq, periods=periods)
    past = pd.DataFrame(past)
    past.rename(columns={0: "ds"}, inplace=True)
    past["ds"] = pd.to_datetime(past["ds"], format="%Y-%m-%d")

    return past


if __name__ == "__main__":
    pass
