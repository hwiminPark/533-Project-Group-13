"""
retire_plan - Retirement planning toolkit for Canadian households.

This top-level package exposes three subpackages:
- accounts: account models and person profile
- simulation: tax system and simulation engine
- strategies: withdrawal policies and analysis utilities
"""

from . import accounts
from . import simulation
from . import strategies

__all__ = ["accounts", "simulation", "strategies"]
