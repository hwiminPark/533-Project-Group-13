# 533-Project-Group-13
# This line was added by SageYang

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
        tax_system.py
        engine.py

    strategies/            # Student C: withdrawal strategies & analysis
        __init__.py
        policies.py
        analysis.py

demo_runner.py             # Demo script entry point (placeholder for now)
