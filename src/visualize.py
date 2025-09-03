import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"
OUT = BASE / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

ft = pd.read_csv(PROC / "feature_table.csv")

# Chart 1: churn rate by age band
cr_by_age = ft.groupby("age_band")["churn"].mean()
plt.figure()
cr_by_age.plot(kind="bar", title="Churn Rate by Age Band")
plt.ylabel("Churn Rate")
plt.tight_layout()
plt.savefig(OUT / "churn_by_age_band.png")
plt.close()

# Chart 2: average basket by premium vs non-premium
ab = ft.groupby("is_premium")["avg_basket_inr"].mean()
ab.index = ["Non-Premium","Premium"]
plt.figure()
ab.plot(kind="bar", title="Average Basket by Membership Type")
plt.ylabel("Average Basket (INR)")
plt.tight_layout()
plt.savefig(OUT / "avg_basket_by_membership.png")
plt.close()

print("Charts saved to outputs/*.png")
