# Simulation Subpackage

Simulation subpackage for the Canada Retirement Optimizer.

This subpackage orchestrates lifecycle simulations, including accumulation (pre-retirement contributions) and decumulation (post-retirement withdrawals).

## Key Classes and Functions

- **Simulator**: Runs full retirement scenarios with strategies.
- **calculate_shortfall_years**: Metrics for sustainability analysis.

## Example

```python
from retire_plan.simulation import Simulator

sim = Simulator(profile, tax_calc, contrib_strategy, withdraw_strategy)
results = sim.run_full_lifecycle(end_age=95, annual_savings=20000, return_rates=[0.05]*55)
```
