# Embedded Systems Validation Lab — Starter 01

**Goal:** build transferable Python / Pytest / CI skills for automotive, robotics, and embedded system testing.

**This is a synthetic educational model, not a certified AEB implementation.** It assumes a straight line, a lead vehicle with constant speed, a simple TTC threshold, fixed response delay, and constant braking deceleration. It does not model sensors, perception, tire friction, road curvature, actual controller requirements, or ISO 26262/SOTIF compliance. The `minimum_gap_m` field records the minimum gap during the simulated interval; the simulation stops early once AEB has activated and the vehicles are no longer closing.

## Run on existing Ubuntu / WSL2

```bash
# First unzip this folder into your Ubuntu home directory.
cd ~/embedded_validation_starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python generate_report.py
```

Expected: **17 passed**, followed by a CSV and a JSON report in `reports/`.

## Engineering exercise

1. Explain why a scenario with the same speed for the ego and lead vehicles has no finite constant-speed TTC.
2. Increase response delay and observe the change in collision outcome.
3. Propose an additional edge-case test (e.g., initially zero gap or invalid parameters).
4. Review the simulation assumptions; note what is missing before making any safety claim.

## Roadmap

- Week 1: improve scenario coverage, assertions and traceable reports.
- Next: plug a scenario controller into **Eclipse SUMO** via TraCI.
- Next: run the suite in CI; the included GitHub Actions workflow provides a baseline.
- Next: let the OpenShell agent **interpret** a report using an approved tool, without granting access to confidential data or modifying tests without approval.

**Cost:** software and the included example: 0 €; downloading Python packages requires ordinary internet, not an AI API or GPU cloud. The included GitHub Actions workflow is intended for public repositories under currently available free hosted runner policies; limits can change.
# Git practice: learning version control

## Continuous Integration
Jenkins automatically runs AEB tests after detecting new Git commits.

### Jenkins Validation Pipeline

- Automatic SCM polling checks for new Git commits.
- Tests run on a Docker-based Jenkins Python Agent.
- All 17 automated tests must pass.
- Minimum required code coverage: 95%.
- JUnit test results and coverage reports are retained.
- The test environment is created from requirements-dev.txt.

This is an educational AEB simulation and not a certified
automotive safety system.
