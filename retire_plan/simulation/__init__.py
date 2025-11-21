"""
simulation subpackage

Defines:
- TaxSystem: interface for tax calculation
- default_tax_system(): helper to build a default TaxSystem
- run_simulation(): main simulation engine

All implementations are left for Student B.
"""

from .tax_system import TaxSystem, default_tax_system
from .engine import run_simulation

__all__ = ["TaxSystem", "default_tax_system", "run_simulation"]

