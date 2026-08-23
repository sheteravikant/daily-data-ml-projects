# Day 600 | 2026-08-23 | Customer Churn Mini-Model
# Category: ML

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 500
df = pd.DataFrame({
    "tenure":          np.random.randint(1, 72, n),
    "monthly_charges": np.random.uniform(20, 120, n),
    "num_services":    np.random.randint(1, 8, n),
    "support_calls":   np.random.randint(0, 10, n),
    "churn":           np.random.choice([0, 1], n, p=[0.73, 0.27]),
})

X = df.drop("churn", axis=1)
y = df["churn"]
X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("=== Customer Churn Mini-Model ===")
print(classification_report(y_test, y_pred))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.3f}")

importance = pd.Series(model.coef_[0], index=X.columns).sort_values(key=abs, ascending=False)
print("\nFeature Importance:")
print(importance)
