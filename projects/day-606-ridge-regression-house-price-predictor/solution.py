# Day 606 | 2026-08-29 | Ridge Regression House Price Predictor
# Category: ML

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

np.random.seed(21)
n = 600
area   = np.random.randint(500, 4000, n)
rooms  = np.random.randint(1, 7, n)
age    = np.random.randint(0, 40, n)
garage = np.random.choice([0,1], n)
price  = area*150 + rooms*8000 - age*500 + garage*15000 + np.random.normal(0, 15000, n)

df = pd.DataFrame({"area":area,"rooms":rooms,"age":age,"garage":garage,"price":price})
df["area_per_room"] = df["area"] / df["rooms"]
df["log_area"] = np.log(df["area"])

X = df.drop("price", axis=1)
y = df["price"]
X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

for name, model in [("Linear Regression", LinearRegression()), ("Ridge(alpha=10)", Ridge(alpha=10))]:
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2   = r2_score(y_test, preds)
    print(f"{name:25s} | RMSE: ${rmse:>10,.0f} | R2: {r2:.3f}")
