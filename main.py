import pandas as pd
from data_loader import load_data
from strategy_engine import compute_strategy
from metrics import compute_metrics
from ai_analysis import analyze_strategies
import json

def main():

    df: pd.DataFrame = load_data("data/assets.csv")

    if df.empty:
        print("Failed to load data from 'data/assets.csv'")
        return

    port_30, cum_30 = compute_strategy(df, 30)
    port_90, cum_90 = compute_strategy(df, 90)

    metrics_30 = compute_metrics(port_30, cum_30)
    metrics_90 = compute_metrics(port_90, cum_90)

    results = {
        "strategy_30_day": metrics_30,
        "strategy_90_day": metrics_90
    }

    print("\n\nPerformance Metrics:\n")
    print(json.dumps(results, indent=2))

    print("\n\nPerforming AI Analysis:\n")
    analysis = analyze_strategies(results)
    print(analysis)

if __name__ == "__main__":
    main()