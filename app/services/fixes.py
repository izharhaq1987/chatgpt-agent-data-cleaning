import pandas as pd

def apply_safe(df: pd.DataFrame, report: dict) -> pd.DataFrame:
    out = df.copy()
    # Safe transforms only
    for col in out.columns:
        if out[col].dtype == "object":
            out[col] = out[col].astype(str).str.strip()
    if "customer_email" in out.columns:
        out["customer_email"] = out["customer_email"].astype(str).str.strip().str.lower()
    if "discount" in out.columns:
        # clip to [0,1] where numeric
        out["discount"] = pd.to_numeric(out["discount"], errors="coerce").clip(lower=0, upper=1)
    if "unit_price" in out.columns:
        out["unit_price"] = pd.to_numeric(out["unit_price"], errors="coerce")
    return out
