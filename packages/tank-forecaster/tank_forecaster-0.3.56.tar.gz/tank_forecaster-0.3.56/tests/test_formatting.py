import numpy as np
import pandas as pd

from tank_forecaster import validation


def is_validated_data(x):
    return (
        type(x) is pd.core.frame.DataFrame
        and len(x["ds"]) != 0
        and len(x["y"]) != 0
        and type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
        and type(x.y.iloc[-1]) is np.float64
    )


def test_format_tank_none_returns_none():
    x = validation.format_tank(None)
    assert x is None


def test_format_tank_empty_returns_none():
    x = validation.format_tank([])
    assert x is None


def test_format_tank_deletes_first_and_list(tank_two_input):
    x = validation.format_tank(tank_two_input)
    assert len(x) == 0


def test_format_tank_returns_validated_data(tank_little_input):
    x = validation.format_tank(tank_little_input)
    assert is_validated_data(x)


def test_format_sales_no_data_returns_none():
    x = validation.format_sales(None)
    assert x is None


def test_format_sales_empty_list_returns_none():
    x = validation.format_sales([])
    assert x is None


def test_format_sales_proper(sales_little_input):
    x = validation.format_sales(sales_little_input)
    assert is_validated_data(x)
