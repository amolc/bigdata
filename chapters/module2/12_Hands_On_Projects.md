# Chapter 12: Hands-On Projects

This chapter outlines three practical projects to solidify your understanding of Databricks and the Lakehouse architecture.

## 1. Build a Lakehouse (Medallion Architecture)

Implement the Medallion Architecture (Bronze, Silver, Gold):
1. **Bronze**: Ingest raw JSON logs using Auto Loader.
2. **Silver**: Cleanse the data, deduplicate, and enforce schema using PySpark, saving as Delta tables.
3. **Gold**: Aggregate the data for business reporting (e.g., daily active users).

```python
# Conceptual Gold Layer Aggregation
gold_df = spark.read.table("silver.user_events") \
    .groupBy("date", "user_id") \
    .count()

gold_df.write.format("delta").mode("overwrite").saveAsTable("gold.daily_user_activity")
```

## 2. ETL for IoT Data

Create a streaming pipeline for IoT sensor data:
- Connect Spark Structured Streaming to an Azure Event Hubs or Kafka topic.
- Use windowing functions to calculate average sensor temperatures per minute.
- Write the streaming aggregates to a Delta table using `MERGE` to update the latest values.

```python
# Conceptual Streaming Aggregation
from pyspark.sql.functions import window, avg

# Read from Kafka/EventHubs
streaming_df = spark.readStream.format("kafka").load()

# Aggregate
aggregated_df = streaming_df \
    .groupBy(window("timestamp", "1 minute"), "sensor_id") \
    .agg(avg("temperature").alias("avg_temp"))

# Write to Delta
aggregated_df.writeStream \
    .format("delta") \
    .outputMode("complete") \
    .option("checkpointLocation", "/mnt/checkpoints/iot") \
    .table("silver.iot_aggregates")
```

## 3. Real-Time Dashboards and ML Apps

- Train a predictive maintenance model on the IoT data using MLflow.
- Deploy the model as an endpoint or apply it in a batch job to flag failing sensors.
- Connect Databricks SQL or Power BI to the resulting Delta table to create a live, real-time dashboard alerting operators of predicted failures.
