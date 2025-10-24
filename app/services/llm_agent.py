import os
import json
from typing import Dict, Any

# Placeholder: follow "fail-safe" principle. Return minimal overlay.
# In production, call OpenAI with compact profiles + masked samples.
def review(profile: Dict[str, Any], masked_sample):
    # Compact overlay example matching the spec schema surface
    return {
        "anomalies": [],
        "global_rules": [
            {"column": "customer_email", "rule": "lowercase+trim"},
            {"column": "order_date", "rule": "parse('%Y-%m-%d')"}
        ],
        "missing_values": {"discount": "fill_zero_if_price>0"},
        "confidence": 0.6
    }
