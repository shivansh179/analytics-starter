import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw" / "customers.csv"
PROC = BASE / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)

# Basic cleaning
df = df.dropna()
df = df[df["income_inr"] > 0]
df["is_premium"] = df["is_premium"].astype(int)
df["churn"] = df["churn"].astype(int)

# Feature engineering
df["spend_per_visit"] = np.where(df["visits_per_month"] > 0,
                                 df["avg_basket_inr"],
                                 0)
df["income_lakh"] = df["income_inr"] / 100000.0
df["tenure_years"] = df["tenure_months"] / 12.0

# Simple segmentation
df["age_band"] = pd.cut(df["age"], bins=[0,25,35,50,100],
                        labels=["<=25","26-35","36-50","50+"], include_lowest=True)
df["income_band"] = pd.cut(df["income_inr"],
                           bins=[0,400000,800000,1200000,10_000_000],
                           labels=["<4L","4-8L","8-12L",">12L"],
                           include_lowest=True)

# Save feature table for ML/BI
out = df.copy()
out.to_csv(PROC / "feature_table.csv", index=False)

# Aggregates for BI
agg = (
    df.groupby(["age_band","income_band","is_premium"], dropna=False)
      .agg(customers=("customer_id","count"),
           avg_visits=("visits_per_month","mean"),
           avg_basket=("avg_basket_inr","mean"),
           churn_rate=("churn","mean"))
      .reset_index()
)
agg.to_csv(PROC / "aggregates_pandas.csv", index=False)

print("Wrote:",
      (PROC / "feature_table.csv").as_posix(),
      (PROC / "aggregates_pandas.csv").as_posix())
