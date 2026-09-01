# Day 609 | 2026-09-01 | Time-Series Trend Decomposition
# Category: Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

np.random.seed(11)
periods = 104
time     = np.arange(periods)
series   = 200 + 1.5*time + 30*np.sin(2*np.pi*time/52) + np.random.normal(0, 10, periods)
dates    = pd.date_range("2023-01-01", periods=periods, freq="W")
ts       = pd.Series(series, index=dates, name="weekly_revenue")

result = seasonal_decompose(ts, model="additive", period=52)

print("=== Time-Series Decomposition ===")
print(f"Mean trend      : {result.trend.dropna().mean():.2f}")
print(f"Seasonal range  : {result.seasonal.max() - result.seasonal.min():.2f}")
print(f"Residual std    : {result.resid.dropna().std():.2f}")

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
for ax, data, label in zip(axes, [ts, result.trend, result.seasonal, result.resid],
                            ["Observed","Trend","Seasonal","Residual"]):
    ax.plot(data, color="steelblue"); ax.set_ylabel(label); ax.grid(alpha=0.3)
plt.suptitle("Weekly Revenue Decomposition", fontsize=13)
plt.tight_layout()
plt.savefig("decomposition.png", dpi=120)
print("Plot saved -> decomposition.png")
