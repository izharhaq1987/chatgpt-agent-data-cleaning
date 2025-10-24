import pandas as pd
import numpy as np
import re

def _is_email(x: str) -> bool:
    if not isinstance(x, str): return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", x) is not None

def run_all(df: pd.DataFrame, prof: dict) -> dict:
    findings = []
    # Example deterministic rules
    if "unit_price" in df.columns:
        idx = df["unit_price"] < 0
        for i in df[idx].index:
            findings.append({"row_index": int(i), "column": "unit_price", "issue": "negative_value", "rule": "range>=0"})
    if "discount" in df.columns:
        idx = (df["discount"].astype("float64", errors="ignore") > 1)
        for i in df[idx.fillna(False)].index:
            findings.append({"row_index": int(i), "column": "discount", "issue": ">1", "rule": "0<=discount<=1"})
    if "customer_email" in df.columns:
        for i, v in df["customer_email"].items():
            if pd.isna(v): 
                findings.append({"row_index": int(i), "column": "customer_email", "issue": "missing_email", "rule": "required"})
            elif not _is_email(str(v)):
                findings.append({"row_index": int(i), "column": "customer_email", "issue": "invalid_email", "rule": "regex"})
    # Naive country typo hint
    if "country" in df.columns:
        for i, v in df["country"].items():
            if isinstance(v, str) and "Untied" in v:
                findings.append({"row_index": int(i), "column": "country", "issue": "typo", "suggest_fix": "replace with 'United States'"})
    summary = {"anomalies": len(findings)}
    return {"summary": summary, "findings": findings, "suggested_fixes": [f for f in findings if "suggest_fix" in f]}

def merge_reports(base: dict, overlay: dict) -> dict:
    if not overlay: return base
    merged = {
        "summary": base.get("summary", {}),
        "findings": base.get("findings", []) + overlay.get("anomalies", []),
        "suggested_fixes": base.get("suggested_fixes", []) + overlay.get("global_rules", [])
    }
    return merged

