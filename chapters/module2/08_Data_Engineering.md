# Chapter 8: Data Engineering

## ETL with PySpark

Databricks is the premier platform for Extract, Transform, Load (ETL) operations. PySpark enables processing of massive datasets efficiently.

```python
# Basic ETL flow
# Extract
raw_df = spark.read.json("/mnt/raw_data/events.json")

# Transform
from pyspark.sql.functions import col, to_date
clean_df = raw_df.filter(col("status") == "success") \
                 .withColumn("event_date", to_date(col("timestamp")))

# Load
clean_df.write.format("delta").mode("append").save("/mnt/silver/events")
```

## Delta Lake Operations (MERGE, UPSERT, CDC)

Delta Lake supports advanced DML operations like `MERGE` (Upsert), `UPDATE`, and `DELETE`.

```sql
-- SQL MERGE Example
MERGE INTO target_table t
USING source_table s
ON t.id = s.id
WHEN MATCHED THEN
  UPDATE SET t.value = s.value
WHEN NOT MATCHED THEN
  INSERT (id, value) VALUES (s.id, s.value)
```

```python
# PySpark MERGE Example using DeltaTable API
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "/mnt/silver/events")
updatesDF = spark.read.parquet("/mnt/landing/updates")

deltaTable.alias("t").merge(
    updatesDF.alias("s"),
    "t.id = s.id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

## Data Ingestion: Auto Loader and Delta Live Tables

**Auto Loader** incrementally and efficiently processes new data files as they arrive in cloud storage.
```python
# Auto Loader Example
df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .load("/mnt/landing/json_data/")

df.writeStream.format("delta") \
    .option("checkpointLocation", "/mnt/checkpoints/events") \
    .start("/mnt/silver/events")
```

**Delta Live Tables (DLT)** simplifies the creation and management of data pipelines by treating them as a declarative DAG of tables.
```python
import dlt

@dlt.table
def cleaned_events():
    return (
        spark.read.table("live.raw_events")
        .filter("status = 'success'")
    )
```

## Using Databricks SQL for Data Warehousing

Databricks SQL provides a dedicated, optimized compute environment (SQL Warehouses) for running SQL queries, enabling analysts to use BI tools without managing Spark clusters.
