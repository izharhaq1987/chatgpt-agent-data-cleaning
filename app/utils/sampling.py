import pandas as pd

def make_sample(df: pd.DataFrame, prof: dict, n:int=25) -> pd.DataFrame:
    # Simple stratified-ish: head, tail, and random
    parts = [df.head(5), df.tail(5)]
    if len(df) > 10:
        parts.append(df.sample(min(n, max(0, len(df)-10)), random_state=42))
    return pd.concat(parts).drop_duplicates().head(n)
