"""python -m engitest: reproducible calculation smoke example."""
import json
from .calculations import controller_error, efficiency, tip_speed_ratio, wind_power

def main():
    print(json.dumps({"wind_power_w": wind_power(10, 40),
                      "controller_error_pct": controller_error(1800, 1760),
                      "efficiency_pct": efficiency(900, 1000),
                      "tip_speed_ratio": tip_speed_ratio(15, 40, 10)}, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
