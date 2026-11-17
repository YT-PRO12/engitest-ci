"""Reference cases for the dimensionless blade-tip speed ratio."""
import math

import pytest

from engitest.calculations import tip_speed_ratio


def test_one_revolution_per_second_has_expected_tip_speed():
    radius_m = 2.0
    wind_mps = 4.0 * math.pi
    assert tip_speed_ratio(60, radius_m, wind_mps) == pytest.approx(1.0)


def test_double_wind_halves_ratio_at_fixed_rpm():
    initial = tip_speed_ratio(15, 40, 10)
    assert tip_speed_ratio(15, 40, 20) == pytest.approx(initial / 2)


@pytest.mark.parametrize("bad", [0, -1, float("nan"), True])
def test_invalid_wind_speed_is_rejected(bad):
    with pytest.raises(ValueError):
        tip_speed_ratio(15, 40, bad)
