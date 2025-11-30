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