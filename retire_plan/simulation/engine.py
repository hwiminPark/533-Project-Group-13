from typing import List, Dict, Any
from ..accounts import PersonProfile, TaxCalculator
from ..strategies.policies import Strategy
from .metrics import calculate_shortfall_years, project_tax_efficiency

class Simulator:
    """
    Core simulation engine for retirement optimization.
    Composes a PersonProfile, TaxCalculator, and contribution/withdrawal strategies
    to run full lifecycle simulations.
    """

    def __init__(self, profile: PersonProfile, tax_calc: TaxCalculator,
                 contrib_strategy: Strategy, withdraw_strategy: Strategy):
        """
        Initialize the simulator with profile, tax calculator, and strategies.
        Sets up empty histories for tracking net worth and taxes over time.
        """
        self.profile = profile
        self.tax_calc = tax_calc
        self.contrib_strategy = contrib_strategy
        self.withdraw_strategy = withdraw_strategy
        self.net_worth_history: List[float] = []
        self.tax_history: List[float] = []

    def simulate_accumulation_phase(self, retirement_age: int, annual_savings: float,
                                    return_rates: List[float]) -> None:
        """
        Simulate pre-retirement accumulation: Update income history, apply contributions
        up to room limits, grow accounts with returns, and age the profile.
        Loops from current age to retirement_age - 1.
        """
        current_age = self.profile.age
        for year in range(retirement_age - current_age):
            # Add current income to history for RRSP room calculation
            self.profile.add_prior_income(self.profile.income)
            
            # Get annual contributions via strategy
            contribs = self.contrib_strategy.get_annual_actions(year, self.profile, annual_savings)
            for acc, amt in contribs.items():
                room = acc.update_room(self.profile.prior_income_history[-1])
                acc.contribute_up_to_room(amt, room)
            
            # Apply returns to all accounts
            for acc in self.profile.accounts:
                acc.apply_return(return_rates[year])
            
            # Age the profile
            self.profile.update_ages(1)