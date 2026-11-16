"""Physical efficiency cannot exceed 100% or accept invalid readings."""
import pytest

from engitest.calculations import efficiency


@pytest.mark.parametrize("output, supplied, expected", [
    (0, 100, 0), (1, 4, 25), (75, 100, 75), (100, 100, 100),
])
def test_efficiency_endpoints_and_reference_values(output, supplied, expected):
    assert efficiency(output, supplied) == pytest.approx(expected)


@pytest.mark.parametrize("output, supplied", [(1, 4), (6, 10), (90, 100)])
def test_scaling_both_powers_does_not_change_efficiency(output, supplied):
    assert efficiency(10 * output, 10 * supplied) == pytest.approx(
        efficiency(output, supplied)
    )


@pytest.mark.parametrize("output, supplied", [
    (101, 100), (-1, 100), (1, 0), (True, 2), (float("nan"), 100),
])
def test_nonphysical_efficiency_inputs_fail(output, supplied):
    with pytest.raises(ValueError):
        efficiency(output, supplied)
