import pandas as pd
from rich.console import Console

def load_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        df.ffill(inplace=True)
        return df
    
    except Exception as e:
        console = Console()
        console.print(f"[red]Error loading data from '{filepath}': {e}[/red]")
        return pd.DataFrame()  # Return empty DataFrame on error
    ...
