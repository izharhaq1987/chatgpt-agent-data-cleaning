import pandas as pd
from app.services import rules, profiling

def test_negative_price_flag():
    df = pd.DataFrame({"unit_price":[10,-1,0]})
    prof = profiling.profile_df(df)
    res = rules.run_all(df, prof)
    assert any(f["issue"]=="negative_value" for f in res["findings"])
