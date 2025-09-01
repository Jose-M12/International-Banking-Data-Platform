import os
from pyspark.sql import SparkSession, functions as F, Window

project = os.getenv("GCP_PROJECT")
silver_table = f"{project}.silver.silver_transactions"
gold_table = f"{project}.gold.customer_features"

spark = SparkSession.builder.appName("customer_features").getOrCreate()
df = (spark.read.format("bigquery").option("table", silver_table).load())

w7 = Window.partitionBy("customer_id").orderBy(F.col("txn_ts_utc").cast("long")).rangeBetween(-7*86400, 0)
w30 = Window.partitionBy("customer_id").orderBy(F.col("txn_ts_utc").cast("long")).rangeBetween(-30*86400, 0)

features = (df
    .withColumn("txn_count_7d", F.count("*").over(w7))
    .withColumn("sum_usd_30d", F.sum("amount_usd").over(w30))
    .withColumn("avg_ticket_30d", F.avg("amount_usd").over(w30))
    .groupBy("customer_id")
    .agg(F.max("txn_count_7d").alias("rolling_7d_txn_count"),
         F.max("sum_usd_30d").alias("rolling_30d_sum_usd"),
         F.max("avg_ticket_30d").alias("avg_ticket_30d"))
)

(features.write.format("bigquery")
    .option("table", gold_table)
    .mode("overwrite")
    .save())
