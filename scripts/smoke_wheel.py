"""Install the built wheel in a clean temporary venv, outside the checkout."""
import json
from pathlib import Path
import subprocess
import tempfile
import venv
import os

wheels = list(Path("dist").resolve().glob("*.whl"))
if len(wheels) != 1:
    raise SystemExit("Expected exactly one wheel in dist/")
with tempfile.TemporaryDirectory() as folder:
    target = Path(folder)
    venv.EnvBuilder(with_pip=True).create(target / "venv")
    python = target / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", "--no-deps", str(wheels[0])], check=True, cwd=target)
    output = subprocess.check_output([str(python), "-m", "engitest"], text=True, cwd=target)
    data = json.loads(output)
    assert data["efficiency_pct"] == 90.0
    assert abs(data["wind_power_w"] - 1231504.3202071988) < 1e-6
    print("Built wheel import and numerical smoke check: PASS")
