import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import json

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"
MODELS = BASE / "models"
OUT = BASE / "outputs"
MODELS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

ft_path = PROC / "feature_table.csv"
if not ft_path.exists():
    raise SystemExit("Run etl_pandas.py first to create feature_table.csv")

df = pd.read_csv(ft_path)

features = ["age","income_inr","visits_per_month","avg_basket_inr",
            "tenure_months","is_premium","spend_per_visit"]
X = df[features]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline([
    ("scaler", StandardScaler(with_mean=False)),  # with_mean=False to be safe if sparse in future
    ("clf", LogisticRegression(max_iter=1000))
])

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

report = classification_report(y_test, y_pred, output_dict=True)
(OUT / "classification_report.json").write_text(json.dumps(report, indent=2))

joblib.dump(pipe, MODELS / "churn_model.joblib")

meta = {
    "features": features,
    "train_size": len(X_train),
    "test_size": len(X_test),
    "target": "churn",
    "model": "LogisticRegression",
}
(MODELS / "metadata.json").write_text(json.dumps(meta, indent=2))

print("Saved model to models/churn_model.joblib")
print("Classification report -> outputs/classification_report.json")
