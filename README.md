# 533-Project-Group-13

## 01 Package Structure

```text
retireplan/
├── src/
│   └── retireplan/
│       ├── __init__.py
│       ├── accounts/
│       │   ├── __init__.py
│       │   ├── accounts.py
│       │   ├── models.py
│       │   └── profile.py
│       ├── simulation/
│       │   ├── __init__.py
│       │   ├── engine.py
│       │   ├── metrics.py
│       │   └── README.md
│       └── strategies/
│           ├── __init__.py
│           ├── analysis.py
│           ├── policies.py
│           └── strategies.md
├── tests/
│   ├── __init__.py
│   ├── test_analysis.py
│   ├── test_engine.py
│   ├── test_metrics.py
│   ├── test_models.py
│   ├── test_policies.py
│   ├── test_profile.py
│   └── test_suite.py
├── demo_runner.py
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt

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
