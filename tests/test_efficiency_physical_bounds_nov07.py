import pytest

from engitest.calculations import efficiency


@pytest.mark.parametrize("output, input_power, expected", [
    (0, 100, 0),
    (50, 100, 50),
    (100, 100, 100),
])
def test_efficiency_reference_values(output, input_power, expected):
    assert efficiency(output, input_power) == expected


@pytest.mark.parametrize("output, input_power", [
    (-1, 100),
    (101, 100),
    (10, 0),
    (float("inf"), 100),
    (True, 100),
])
def test_invalid_passive_efficiency_inputs(output, input_power):
    with pytest.raises(ValueError):
        efficiency(output, input_power)
