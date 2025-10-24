import pandas as pd
import hashlib

MASK_COLS = {"customer_email"}

def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]

def mask_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in df.columns:
        if c in MASK_COLS:
            out[c] = out[c].astype(str).apply(lambda x: _hash(x) if x and x != "nan" else x)
    return out
