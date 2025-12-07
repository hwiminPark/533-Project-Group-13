# demo_runner.py
"""
Interactive Retirement Planner
Let users input their own numbers → instantly see the BEST strategy
"""

from retire_plan import PersonProfile
from retire_plan.accounts import TaxDeferredAccount, TaxFreeAccount, TaxableAccount
from retire_plan.simulation.engine import Simulator
from retire_plan.strategies.policies import (
    contrib_max_tfsa_first,
    contrib_max_rrsp_first,
    strategy_spend_taxable_first,
    strategy_spend_rrsp_first,
    strategy_smooth_with_tfsa,
)

import matplotlib.pyplot as plt


def get_float(prompt: str, default: float | None = None, min_val: float | None = None) -> float:
    while True:
        try:
            value = input(f"{prompt} [{default if default is not None else ''}]: ").strip()
            if value == "" and default is not None:
                return default
            num = float(value.replace(",", "").replace("$", ""))
            if min_val is not None and num < min_val:
                print(f"   Please enter a value >= {min_val}")
                continue
            return num
        except ValueError:
            print("   Please enter a valid number")


def main():
    print("\n" + "="*60)
    print("    RETIREMENT PLAN OPTIMIZER – Interactive Mode".center(60))
    print("="*60 + "\n")

    # === User Input ===
    name = input("Your name (or household): ").strip() or "Retiree"

    current_age = int(get_float("Current age", 35, 20))
    retirement_age = int(get_float("Desired retirement age", 65, current_age + 1))
    end_age = int(get_float("Life expectancy (planning age)", 95, retirement_age + 10))

    print("\nCurrent savings (enter 0 if none):")
    rrsp_bal = get_float("  RRSP/RRIF balance ($)", 50_000, 0)
    tfsa_bal = get_float("  TFSA balance ($)", 30_000, 0)
    taxable_bal = get_float("  Non-registered balance ($)", 10_000, 0)

    print("\nFuture plans:")
    annual_savings = get_float("Annual savings during working years ($)", 28_000, 0)
    desired_spending = get_float("Desired annual spending in retirement (after-tax) ($)", 80_000, 10000)

    cpp = get_float("Expected annual CPP (today's $) [0 if unsure]", 15_000, 0)
    oas = get_float("Expected annual OAS (today's $) [0 if unsure]", 8_184, 0)

    # === Build Profile ===
    profile = PersonProfile(
        name=name,
        current_age=current_age,
        end_age=end_age,
        tax_deferred=TaxDeferredAccount("RRSP/RRIF", balance=rrsp_bal, annual_return=0.07),
        tax_free=TaxFreeAccount("TFSA", balance=tfsa_bal, annual_return=0.07),
        taxable=TaxableAccount("Non-registered", balance=taxable_bal, annual_return=0.07),
        cpp_annual=cpp,
        oas_annual=oas,
    )

    years_working = retirement_age - current_age

    print(f"\nRunning optimization for {name}...")
    print(f"   Working years: {current_age} → {retirement_age} ({years_working} years)")
    print(f"   Retirement: {retirement_age} → {end_age} ({end_age - retirement_age} years)")
    print("   Testing all 6 strategy combinations...\n")

    # === Run Optimizer ===
    results = Simulator.optimize(
        base_profile=profile,
        contribution_strategies=[
            ("TFSA-First", contrib_max_tfsa_first),
            ("RRSP-First", contrib_max_rrsp_first),
        ],
        withdrawal_strategies=[
            ("Taxable-First", strategy_spend_taxable_first),
            ("RRSP-First", strategy_spend_rrsp_first),
            ("Smooth-with-TFSA", strategy_smooth_with_tfsa),
        ],
        years_working=years_working,
        annual_savings=annual_savings,
        annual_spending=desired_spending,
    )

    best = results[0]

    # === Results ===
    print("OPTIMAL STRATEGY FOUND".center(60, "="))
    print(f"Name                  : {name}")
    print(f"Best Contribution     : {best['contrib_strategy']}")
    print(f"Best Withdrawal       : {best['withdraw_strategy']}")
    print(f"Lifetime Tax Paid     : ${best['total_tax_paid']:,.0f}")
    print(f"Final Wealth (Age {end_age}) : ${best['final_wealth']:,.0f}")
    print(f"Peak Wealth           : ${best['peak_wealth']:,.0f}")
    print(f"Success (Funds last)  : {'YES' if best['success'] else 'NO'}")
    print("="*60)

    # === Graph ===
    history = best["history"]
    ages = [y["age"] for y in history]
    wealth = [y["total_wealth"] for y in history]

    plt.figure(figsize=(15, 9))
    plt.plot(ages, wealth, color='green', linewidth=4, label="Your Optimal Path")

    plt.axvline(retirement_age, color='red', linestyle='--', linewidth=2, label=f"Retirement (Age {retirement_age})")
    plt.axhline(0, color='black', linewidth=1)

    plt.title(
        f"Optimal Retirement Plan for {name}\n"
        f"{best['contrib_strategy']} + {best['withdraw_strategy']} → "
        f"Ends with ${best['final_wealth']:,.0f} (Age {end_age})",
        fontsize=18, pad=20
    )
    plt.xlabel("Age", fontsize=14)
    plt.ylabel("Total Wealth ($)", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()