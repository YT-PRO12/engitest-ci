"""Tolerance checks are inclusive at their configured boundaries."""
import pytest

from engitest.calculations import tolerance_check


def test_relative_tolerance_includes_both_bounds():
    assert tolerance_check(100, 95, tolerance_pct=5)
    assert tolerance_check(100, 105, tolerance_pct=5)
    assert not tolerance_check(100, 94, tolerance_pct=5)
    assert not tolerance_check(100, 106, tolerance_pct=5)


def test_zero_tolerance_allows_only_exact_equality():
    assert tolerance_check(100, 100, tolerance_pct=0)
    assert not tolerance_check(100, 101, tolerance_pct=0)
    assert tolerance_check(0, 0, tolerance_pct=0, zero_tolerance=0)


@pytest.mark.parametrize("invalid", [True, float("nan"), float("inf"), -1, 101])
def test_invalid_percentage_is_rejected(invalid):
    with pytest.raises(ValueError):
        tolerance_check(100, 100, tolerance_pct=invalid)
