import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        df.ffill(inplace=True)
        return df
    
    except Exception as e:
        print(e)
        return pd.DataFrame()  # Return empty DataFrame on error
    ...
