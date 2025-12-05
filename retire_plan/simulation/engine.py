"""
Simulation engine for the retire_plan package.
"""

from __future__ import annotations

from typing import List, Dict, Any, Callable, Sequence
import copy

from retire_plan.accounts import PersonProfile
from .metrics import TaxCalculator
from retire_plan.strategies.policies import (
    contrib_max_tfsa_first,
    contrib_max_rrsp_first,
    strategy_spend_taxable_first,
    strategy_spend_rrsp_first,
    strategy_smooth_with_tfsa,
)

StrategyFunc = Callable[[Dict[str, Any]], Dict[str, float]]


class Simulator:
    def __init__(self, profile: PersonProfile, tax_calculator: TaxCalculator | None = None):
        self.original_profile = profile
        self.profile = copy.deepcopy(profile)
        self.tax_calc = tax_calculator or TaxCalculator()
        self.history: List[Dict[str, Any]] = []  # Full lifecycle history

    def reset(self):
        self.profile = copy.deepcopy(self.original_profile)
        self.history.clear()

    # --------------------------------------------------------------
    # 1. Accumulation phase – records every year
    # --------------------------------------------------------------
    def run_accumulation(
        self,
        contribution_strategy: StrategyFunc,
        years_to_retirement: int,
        annual_savings: float = 30_000,
        return_rate: float = 0.07,
    ) -> None:
        age = self.profile.current_age

        for year in range(years_to_retirement):
            current_age = age + year

            state = {
                "age": current_age,
                "annual_savings_available": annual_savings,
                "balances": self.profile.all_balances(),
            }
            plan = contribution_strategy(state)

            # Apply contributions
            for key, amt in plan.items():
                if amt > 0:
                    {
                        "tax_deferred": self.profile.tax_deferred,
                        "tax_free": self.profile.tax_free,
                        "taxable": self.profile.taxable,
                    }[key].deposit(amt)

            # Grow accounts
            for acc in (self.profile.tax_deferred, self.profile.tax_free, self.profile.taxable):
                acc.annual_return = return_rate
                acc.grow()

            # RECORD ACCUMULATION YEAR
            self.history.append({
                "age": current_age + 1,
                "phase": "accumulation",
                "total_wealth": self.profile.total_balance(),
                "end_balances": self.profile.all_balances(),
            })

        # Advance age to retirement
        self.profile.current_age = age + years_to_retirement

    # --------------------------------------------------------------
    # 2. Decumulation phase – appends to existing history
    # --------------------------------------------------------------
    def run_decumulation(
        self,
        withdrawal_strategy: StrategyFunc,
        annual_spending: float = 70_000,
        inflation_rate: float = 0.02,
        return_rate: float = 0.05,
    ) -> None:
        current_age = self.profile.current_age
        spending = annual_spending

        for year in range(self.profile.retirement_horizon()):
            age = current_age + year

            state = {
                "age": age,
                "target_net_cash": spending,
                "cpp_income": self.profile.cpp_annual,
                "oas_income": self.profile.oas_annual,
                "balances": self.profile.all_balances(),
            }
            plan = withdrawal_strategy(state)

            taxable_income = gross_withdrawn = 0.0
            for key, amt in plan.items():
                if amt <= 0:
                    continue
                acc = {
                    "tax_deferred": self.profile.tax_deferred,
                    "tax_free": self.profile.tax_free,
                    "taxable": self.profile.taxable,
                }[key]
                inc, cash = acc.withdraw(amt)
                taxable_income += inc
                gross_withdrawn += cash

            tax_paid = self.tax_calc.tax_on(taxable_income)
            net_cash = gross_withdrawn - tax_paid + self.profile.annual_gov_benefits()

            # Growth after withdrawal
            for acc in (self.profile.tax_deferred, self.profile.tax_free, self.profile.taxable):
                acc.annual_return = return_rate
                acc.grow()

            # RECORD DECUMULATION YEAR
            self.history.append({
                "age": age,
                "phase": "decumulation",
                "spending": spending,
                "gross_withdrawal": gross_withdrawn,
                "tax_paid": tax_paid,
                "net_cash_flow": net_cash,
                "total_wealth": self.profile.total_balance(),
                "end_balances": self.profile.all_balances(),
            })

            spending *= (1 + inflation_rate)

    # --------------------------------------------------------------
    # 3. Full lifecycle – now preserves full history
    # --------------------------------------------------------------
    def run_full_lifecycle(
        self,
        contribution_strategy: StrategyFunc,
        withdrawal_strategy: StrategyFunc,
        years_working: int = 35,
        annual_savings: float = 28_000,
        annual_spending: float = 80_000,
    ) -> Dict[str, Any]:
        self.reset()
        self.run_accumulation(contribution_strategy, years_working, annual_savings)
        self.run_decumulation(withdrawal_strategy, annual_spending)

        total_tax = sum(r.get("tax_paid", 0) for r in self.history if "tax_paid" in r)
        final_wealth = self.history[-1]["total_wealth"]
        ruin_age = next((r["age"] for r in self.history if r["total_wealth"] < 1_000), None)

        return {
            "final_wealth": final_wealth,
            "total_tax_paid": total_tax,
            "ruin_age": ruin_age,
            "success": ruin_age is None,
            "peak_wealth": max(r["total_wealth"] for r in self.history),
            "history": self.history,
        }

    # --------------------------------------------------------------
    # 4. Optimizer – unchanged
    # --------------------------------------------------------------
    @staticmethod
    def optimize(
        base_profile: PersonProfile,
        contribution_strategies: Sequence[tuple[str, StrategyFunc]],
        withdrawal_strategies: Sequence[tuple[str, StrategyFunc]],
        years_working: int = 35,
        annual_savings: float = 28_000,
        annual_spending: float = 80_000,
    ) -> List[Dict[str, Any]]:
        results = []
        tax_calc = TaxCalculator()

        for c_name, c_strat in contribution_strategies:
            for w_name, w_strat in withdrawal_strategies:
                sim = Simulator(base_profile, tax_calc)
                outcome = sim.run_full_lifecycle(
                    c_strat, w_strat,
                    years_working=years_working,
                    annual_savings=annual_savings,
                    annual_spending=annual_spending,
                )
                results.append({
                    "contrib_strategy": c_name,
                    "withdraw_strategy": w_name,
                    **outcome
                })

        return sorted(results, key=lambda x: x["total_tax_paid"])