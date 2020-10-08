__all__ = ["cointegration", "signal_generation", "plot", "portfolio", "stats", "mdd", "omega", "sortino", "profit"]

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

#TODO: Add init docstring