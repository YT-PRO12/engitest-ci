from dataclasses import FrozenInstanceError

import pytest

from engitest.calculations import MeasurementRange


def test_measurement_range_is_immutable():
    rule = MeasurementRange(-20, 120)
    with pytest.raises(FrozenInstanceError):
        rule.minimum = 0


def test_measurement_range_includes_both_endpoints():
    rule = MeasurementRange(-20, 120)
    assert rule.contains(-20)
    assert rule.contains(120)
    assert not rule.contains(120.001)


@pytest.mark.parametrize("value", [True, None, "12", float("nan"), float("inf")])
def test_measurement_range_rejects_invalid_reading(value):
    with pytest.raises(ValueError):
        MeasurementRange(0, 100).contains(value)
