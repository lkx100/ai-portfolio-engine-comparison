import pandas as pd

def load_data(filepath: str) -> pd.DataFrame | Exception | None:
    try:
        df = pd.read_csv(filepath, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        df.ffill(inplace=True)
        return df
    
    except Exception as e:
        return e
    ...
