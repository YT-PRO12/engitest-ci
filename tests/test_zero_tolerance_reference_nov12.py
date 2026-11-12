"""At zero demand, tolerance_check uses an absolute threshold."""
import pytest

from engitest.calculations import tolerance_check, controller_error


def test_zero_expected_with_small_absolute_error_passes():
    assert tolerance_check(0, 0.4, tolerance_pct=5, zero_tolerance=0.5)
    assert not tolerance_check(0, 0.6, tolerance_pct=5, zero_tolerance=0.5)


def test_exact_zero_expected_and_actual_have_zero_error():
    assert controller_error(0, 0) == 0
    assert tolerance_check(0, 0, tolerance_pct=0, zero_tolerance=0)


def test_percent_error_with_zero_expected_and_positive_actual_is_undefined():
    with pytest.raises(ValueError, match="undefined"):
        controller_error(0, 0.1)


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), True])
def test_invalid_absolute_tolerance_is_rejected(value):
    with pytest.raises(ValueError):
        tolerance_check(0, 0, zero_tolerance=value)
