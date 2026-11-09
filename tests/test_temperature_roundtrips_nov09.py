"""Temperature conversions retain physical units under reverse conversion."""
import pytest

from engitest.calculations import temperature_conversion


@pytest.mark.parametrize("value", [-273.15, -40, 0, 37, 100])
def test_celsius_fahrenheit_roundtrip(value):
    fahrenheit = temperature_conversion(value, "C", "F")
    restored = temperature_conversion(fahrenheit, "F", "C")
    assert restored == pytest.approx(value, abs=1e-9)


@pytest.mark.parametrize("value", [0, 1, 273.15, 373.15, 1000])
def test_kelvin_celsius_roundtrip(value):
    celsius = temperature_conversion(value, "K", "C")
    restored = temperature_conversion(celsius, "C", "K")
    assert restored == pytest.approx(value, abs=1e-9)


def test_below_absolute_zero_is_rejected():
    with pytest.raises(ValueError):
        temperature_conversion(-273.151, "C", "K")
