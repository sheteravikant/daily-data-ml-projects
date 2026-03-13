"""
Daily Project Generator — tailored to Ravikant's resume skills
Generates a new mini-project every day covering ML, Data Analysis,
NLP, GCP/BigQuery concepts, and BI themes.
"""

import os
import json
import datetime

TODAY = datetime.date.today().isoformat()
DAY_NUMBER = (datetime.date.today() - datetime.date(2025, 1, 1)).days + 1

PROJECTS = [
    {
        "category": "ML",
        "title": "Customer Churn Mini-Model",
        "description": "Train a logistic regression model on synthetic telecom data to predict churn.",
        "skills": ["scikit-learn", "pandas", "classification"],
        "code": '''import pandas as pd
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
print("\\nFeature Importance:")
print(importance)
''',
    },
    {
        "category": "ML",
        "title": "Anomaly Detection on Sales Data",
        "description": "Use Isolation Forest to detect revenue anomalies in synthetic daily sales.",
        "skills": ["scikit-learn", "anomaly-detection", "pandas"],
        "code": '''import pandas as pd
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
print("\\nAnomalous days:")
print(df[df["is_anomaly"]][["date", "sales"]].to_string(index=False))
''',
    },
    {
        "category": "ML",
        "title": "RFM Customer Segmentation",
        "description": "Apply KMeans clustering to segment customers by Recency, Frequency, Monetary value.",
        "skills": ["scikit-learn", "clustering", "pandas"],
        "code": '''import pandas as pd
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
''',
    },
    {
        "category": "Data Analysis",
        "title": "EDA on E-Commerce Sales",
        "description": "Exploratory Data Analysis on a synthetic e-commerce dataset with summary stats and trends.",
        "skills": ["pandas", "matplotlib", "EDA"],
        "code": '''import pandas as pd
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
print("\\nRevenue by Category:")
print(cat_rev.round(2))

monthly = df.groupby("month")["revenue"].sum()
print(f"\\nPeak month: {monthly.idxmax()} (${monthly.max():,.0f})")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
cat_rev.plot(kind="bar", ax=axes[0], color="steelblue", title="Revenue by Category")
monthly.plot(kind="line", ax=axes[1], marker="o", color="darkorange", title="Monthly Revenue Trend")
plt.tight_layout()
plt.savefig("eda_plots.png", dpi=120)
print("Plot saved -> eda_plots.png")
''',
    },
    {
        "category": "Data Analysis",
        "title": "Data Quality Checker",
        "description": "Build a reusable data quality audit tool that flags nulls, duplicates, and outliers.",
        "skills": ["pandas", "numpy", "data-governance"],
        "code": '''import pandas as pd
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
print(f"\\nHealth: {(report['status']=='OK').sum()}/{len(report)} columns OK")
''',
    },
    {
        "category": "NLP",
        "title": "TF-IDF Resume Keyword Extractor",
        "description": "Extract top keywords from job descriptions using TF-IDF cosine similarity.",
        "skills": ["NLP", "scikit-learn", "TF-IDF"],
        "code": '''from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

jds = [
    "data analyst Python SQL Power BI Tableau ETL pipeline data governance",
    "machine learning engineer scikit-learn XGBoost deep learning NLP model deployment AWS GCP",
    "BI specialist Tableau Power BI Looker dashboard KPI tracking stakeholder reporting",
    "data scientist pandas numpy statistical modelling clustering classification regression big data",
    "cloud data engineer BigQuery Apache Spark GCP Docker data warehousing pipeline automation",
]

vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=50)
tfidf_matrix = vectorizer.fit_transform(jds)
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

print("=== TF-IDF Keyword Extraction ===\\n")
for i, jd in enumerate(jds):
    top = df_tfidf.iloc[i].sort_values(ascending=False).head(5)
    print(f"JD {i+1} top keywords: {', '.join(top.index.tolist())}")

print("\\nGlobal top 10 keywords:")
print(df_tfidf.sum().sort_values(ascending=False).head(10).round(3))
''',
    },
    {
        "category": "ML",
        "title": "Ridge Regression House Price Predictor",
        "description": "Predict house prices with feature engineering and Ridge regression baseline.",
        "skills": ["scikit-learn", "regression", "feature-engineering"],
        "code": '''import numpy as np
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
''',
    },
    {
        "category": "Data Analysis",
        "title": "SQL Window Functions with Pandas",
        "description": "Simulate SQL window functions (RANK, cumulative SUM, moving average) using pandas.",
        "skills": ["pandas", "SQL", "analytics"],
        "code": '''import pandas as pd
import numpy as np

np.random.seed(5)
n = 300
df = pd.DataFrame({
    "rep":     np.random.choice(["Alice","Bob","Carol","Dave","Eve"], n),
    "region":  np.random.choice(["North","South","East","West"], n),
    "month":   np.random.randint(1, 13, n),
    "revenue": np.random.uniform(100, 5000, n).round(2),
})

print("=== SQL Analytics via Pandas ===\\n")

print("1. Revenue by region (GROUP BY):")
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False).round(2))

print("\\n2. Top 3 reps by revenue (RANK):")
rep_rev = df.groupby("rep")["revenue"].sum().reset_index()
rep_rev["rank"] = rep_rev["revenue"].rank(ascending=False).astype(int)
print(rep_rev.sort_values("rank").head(3).to_string(index=False))

print("\\n3. Running monthly total + 3-month moving average:")
monthly = df.groupby("month")["revenue"].sum().reset_index()
monthly["cumulative"] = monthly["revenue"].cumsum().round(2)
monthly["moving_avg_3m"] = monthly["revenue"].rolling(3).mean().round(2)
print(monthly.to_string(index=False))
''',
    },
    {
        "category": "ML",
        "title": "Random Forest Feature Importance",
        "description": "Train a Random Forest on loan default data and visualise feature importances.",
        "skills": ["scikit-learn", "random-forest", "feature-importance"],
        "code": '''import pandas as pd
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
print("\\nFeature Importances:")
print(fi.round(4))

fi.plot(kind="barh", color="steelblue", figsize=(8,4), title="Feature Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=120)
print("Plot saved -> feature_importance.png")
''',
    },
    {
        "category": "Data Analysis",
        "title": "Time-Series Trend Decomposition",
        "description": "Decompose a synthetic time-series into trend, seasonality, and residual components.",
        "skills": ["pandas", "statsmodels", "time-series"],
        "code": '''import pandas as pd
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
''',
    },
]


