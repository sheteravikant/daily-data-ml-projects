# Day 584 | 2026-08-07 | Data Quality Checker
# Category: Data Analysis

import pandas as pd
import numpy as np

def data_quality_report(df):
    report = []
    for col in df.columns:
        s = df[col]
        null_pct = s.isna().mean() * 100
        dup_count = df.duplicated(subset=[col]).sum()
        outlier_count = 0
        if pd.api.types.is_numeric_dtype(s):
            q1, q3 = s.quantile([0.25, 0.75])
            iqr = q3 - q1
            outlier_count = int(((s < q1-1.5*iqr) | (s > q3+1.5*iqr)).sum())
        report.append({
            "column": col, "dtype": str(s.dtype), "unique": s.nunique(),
            "null_%": round(null_pct, 2), "duplicates": dup_count,
            "outliers": outlier_count,
            "status": "WARN" if null_pct > 5 or outlier_count > 10 else "OK",
        })
    return pd.DataFrame(report)

np.random.seed(3)
n = 200
df = pd.DataFrame({
    "customer_id": list(range(180)) + list(range(20)),
    "age":   np.where(np.random.rand(n) < 0.06, np.nan, np.random.randint(18, 80, n)),
    "spend": np.append(np.random.uniform(10, 1000, 190), [99999]*10),
    "region":np.random.choice(["North","South","East","West"], n),
})

print("=== Data Quality Report ===")
report = data_quality_report(df)
print(report.to_string(index=False))
print(f"\nHealth: {(report['status']=='OK').sum()}/{len(report)} columns OK")
