# 533-Project-Group-13

## 01 Package Structure

```text
retire_plan/
    __init__.py

    accounts/              # Student A: account models & profile
        __init__.py
        models.py          # AccountBase + 3 concrete account types
        profile.py         # PersonProfile

    simulation/            # Student B: simulation engine & tax system
        __init__.py
        metrics.py
        engine.py

    strategies/            # Student C: withdrawal strategies & analysis
        __init__.py
        policies.py
        analysis.py

demo_runner.py             # Demo script entry point (placeholder for now)

```

## 02 Testing & documentation responsibilities

In our group, the responsibilities are:

Accounts sub-package (retire_plan.accounts)

Implementation: Sage Yang

Documentation + tests: Rex (writes the user-facing documentation and unit tests for the accounts models and PersonProfile.)

Simulation sub-package (retire_plan.simulation)

Implementation: Hwimin

Documentation + tests: Sage Yang (writes the documentation and unittest-based test suite in tests/test_engine.py and tests/test_metrics.py.)

Strategies sub-package (retire_plan.strategies)

Implementation: Rex

Documentation + tests: Hwimin (writes the documentation and unit tests for withdrawal strategies and analysis helpers.)
