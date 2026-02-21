import pandas as pd

def compute_momentum_score(prices: pd.DataFrame, lookback_days: int
) -> pd.DataFrame:
    shifted = prices.apply(
        lambda col: [
            col.asof(date - pd.DateOffset(days=lookback_days)) for date in col.index
        ]
    )
    shifted = pd.DataFrame(shifted, index=prices.index, columns=prices.columns)
    return (prices / shifted) - 1
    # return (prices / prices.shift(lookback_days)) - 1


def get_rebalance_dates(df: pd.DataFrame):
    return df.groupby(df.index.to_period('M')).apply(lambda x: x.index.min())


def get_top2_assets(scores: pd.DataFrame, rebalance_dates) -> dict:
    holdings = {}
    for date in rebalance_dates:
        row = scores.loc[date].dropna()
        top2 = row.nlargest(2).index.tolist()
        holdings[date] = top2
    return holdings


def compute_portfolio_returns(
    daily_returns: pd.DataFrame, holdings: dict, rebalance_dates
) -> pd.Series:
    portfolio_returns = pd.Series(index=daily_returns.index, dtype=float)
    sorted_dates = sorted(holdings.keys())

    for i, reb_date in enumerate(sorted_dates):
        next_reb = sorted_dates[i + 1] if i + 1 < len(sorted_dates) else daily_returns.index[-1]
        assets = holdings[reb_date]

        if not assets:
            portfolio_returns[reb_date:next_reb] = 0.0
            continue

        period_mask = (daily_returns.index >= reb_date) & (daily_returns.index < next_reb)
        period_returns = daily_returns.loc[period_mask, assets]
        portfolio_returns[period_mask] = period_returns.mean(axis=1)

    return portfolio_returns.dropna()


def compute_strategy(df: pd.DataFrame, lookback_days: int):
    """
    Master function. Returns (portfolio_returns, cumulative_value).
    """
    daily_returns = df.pct_change()
    daily_returns.dropna(how='all', inplace=True)

    scores = compute_momentum_score(df, lookback_days)
    rebalance_dates = get_rebalance_dates(df)
    holdings = get_top2_assets(scores, rebalance_dates)

    port_returns = compute_portfolio_returns(daily_returns, holdings, rebalance_dates)
    cumulative = (1 + port_returns).cumprod()

    return port_returns, cumulative
