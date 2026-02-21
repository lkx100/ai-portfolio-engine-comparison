# Dual Momentum Portfolio Engine with AI Performance Comparison

> A ranking-based portfolio simulation engine that implements two momentum strategies (30-day and 90-day lookback), computes performance metrics, and uses an LLM to compare them.

---

## Project Structure

```
project/
    ├── data/
    │     └── assets.csv
    ├── main.py
    ├── data_loader.py
    ├── strategy_engine.py
    ├── metrics.py
    ├── ai_analysis.py
```

---

## Setup Instructions

### 0. Prerequisites
- `Python` >= 3.10
- `UV` ([install](https://docs.astral.sh/uv/#installation)) package Manager (recommended) or pip
- `Groq API` key (FREE tier available). Place in `.env` variable `GROQ_API_KEY=<placeholder>`.

### 1. Clone the Repo

```bash
git clone https://github.com/lkx100/ai-portfolio-engine-comparison.git
cd ai-portfolio-engine-comparison
```

### 2. Install dependencies

This project uses `uv` for dependency management.

```bash
uv sync

# OR with pip:
python -m venv .venv      # python3 for linux/macOS
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install pandas groq python-dotenv rich
```

### 5. Run

```bash
uv run main.py

# OR with pip:
python main.py
```

---

## Output

Running the project produces two outputs:

**1. Performance Metrics (Output Structure)**
```json
{
    "strategy_30_day": {
        "total_return": ...,
        "cagr": ...,
        "max_drawdown": ...,
        "volatility": ...
    },
    "strategy_90_day": {
        "total_return": ...,
        "cagr": ...,
        "max_drawdown": ...,
        "volatility": ...
    }
}
```

**2. AI analysis** comparing the two strategies, referencing actual numbers.

---

## Design Decisions

### Data Cleaning — Forward Fill over Interpolation

The dataset has ~2–4% missing values per asset, (gaps of 4–5 days only — confirmed via EDA). Used Forward fill (`ffill`) to fill missing values, because the last traded price is the accurate representation of an asset's value on a non-trading day.

### Calendar-Day Lookback over Row Offset

Momentum scores use a calendar-day lookback via `.asof()` + `pd.DateOffset`, not row indexing (`iloc[-30]`). On irregular trading data, 30 rows ≠ 30 calendar days — using row offset would silently shift the lookback window inconsistently across months. Calendar-day lookback is the only correct approach here.

### Rebalance Dates — First Actual Trading Day of Each Month

Rebalance dates are derived by grouping on calendar month and selecting the minimum date per group. `resample('MS')` was rejected because it returns the calendar start of the month (e.g., May 1st), which may not be a trading day. Executing a trade on a non-trading day is not valid.

### Parameterized Strategy Function

Both strategies run through a single `compute_strategy(df, lookback_days)` function. No code duplication. Lookback period is the only variable — all logic (scoring, rebalancing, portfolio construction) is identical.

### Equal Weight Allocation

Portfolio return = `mean(axis=1)` across the top 2 assets, equivalent to a 50/50 split. This is the simplest allocation with no bias toward either asset, and is what the assignment specifies.

---

## AI Prompt Structure

The `ai_analysis.py` module sends a structured two-part prompt to the LLM:

**System message** — sets the model's persona and constraints:
> "You are a quantitative finance analyst who gives precise, numbers-driven analysis."

**User message** — carries the task, with the metrics JSON embedded directly:
```
You are a quantitative finance analyst. Analyze the following portfolio strategy 
performance metrics and provide a concise comparison.

Strategy Results (JSON):
{ ... }

Please address the following:
1. Compare the two strategies on total return and CAGR
2. Highlight risk-return trade-offs
3. Explain what the max drawdown difference implies for an investor
4. Suggest a market condition where each strategy might outperform the other
5. Suggest one concrete improvement to either strategy
```

**Why `temperature=0.3`:** Keeps the model grounded in the provided numbers. Higher temperature increases the risk of fabricated or speculative financial conclusions that aren't supported by the data.

**Model:** `meta-llama/llama-4-scout-17b-16e-instruct` via Groq API. The API key is read exclusively from `os.environ.get("GROQ_API_KEY")`.

---

## Assumptions

- Day gaps in the dataset are non-trading days like weekends/holidays.
- All 6 assets are valid candidates for selection at each rebalance date (no asset-level filters applied).
- The warmup gap in the 90-day strategy (first 3 months have no valid scores) is expected and handled — those months hold no assets and contribute zero returns. Same for the first month of the 30-day strategy.

---