def pick_project(day_number):
    return PROJECTS[day_number % len(PROJECTS)]


def create_readme(project, date, day):
    return f"""# Day {day} — {project['title']}

**Date:** {date}  
**Category:** {project['category']}  
**Skills practiced:** {', '.join(project['skills'])}

## Overview
{project['description']}

## How to run
```bash
pip install -r requirements.txt
python solution.py
```

## What you'll learn
- Hands-on with: {', '.join(project['skills'])}
- Applied to a realistic mini-dataset
- Part of a daily portfolio-building streak

---
*Auto-generated as part of Ravikant's daily Data/ML project system.*
"""


def create_requirements(project):
    base = ["pandas", "numpy", "matplotlib"]
    skill_to_pkg = {"scikit-learn": "scikit-learn", "statsmodels": "statsmodels",
                    "NLP": "scikit-learn", "TF-IDF": "scikit-learn"}
    deps = set(base)
    for s in project["skills"]:
        if s in skill_to_pkg:
            deps.add(skill_to_pkg[s])
    return "\n".join(sorted(deps)) + "\n"


def main():
    project = pick_project(DAY_NUMBER)
    slug    = project['title'].lower().replace(' ', '-').replace('/', '-')
    folder  = f"projects/day-{DAY_NUMBER:03d}-{slug}"

    os.makedirs(folder, exist_ok=True)

    with open(f"{folder}/solution.py", "w") as f:
        f.write(f"# Day {DAY_NUMBER} | {TODAY} | {project['title']}\n")
        f.write(f"# Category: {project['category']}\n\n")
        f.write(project["code"].strip() + "\n")

    with open(f"{folder}/README.md", "w") as f:
        f.write(create_readme(project, TODAY, DAY_NUMBER))

    with open(f"{folder}/requirements.txt", "w") as f:
        f.write(create_requirements(project))

    log_path = "projects/LOG.md"
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("# Daily Project Log\n\n| Day | Date | Category | Project |\n|-----|------|----------|---------|\n")

    with open(log_path, "a") as f:
        f.write(f"| {DAY_NUMBER:>3} | {TODAY} | {project['category']:<15} | [{project['title']}]({folder}/README.md) |\n")

    print(json.dumps({"day": DAY_NUMBER, "date": TODAY,
                      "title": project["title"], "category": project["category"],
                      "folder": folder}, indent=2))


if __name__ == "__main__":
    main()
