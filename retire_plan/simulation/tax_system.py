"""
Tax system model for the retire_plan package.

Provides:
- TaxSystem: simple interface with compute_tax()
- default_tax_system(): helper to construct a default TaxSystem

Implementation details are intentionally left to Student B.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TaxSystem:
    """Simple tax system interface.

    Student B should implement the tax logic for:
    - progressive tax brackets
    - credits / deductions (if desired)
    - federal vs provincial (optional)
    """

    # Optionally later: attributes for brackets / rates etc.

    def compute_tax(self, taxable_income: float) -> float:
        """Compute tax on the given taxable income.

        Parameters
        ----------
        taxable_income : float

        Returns
        -------
        float
            Tax owed for this year.

        Notes
        -----
        Student B: please implement the tax formula here.
        """
        raise NotImplementedError("TaxSystem.compute_tax() is not implemented yet.")


def default_tax_system() -> TaxSystem:
    """Construct a default TaxSystem.

    Student B can later extend this to accept parameters:
    e.g., province, year, custom brackets.
    """
    return TaxSystem()

