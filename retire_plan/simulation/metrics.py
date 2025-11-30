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