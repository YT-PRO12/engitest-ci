# Verification record

Executed 21 September 2026 on Linux / Python 3.12.14.

- **51/51 pytest tests passed**; zero failures, errors or skips.
- Combined statement/branch coverage: **98.11%**.
- Ruff lint checks passed.
- Source/wheel builds completed.
- GitHub Actions workflow YAML parsed successfully.
- Wheel and source archive built successfully.
- Wheel installed in a fresh temporary virtual environment; import and numeric smoke check passed.
- 90% coverage gate passed.
- Jenkinsfile is supplied; **Jenkins and Artifactory were not provisioned or executed**.

## Execution boundary

These are **local verification results**, not a claim that hosted CI or a live
public deployment has succeeded. GitHub publication, remote CI and public
link verification are pending. Windows and Python 3.11 are configured CI
targets but were not executed in this local Linux/Python 3.12 environment.
The cloud browser could not reach the isolated local server; dashboard
interactions were tested with Streamlit AppTest, and startup separately through
the HTTP health endpoint. Public browser workflow verification remains pending.

Machine-readable evidence is in `verification/`. Coverage includes the Python
package; Streamlit controls are exercised separately by the interaction tests.
