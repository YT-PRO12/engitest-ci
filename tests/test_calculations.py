import math
import pytest
from engitest.calculations import (wind_power, controller_error, efficiency, tip_speed_ratio,
    temperature_conversion, tolerance_check, validate_measurement, MeasurementRange)

def test_reference_wind_power():
    # Independently calculated analytical fixture: 0.5*1.225*pi*40²*10³*0.4.
    assert wind_power(10, 40) == pytest.approx(1231504.3202071988)

def test_wind_scaling_and_zero():
    assert wind_power(20, 40) == pytest.approx(8 * wind_power(10, 40))
    assert wind_power(10, 80) == pytest.approx(4 * wind_power(10, 40))
    assert wind_power(0, 40) == 0
    assert wind_power(10, 40, power_coefficient=0) == 0
    assert wind_power(10, 40, power_coefficient=16/27) > 0

@pytest.mark.parametrize("kwargs", [{"wind_speed_mps":-1},{"rotor_radius_m":0},{"air_density_kg_m3":0},
    {"power_coefficient":.6},{"power_coefficient":-.1},{"wind_speed_mps":1e200}])
def test_invalid_wind_inputs(kwargs):
    args = {"wind_speed_mps":10,"rotor_radius_m":40}
    args.update(kwargs)
    with pytest.raises(ValueError):
        wind_power(**args)

@pytest.mark.parametrize("bad", [float("nan"),float("inf"),-float("inf"),True,"10",None])
def test_reject_non_finite_and_non_numeric(bad):
    with pytest.raises(ValueError):
        wind_power(bad, 40)
    with pytest.raises(ValueError):
        MeasurementRange(0, bad)
    with pytest.raises(ValueError):
        validate_measurement(bad, 0, 100)

@pytest.mark.parametrize("expected,actual,error", [(1800,1760,2.222222222222),(100,105,5),(100,95,5),(0,0,0)])
def test_controller_regression(expected, actual, error):
    assert controller_error(expected, actual) == pytest.approx(error)

def test_controller_zero_and_overflow():
    with pytest.raises(ValueError, match="undefined"):
        controller_error(0, 1)
    with pytest.raises(ValueError):
        controller_error(1e-300, 1e300)

@pytest.mark.parametrize("actual,status", [(95,True),(105,True),(94.99,False),(105.01,False)])
def test_tolerance_boundaries(actual, status):
    assert tolerance_check(100, actual) is status

def test_tolerance_zero_and_invalid():
    assert tolerance_check(0, .5, zero_tolerance=.5)
    assert not tolerance_check(0, .5001, zero_tolerance=.5)
    assert tolerance_check(.1, .105, tolerance_pct=5)
    with pytest.raises(ValueError):
        tolerance_check(100,100,-1)

@pytest.mark.parametrize("output,supplied,expected", [(900,1000,90),(0,1000,0),(1000,1000,100)])
def test_efficiency(output, supplied, expected):
    assert efficiency(output,supplied) == expected

@pytest.mark.parametrize("args", [(1,0),(110,100),(-1,100)])
def test_efficiency_invalid(args):
    with pytest.raises(ValueError):
        efficiency(*args)

def test_tip_speed_ratio():
    assert tip_speed_ratio(15,40,10) == pytest.approx(2 * math.pi)
    assert tip_speed_ratio(0,40,10) == 0
    with pytest.raises(ValueError):
        tip_speed_ratio(15,40,0)
    with pytest.raises(ValueError):
        tip_speed_ratio(1e300,1e300,1)

@pytest.mark.parametrize("value,source,target,expected", [(0,"C","K",273.15),(100,"C","F",212),
    (32,"F","C",0),(273.15,"K","C",0),(-273.15,"C","K",0),(0,"K","F",-459.67),
    (10,"C","C",10),(32,"F","F",32),(273.15,"K","K",273.15)])
def test_temperature_regression(value, source, target, expected):
    assert temperature_conversion(value,source,target) == pytest.approx(expected)

@pytest.mark.parametrize("args", [(-274,"C","K"),(-1,"K","C"),(0,"bad","C"),(0,"C","bad")])
def test_temperature_invalid(args):
    with pytest.raises(ValueError):
        temperature_conversion(*args)

@pytest.mark.parametrize("value,expected", [(0,True),(100,True),(50,True),(-.01,False),(100.01,False)])
def test_measurement_boundaries(value, expected):
    assert validate_measurement(value,0,100) is expected

def test_invalid_range_order():
    with pytest.raises(ValueError):
        MeasurementRange(100, 0)
