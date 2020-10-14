__all__ = [
    "cointegration",
    "signal_generation",
    "plot",
    "portfolio",
    "stats",
    "mdd",
    "omega",
    "sortino",
    "profit",
]

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("numpy", "pandas", "statsmodels", "yfinance", "scipy", "sklearn")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

import matplotlib.pyplot as plt
import yfinance as yf
import scipy.integrate
import scipy.stats

from pairs_trading.cointegration import cointegration
from pairs_trading.EG_method import EG_method
from pairs_trading.signal_generation import signal_generation
from pairs_trading.plot import plot
from pairs_trading.portfolio import portfolio
from pairs_trading.stats import stats
from pairs_trading.mdd import mdd
from pairs_trading.omega import omega
from pairs_trading.sortino import sortino
from pairs_trading.profit import profit


# TODO: Add init docstring
