# Day 567 | 2026-07-21 | SQL Window Functions with Pandas
# Category: Data Analysis

import pandas as pd
import numpy as np

np.random.seed(5)
n = 300
df = pd.DataFrame({
    "rep":     np.random.choice(["Alice","Bob","Carol","Dave","Eve"], n),
    "region":  np.random.choice(["North","South","East","West"], n),
    "month":   np.random.randint(1, 13, n),
    "revenue": np.random.uniform(100, 5000, n).round(2),
})

print("=== SQL Analytics via Pandas ===\n")

print("1. Revenue by region (GROUP BY):")
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False).round(2))

print("\n2. Top 3 reps by revenue (RANK):")
rep_rev = df.groupby("rep")["revenue"].sum().reset_index()
rep_rev["rank"] = rep_rev["revenue"].rank(ascending=False).astype(int)
print(rep_rev.sort_values("rank").head(3).to_string(index=False))

print("\n3. Running monthly total + 3-month moving average:")
monthly = df.groupby("month")["revenue"].sum().reset_index()
monthly["cumulative"] = monthly["revenue"].cumsum().round(2)
monthly["moving_avg_3m"] = monthly["revenue"].rolling(3).mean().round(2)
print(monthly.to_string(index=False))
