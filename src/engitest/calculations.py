"""Small engineering calculations with explicit SI units and input contracts."""
from dataclasses import dataclass
import math
from numbers import Real

def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number")
    return float(value)

def _positive(value, name, allow_zero=False):
    value = _number(value, name)
    if value < 0 or (not allow_zero and value == 0):
        raise ValueError(f"{name} must be {'non-negative' if allow_zero else 'positive'}")
    return value

def wind_power(wind_speed_mps, rotor_radius_m, air_density_kg_m3=1.225, power_coefficient=0.4):
    """Extracted aerodynamic power in watts: 0.5*rho*pi*r²*v³*Cp.

    Steady uniform flow, no drivetrain losses or rated-power clipping.
    Cp must be between zero and the ideal Betz limit (16/27).
    """
    speed = _positive(wind_speed_mps, "wind_speed_mps", allow_zero=True)
    radius = _positive(rotor_radius_m, "rotor_radius_m")
    density = _positive(air_density_kg_m3, "air_density_kg_m3")
    cp = _number(power_coefficient, "power_coefficient")
    if not 0 <= cp <= 16 / 27:
        raise ValueError("power_coefficient must be within 0..16/27")
    try:
        result = 0.5 * density * math.pi * radius**2 * speed**3 * cp
    except OverflowError as exc:
        raise ValueError("wind_power exceeds numeric limits") from exc
    return _number(result, "wind_power result")

def controller_error(expected, actual):
    """Absolute percent error. 0 vs 0 is 0; nonzero vs 0 is undefined."""
    expected = _positive(expected, "expected", allow_zero=True)
    actual = _positive(actual, "actual", allow_zero=True)
    if expected == 0:
        if actual == 0:
            return 0.0
        raise ValueError("Percentage error is undefined for zero expected output")
    return _number(abs(actual - expected) / expected * 100, "controller_error result")

def efficiency(output_power_w, input_power_w):
    """Percent efficiency for a passive steady-state device, from 0 to 100."""
    output = _positive(output_power_w, "output_power_w", allow_zero=True)
    supplied = _positive(input_power_w, "input_power_w")
    if output > supplied:
        raise ValueError("output_power_w cannot exceed input_power_w")
    return output / supplied * 100

def tip_speed_ratio(rotor_rpm, rotor_radius_m, wind_speed_mps):
    """Dimensionless blade-tip speed divided by positive wind speed."""
    rpm = _positive(rotor_rpm, "rotor_rpm", allow_zero=True)
    radius = _positive(rotor_radius_m, "rotor_radius_m")
    wind = _positive(wind_speed_mps, "wind_speed_mps")
    return _number((rpm * 2 * math.pi / 60) * radius / wind, "tip_speed_ratio result")

def temperature_conversion(value, from_unit="C", to_unit="K"):
    """Convert C/F/K and reject input below absolute zero."""
    value = _number(value, "temperature")
    if from_unit not in ("C", "F", "K") or to_unit not in ("C", "F", "K"):
        raise ValueError("Temperature units must be C, F or K")
    celsius = value if from_unit == "C" else value - 273.15 if from_unit == "K" else (value - 32) * 5 / 9
    if celsius < -273.15 - 1e-10:
        raise ValueError("Temperature is below absolute zero")
    celsius = max(celsius, -273.15)
    result = celsius if to_unit == "C" else celsius + 273.15 if to_unit == "K" else celsius * 9 / 5 + 32
    return _number(result, "converted temperature")

def tolerance_check(expected, actual, tolerance_pct=5.0, zero_tolerance=0.0):
    """Inclusive relative tolerance; absolute tolerance at exactly zero demand."""
    expected = _positive(expected, "expected", allow_zero=True)
    actual = _positive(actual, "actual", allow_zero=True)
    tolerance = _number(tolerance_pct, "tolerance_pct")
    absolute = _positive(zero_tolerance, "zero_tolerance", allow_zero=True)
    if not 0 <= tolerance <= 100:
        raise ValueError("tolerance_pct must be within 0..100")
    allowed = expected * (tolerance / 100) if expected else absolute
    difference = abs(actual - expected)
    return difference <= allowed or math.isclose(difference, allowed, rel_tol=1e-12, abs_tol=1e-12)

@dataclass(frozen=True)
class MeasurementRange:
    """Reusable inclusive finite-number range contract."""
    minimum: float
    maximum: float

    def __post_init__(self):
        low = _number(self.minimum, "minimum")
        high = _number(self.maximum, "maximum")
        if low > high:
            raise ValueError("minimum must not exceed maximum")

    def contains(self, value):
        value = _number(value, "measurement")
        return self.minimum <= value <= self.maximum

def validate_measurement(value, minimum, maximum):
    """Return whether a finite measurement lies in the inclusive range."""
    return MeasurementRange(minimum, maximum).contains(value)
