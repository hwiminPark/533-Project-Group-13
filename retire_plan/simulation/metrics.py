from typing import List
import numpy as np

def calculate_shortfall_years(net_worth_history: List[float], target_nw: float) -> int:
    """
    Count the number of years in the simulation where net worth falls below a target.
    Returns 0 if history is empty.
    """
    if not net_worth_history:
        return 0
    return sum(1 for nw in net_worth_history if nw < target_nw)

def estimate_lifetime_returns(return_rates: List[float], initial_nw: float) -> float:
    """
    Estimate total compounded returns over the simulation period starting from initial NW.
    Uses numpy for product of (1 + rates).
    """
    if not return_rates:
        return 0.0
    compounded = np.prod([1 + r for r in return_rates])
    return initial_nw * (compounded - 1)