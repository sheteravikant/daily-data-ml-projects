# Day 603 | 2026-08-26 | EDA on E-Commerce Sales
# Category: Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)
n = 1000
categories = ["Electronics","Clothing","Books","Home","Sports"]
df = pd.DataFrame({
    "category": np.random.choice(categories, n),
    "quantity": np.random.randint(1, 10, n),
    "price":    np.random.uniform(5, 500, n).round(2),
    "month":    np.random.randint(1, 13, n),
    "rating":   np.random.uniform(1, 5, n).round(1),
})
df["revenue"] = (df["quantity"] * df["price"]).round(2)

print("=== E-Commerce EDA ===")
print(df[["quantity","price","revenue","rating"]].describe().round(2))

cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
print("\nRevenue by Category:")
print(cat_rev.round(2))

monthly = df.groupby("month")["revenue"].sum()
print(f"\nPeak month: {monthly.idxmax()} (${monthly.max():,.0f})")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
cat_rev.plot(kind="bar", ax=axes[0], color="steelblue", title="Revenue by Category")
monthly.plot(kind="line", ax=axes[1], marker="o", color="darkorange", title="Monthly Revenue Trend")
plt.tight_layout()
plt.savefig("eda_plots.png", dpi=120)
print("Plot saved -> eda_plots.png")
