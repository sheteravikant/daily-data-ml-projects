# Day 611 | 2026-09-03 | Anomaly Detection on Sales Data
# Category: ML

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

np.random.seed(0)
dates = pd.date_range("2024-01-01", periods=120, freq="D")
sales = np.random.normal(loc=5000, scale=400, size=120)
sales[[10, 45, 90, 110]] = [12000, 300, 11500, 200]

df = pd.DataFrame({"date": dates, "sales": sales})
df["anomaly"] = IsolationForest(contamination=0.05, random_state=42).fit_predict(df[["sales"]])
df["is_anomaly"] = df["anomaly"] == -1

print("=== Anomaly Detection on Sales Data ===")
print(f"Total records  : {len(df)}")
print(f"Anomalies found: {df['is_anomaly'].sum()}")
print("\nAnomalous days:")
print(df[df["is_anomaly"]][["date", "sales"]].to_string(index=False))
