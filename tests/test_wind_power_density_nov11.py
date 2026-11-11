"""Metamorphic tests of the model's published physical equation."""
import pytest

from engitest.calculations import wind_power


@pytest.mark.parametrize("speed,radius", [(2, 10), (8, 40), (15, 60)])
def test_doubling_air_density_doubles_power(speed, radius):
    baseline = wind_power(speed, radius, air_density_kg_m3=1.225)
    dense = wind_power(speed, radius, air_density_kg_m3=2.45)
    assert dense == pytest.approx(2 * baseline)


def test_halving_power_coefficient_halves_extracted_power():
    at_forty_percent = wind_power(10, 40, power_coefficient=0.4)
    at_twenty_percent = wind_power(10, 40, power_coefficient=0.2)
    assert at_twenty_percent == pytest.approx(at_forty_percent / 2)


def test_zero_wind_remains_zero_with_positive_coefficient():
    assert wind_power(0, 40, power_coefficient=16 / 27) == 0
