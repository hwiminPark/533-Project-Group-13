The strategies subpackage defines three withdrawal strategies for retirement planning and provides tools to analyze their outcomes.

policies.py implements three strategies: taxable-first, RRSP-first, and a 4%-rule smoothing strategy using TFSA.

analysis.py summarizes simulation results (lifetime tax, final wealth, ruin age) and compares strategies.

Functions are exported through __init__.py for easy access.
This subpackage was implemented by Po-Kai Tseng.