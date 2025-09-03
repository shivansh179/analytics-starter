# Using the Processed CSVs in Tableau or Power BI

## Files
- `data/processed/feature_table.csv`
- `data/processed/aggregates_pandas.csv`
- `data/processed/aggregates_spark.csv` (after running `spark_job.py`)

## Tableau
1. Open Tableau and choose **Text file** as a data source.
2. Select `feature_table.csv` (you can add joins/unions with other processed files).
3. Drag fields like `age_band`, `income_band`, `is_premium`, `churn` into a sheet.
4. Example visuals:
   - Bar chart: `age_band` vs `AVG(churn)`
   - Heat map: `income_band` by `is_premium` with `AVG(avg_basket_inr)`

## Power BI
1. Open Power BI Desktop → **Get Data** → **Text/CSV**.
2. Import `feature_table.csv` and `aggregates_pandas.csv`.
3. In **Model** view, set data types (e.g., `is_premium` as whole number).
4. Create visuals like:
   - Clustered column chart: `age_band` on Axis, `Average of churn` as Value.
   - Matrix: `income_band` x `is_premium` with `Average of avg_basket_inr`.

> Tip: Refresh the data after rerunning the ETL to pick up new CSVs.
