"""
Analysis utilities for retire_plan strategies.

All functions operate only on the results list returned by run_simulation().
Implementation details are left to Student C.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
import statistics  # 新增：用來計算平均與標準差


def summarize_results(name: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute high-level summary metrics from a simulation result list.

    Expected result keys per year:
    - 'age'
    - 'gross_income'
    - 'taxable_income'
    - 'tax_paid'
    - 'net_cash_flow'
    - 'end_balances'

    Student C: implement summary calculations here (total tax, ruin age, etc.).
    """
    if not results:
        raise ValueError("results must be a non-empty list")

    # 1. 終身總稅金（把每年的 tax_paid 加總）
    lifetime_tax = sum(float(r.get("tax_paid", 0.0)) for r in results)

    # 2. 期末資產（最後一年 end_balances 中三個帳戶加總）
    last_balances = results[-1].get("end_balances", {})
    final_wealth = sum(float(v) for v in last_balances.values())

    # 3. 破產年齡（第一次出現總資產幾乎為 0 的年）
    ruin_age = None
    for r in results:
        balances = r.get("end_balances", {})
        total_balance = sum(float(v) for v in balances.values())
        if total_balance <= 1e-6:  # 視為資產已耗盡
            ruin_age = int(r.get("age"))
            break

    # 4. 每年淨現金流的平均與標準差（衡量收入是否平滑）
    net_flows = [float(r.get("net_cash_flow", 0.0)) for r in results]
    avg_net_cash = statistics.mean(net_flows)
    stdev_net_cash = statistics.pstdev(net_flows) if len(net_flows) > 1 else 0.0

    # 回傳一個 summary dict，後續 compare_strategies 可以直接拿來用
    return {
        "name": name,
        "lifetime_tax": lifetime_tax,
        "final_wealth": final_wealth,
        "ruin_age": ruin_age,
        "avg_net_cash": avg_net_cash,
        "stdev_net_cash": stdev_net_cash,
    }


def compare_strategies(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare multiple strategy summaries.

    This may return, for example:
    - the name of the lowest-tax strategy
    - the highest-final-wealth strategy
    - any other comparison metrics Student C decides.

    Student C: implement comparison logic here.
    """
    if not summaries:
        raise ValueError("summaries must be a non-empty list")

    # 找出終身稅金最低的策略
    lowest_tax_summary = min(
        summaries, key=lambda s: float(s.get("lifetime_tax", float("inf")))
    )

    # 找出期末資產最高的策略
    highest_wealth_summary = max(
        summaries, key=lambda s: float(s.get("final_wealth", float("-inf")))
    )

    # 可以同時把全部 summary 一起回傳，方便上層列印表格
    return {
        "lowest_tax_strategy": lowest_tax_summary.get("name"),
        "lowest_tax_value": lowest_tax_summary.get("lifetime_tax"),
        "highest_wealth_strategy": highest_wealth_summary.get("name"),
        "highest_wealth_value": highest_wealth_summary.get("final_wealth"),
        "all_summaries": summaries,
    }


def income_profile_by_age(
    results: List[Dict[str, Any]],
) -> List[Tuple[int, float]]:
    """Extract a simple (age, net_cash_flow) profile from simulation results.

    Student C: implement how to transform the raw results into a sequence
    of (age, net_cash_flow) tuples.
    """
    profile: List[Tuple[int, float]] = []

    for r in results:
        age = int(r.get("age"))
        net_cash_flow = float(r.get("net_cash_flow", 0.0))
        profile.append((age, net_cash_flow))

    return profile
