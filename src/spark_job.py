from pyspark.sql import SparkSession, functions as F, types as T
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"
RAW = BASE / "data" / "raw" / "customers.csv"
PROC.mkdir(parents=True, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("AnalyticsSparkJob")
    .master("local[*]")
    .getOrCreate()
)

df = spark.read.option("header", True).option("inferSchema", True).csv(RAW.as_posix())

# Spark transforms mirroring part of pandas ETL
df = df.dropna()

df = df.withColumn("spend_per_visit",
                   F.when(F.col("visits_per_month") > 0, F.col("avg_basket_inr"))
                    .otherwise(F.lit(0)))

# age bands
df = df.withColumn(
    "age_band",
    F.when(F.col("age") <= 25, F.lit("<=25"))
     .when((F.col("age") > 25) & (F.col("age") <= 35), F.lit("26-35"))
     .when((F.col("age") > 35) & (F.col("age") <= 50), F.lit("36-50"))
     .otherwise(F.lit("50+"))
)

# income bands
df = df.withColumn(
    "income_band",
    F.when(F.col("income_inr") <= 400000, F.lit("<4L"))
     .when((F.col("income_inr") > 400000) & (F.col("income_inr") <= 800000), F.lit("4-8L"))
     .when((F.col("income_inr") > 800000) & (F.col("income_inr") <= 1200000), F.lit("8-12L"))
     .otherwise(F.lit(">12L"))
)

agg = (
    df.groupBy("age_band","income_band","is_premium")
      .agg(F.count("*").alias("customers"),
           F.avg("visits_per_month").alias("avg_visits"),
           F.avg("avg_basket_inr").alias("avg_basket"),
           F.avg("churn").alias("churn_rate"))
)

out_path = (PROC / "aggregates_spark.csv").as_posix()
agg.coalesce(1).write.mode("overwrite").option("header", True).csv(PROC.as_posix() + "/aggregates_spark_tmp")

# Move the single part file to a nice name
import glob, os, shutil
tmp_dir = PROC.as_posix() + "/aggregates_spark_tmp"
part_files = glob.glob(tmp_dir + "/part-*.csv")
if part_files:
    shutil.move(part_files[0], out_path)
shutil.rmtree(tmp_dir, ignore_errors=True)

print("Wrote:", out_path)
spark.stop()
