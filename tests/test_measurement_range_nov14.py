"""Reusable measurement bounds should be explicit and fail closed."""
import pytest

from engitest.calculations import MeasurementRange, validate_measurement


def test_inclusive_range_preserves_both_endpoints():
    rule = MeasurementRange(-40, 120)
    assert rule.contains(-40)
    assert rule.contains(120)
    assert rule.contains(0)
    assert not rule.contains(-40.01)
    assert not rule.contains(120.01)


def test_validation_utility_delegates_to_the_same_range_contract():
    assert validate_measurement(5, 0, 10)
    assert not validate_measurement(11, 0, 10)


@pytest.mark.parametrize("low,high", [(3, 2), (float("nan"), 1), (0, float("inf")), (True, 1)])
def test_invalid_range_construction_fails(low, high):
    with pytest.raises(ValueError):
        MeasurementRange(low, high)


@pytest.mark.parametrize("bad", [None, True, "12", float("nan"), float("inf")])
def test_invalid_readings_cannot_pass_as_numbers(bad):
    with pytest.raises(ValueError):
        MeasurementRange(0, 100).contains(bad)
