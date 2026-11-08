import pytest

from engitest.calculations import tip_speed_ratio


@pytest.mark.parametrize("rpm,radius,wind", [
    (5, 10, 5),
    (15, 40, 10),
    (30, 80, 12),
])
def test_rotor_speed_and_radius_scale_linearly(rpm, radius, wind):
    original = tip_speed_ratio(rpm, radius, wind)
    assert tip_speed_ratio(2 * rpm, radius, wind) == pytest.approx(2 * original)
    assert tip_speed_ratio(rpm, 2 * radius, wind) == pytest.approx(2 * original)
    assert tip_speed_ratio(rpm, radius, 2 * wind) == pytest.approx(original / 2)


def test_stationary_rotor_has_zero_tip_speed_ratio():
    assert tip_speed_ratio(0, 40, 10) == 0
