# Day 492 | 2026-05-07 | RFM Customer Segmentation
# Category: ML

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(7)
n = 300
df = pd.DataFrame({
    "recency":   np.random.randint(1, 365, n),
    "frequency": np.random.randint(1, 50, n),
    "monetary":  np.random.uniform(10, 5000, n),
})

X = StandardScaler().fit_transform(df)
df["segment"] = KMeans(n_clusters=4, random_state=42, n_init=10).fit_predict(X)

print("=== RFM Customer Segmentation ===")
summary = df.groupby("segment").agg(
    count=("segment","size"),
    avg_recency=("recency","mean"),
    avg_frequency=("frequency","mean"),
    avg_monetary=("monetary","mean"),
).round(1)
print(summary)
