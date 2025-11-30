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

    def simulate_end_of_life_net_worth(self, end_age: int, return_rates: List[float]) -> Dict[str, Any]:
        """
        Simulate post-retirement: Apply withdrawals to meet spending target,
        calculate taxes, apply returns, and track net worth/taxes.
        Loops from current age to end_age - 1; returns summary dict.
        """
        current_age = self.profile.age
        for year in range(end_age - current_age):
            # Get annual withdrawals via strategy (available = spending_target)
            withdrawals = self.withdraw_strategy.get_annual_actions(
                year, self.profile, self.profile.spending_target
            )
            total_withdrawn = 0
            for acc, amt in withdrawals.items():
                withdrawn = acc.withdraw(amt)
                total_withdrawn += withdrawn
            
            # Calculate taxes on withdrawals
            gross = total_withdrawn
            deductions = {'rrsp': 0}  # Placeholder; could track unused
            taxable = self.tax_calc.calc_taxable_income(gross, deductions)
            net_income = self.tax_calc.calc_net_income(taxable)
            tax_paid = gross - net_income
            self.tax_history.append(tax_paid)
            
            # Apply returns after withdrawals
            for acc in self.profile.accounts:
                acc.apply_return(return_rates[year])
            
            # Track net worth
            nw = self.profile.get_total_net_worth()
            self.net_worth_history.append(nw)
            
            # Age the profile
            self.profile.update_ages(1)
        
        # Compute integrated metrics
        shortfalls = calculate_shortfall_years(self.net_worth_history, self.profile.spending_target * 25)  # 25x rule target
        tax_eff = project_tax_efficiency(self.tax_history, sum(self.net_worth_history) / len(self.net_worth_history))  # Avg NW as proxy
        
        return {
            'final_nw': self.net_worth_history[-1] if self.net_worth_history else 0,
            'total_taxes': sum(self.tax_history),
            'shortfall_years': shortfalls,
            'tax_efficiency': tax_eff
        }
    
    def run_full_lifecycle(self, end_age: int, annual_savings: float, return_rates: List[float]) -> Dict[str, Any]:
        """
        Run complete lifecycle: Accumulation phase followed by decumulation.
        Resets histories before starting; returns end-of-life summary.
        """
        self.net_worth_history = []
        self.tax_history = []
        retirement_age = self.profile.retirement_age
        
        self.simulate_accumulation_phase(retirement_age, annual_savings, return_rates)
        return self.simulate_end_of_life_net_worth(end_age, return_rates)