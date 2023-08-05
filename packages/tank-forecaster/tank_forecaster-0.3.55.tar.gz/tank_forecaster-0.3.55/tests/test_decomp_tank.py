from tank_forecaster import decomp


def test_decomp_tank_none_returns_correct_len(tank_full_data):
    x = decomp.decompose_tank(None)
    assert len(x) == 48


def test_decomp_tank_little_returns_correct_len(tank_little_data):
    x = decomp.decompose_tank(tank_little_data)
    assert len(x) == 48


def test_decomp_tank_full_data_returns_correct_len(tank_full_data):
    x = decomp.decompose_tank(tank_full_data)
    assert len(x) == 48
