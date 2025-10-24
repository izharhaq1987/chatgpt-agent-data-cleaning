import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    # Robust load with encoding sniff could be added here
    return pd.read_csv(path)
