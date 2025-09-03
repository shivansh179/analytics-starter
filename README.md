
# AI + Analytics Starter (PySpark, Pandas, NumPy, Matplotlib, + ML)

A ready-to-run reference project that includes:
- **PySpark** for distributed transforms (local mode by default)
- **Pandas/NumPy** for fast ETL
- **Matplotlib** for charts
- **Scikit-learn** for a simple ML model (customer churn)
- **Tableau / Power BI** friendly CSV outputs in `data/processed/`

## Quickstart

```bash
# 1) Create and activate a virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run ETL (Pandas)
python src/etl_pandas.py

# 4) Run Spark job (local mode)
python src/spark_job.py

# 5) Train ML model
python src/train_model.py

# 6) Make charts
python src/visualize.py
```

Outputs go to:
- Processed CSVs: `data/processed/`
- Model artifacts: `models/`
- Charts/Reports: `outputs/`

### Tableau / Power BI
- Import `data/processed/feature_table.csv` and `data/processed/aggregates_spark.csv`.
- A starter guide is in `dashboards/bi_instructions.md`.

## Project Layout
```
ai-ml-analytics-starter/
├─ data/
│  ├─ raw/                 # synthetic sample data
│  └─ processed/           # CSV outputs for BI + ML
├─ models/                 # saved model + metadata
├─ outputs/                # charts/figures
├─ src/
│  ├─ etl_pandas.py        # Pandas/NumPy ETL pipeline
│  ├─ spark_job.py         # PySpark transforms (local[*])
│  ├─ train_model.py       # Scikit-learn binary classifier
│  └─ visualize.py         # Matplotlib charts saved as PNG
├─ dashboards/
│  └─ bi_instructions.md   # Tableau/Power BI steps
├─ requirements.txt
└─ README.md
```

## Notes
- PySpark runs in local mode (`master=local[*]`). No Hadoop install required.
- The synthetic dataset is generated under `data/raw/customers.csv`.
- Everything is CPU-friendly and should run in a few seconds on a laptop.
# analytics-starter
# analytics-starter
