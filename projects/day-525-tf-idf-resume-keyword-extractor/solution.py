# Day 525 | 2026-06-09 | TF-IDF Resume Keyword Extractor
# Category: NLP

from sklearn.feature_extraction.text import TfidfVectorizer
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

print("=== TF-IDF Keyword Extraction ===\n")
for i, jd in enumerate(jds):
    top = df_tfidf.iloc[i].sort_values(ascending=False).head(5)
    print(f"JD {i+1} top keywords: {', '.join(top.index.tolist())}")

print("\nGlobal top 10 keywords:")
print(df_tfidf.sum().sort_values(ascending=False).head(10).round(3))
