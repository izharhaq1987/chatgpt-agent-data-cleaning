import pandas as pd
import numpy as np

def _col_stats(s: pd.Series):
    stats = {
        "dtype": str(s.dtype),
        "null_pct": float(s.isna().mean()),
        "unique": int(s.nunique(dropna=True))
    }
    if pd.api.types.is_numeric_dtype(s):
        stats.update({
            "min": float(np.nanmin(s)) if s.notna().any() else None,
            "max": float(np.nanmax(s)) if s.notna().any() else None,
            "mean": float(np.nanmean(s)) if s.notna().any() else None,
            "std": float(np.nanstd(s)) if s.notna().any() else None,
        })
    return stats

def profile_df(df: pd.DataFrame) -> dict:
    per_col = {c: _col_stats(df[c]) for c in df.columns}
    dup_rows = int(df.duplicated().sum())
    return {"rows": int(len(df)), "columns": list(df.columns), "per_column": per_col, "duplicates": dup_rows}
