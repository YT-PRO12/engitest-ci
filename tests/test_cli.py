import json
from engitest.__main__ import main

def test_cli_json(capsys):
    main()
    data = json.loads(capsys.readouterr().out)
    assert data["efficiency_pct"] == 90
    assert data["controller_error_pct"] > 0
