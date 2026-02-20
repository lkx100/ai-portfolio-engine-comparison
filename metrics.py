import pandas as pd
from typing import Dict

def compute_metrics(portfolio_returns: pd.Series, cumulative_value: pd.Series) -> Dict[str, float]:
    total_return = cumulative_value.iloc[-1] - 1
    n_years = len(portfolio_returns) / 252
    cagr = (cumulative_value.iloc[-1]) ** (1 / n_years) - 1
    rolling_peak = cumulative_value.expanding().max()
    drawdown = (cumulative_value - rolling_peak) / rolling_peak
    max_drawdown = drawdown.min()
    volatility = portfolio_returns.std() * (252 ** 0.5)

    return {
        "total_return": round(float(total_return), 4),
        "cagr": round(float(cagr), 4),
        "max_drawdown": round(float(max_drawdown), 4),
        "volatility": round(float(volatility), 4)
    }
    ...