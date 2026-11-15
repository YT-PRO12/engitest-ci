"""The idealized aerodynamic equation scales with rotor swept area."""
import pytest

from engitest.calculations import wind_power


@pytest.mark.parametrize("radius", [2.0, 10.0, 40.0])
def test_double_rotor_radius_quadruples_extracted_power(radius):
    baseline = wind_power(8.0, radius)
    doubled = wind_power(8.0, radius * 2)
    assert doubled == pytest.approx(4 * baseline, rel=1e-12)


def test_zero_power_coefficient_yields_zero_extraction():
    assert wind_power(12.0, 40.0, power_coefficient=0.0) == 0.0


@pytest.mark.parametrize("invalid", [-0.001, 1.0, True, float("nan")])
def test_invalid_power_coefficient_fails_closed(invalid):
    with pytest.raises(ValueError):
        wind_power(10.0, 40.0, power_coefficient=invalid)
