from tank_forecaster import decomp


def seas_are_of_correct_length(x):
    return len(x[0]) == 53 and len(x[1]) == 7


def test_decompose_sales_none_returns_none():
    x = decomp.decompose_sales(None)
    assert seas_are_of_correct_length(x)


def test_decompose_sales_little_data_returns_lists(sales_little_data):
    x = decomp.decompose_sales(sales_little_data)
    assert seas_are_of_correct_length(x)


def test_decompose_sales_week_data_returns_correct_len(sales_week_data):
    x = decomp.decompose_sales(sales_week_data)
    assert seas_are_of_correct_length(x)


def test_decompose_sales_three_week_data_returns_correct_len(sales_three_week_data):
    x = decomp.decompose_sales(sales_three_week_data)
    assert seas_are_of_correct_length(x)
