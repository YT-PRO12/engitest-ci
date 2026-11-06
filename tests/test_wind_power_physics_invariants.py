"""The simplified wind-power equation should retain its analytic invariants."""
import pytest

from engitest.calculations import wind_power


@pytest.mark.parametrize("speed", [2, 5, 10, 20])
def test_doubling_speed_multiplies_extracted_power_by_eight(speed):
    low = wind_power(speed, 40)
    high = wind_power(2 * speed, 40)
    assert high == pytest.approx(8 * low)


def test_zero_wind_has_zero_extracted_power():
    assert wind_power(0, 40) == 0.0


def test_betz_limit_is_inclusive_but_excess_is_rejected():
    assert wind_power(10, 40, power_coefficient=16 / 27) > 0
    with pytest.raises(ValueError):
        wind_power(10, 40, power_coefficient=0.6)
