# Day 458 | 2026-04-03 | Random Forest Feature Importance
# Category: ML

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(99)
n = 700
df = pd.DataFrame({
    "age":            np.random.randint(18, 65, n),
    "income":         np.random.uniform(20000, 120000, n),
    "credit_score":   np.random.randint(300, 850, n),
    "debt_ratio":     np.random.uniform(0, 1, n),
    "num_products":   np.random.randint(1, 6, n),
    "years_customer": np.random.randint(0, 20, n),
})
df["default"] = ((df["debt_ratio"] > 0.6) & (df["credit_score"] < 600)).astype(int)

X = df.drop("default", axis=1)
y = df["default"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

print(f"=== Random Forest Loan Default ===")
print(f"Accuracy: {accuracy_score(y_test, rf.predict(X_test)):.3f}")

fi = pd.Series(rf.feature_importances_, index=X.columns).sort_values()
print("\nFeature Importances:")
print(fi.round(4))

fi.plot(kind="barh", color="steelblue", figsize=(8,4), title="Feature Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=120)
print("Plot saved -> feature_importance.png")
