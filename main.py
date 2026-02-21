import pandas as pd
from data_loader import load_data
from strategy_engine import compute_strategy
from metrics import compute_metrics
from ai_analysis import analyze_strategies

import sys
import json
from rich.console import Console
from rich.markdown import Markdown

def main():

    df: pd.DataFrame = load_data("data/assets.csv")
    console = Console()

    if df.empty:
        sys.exit(0)

    port_30, cum_30 = compute_strategy(df, 30)
    port_90, cum_90 = compute_strategy(df, 90)

    metrics_30 = compute_metrics(port_30, cum_30)
    metrics_90 = compute_metrics(port_90, cum_90)

    results = {
        "strategy_30_day": metrics_30,
        "strategy_90_day": metrics_90
    }
    print("\n\n")
    console.print(Markdown("# Performance Metrics:"))
    console.print(json.dumps(results, indent=2))

    print("\n\n")
    console.print(Markdown("\n\n# Performing AI Analysis:"))
    analysis = analyze_strategies(results)
    console.print(Markdown(analysis))

if __name__ == "__main__":
    main()