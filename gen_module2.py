import os
from pathlib import Path

base_dir = Path('/Users/amolc/2026/databricksdocs')
module2_dir = base_dir / 'chapters' / 'module2'

# Ensure the directory exists
module2_dir.mkdir(parents=True, exist_ok=True)

ch6_content = """# Chapter 6: Introduction to Databricks

## What is Databricks & Lakehouse Architecture

Databricks is a unified analytics platform that leverages the power of Apache Spark. It brings together data engineering, data science, and analytics into a single collaborative workspace.

The core innovation of Databricks is the **Lakehouse Architecture**. A Lakehouse combines the best elements of data lakes (cheap, scalable storage) and data warehouses (ACID transactions, schema enforcement).

```python
# A simple conceptual check in PySpark to verify Databricks runtime
spark.conf.get("spark.databricks.clusterUsageTags.clusterName", "Not on Databricks")
```

## Delta Lake Basics

Delta Lake is an open-source storage layer that brings ACID transactions to Apache Spark and big data workloads. It runs on top of your existing data lake (e.g., ADLS, S3) and is fully compatible with Spark APIs.

```python
# Creating a Delta Table
data = [("Alice", 28), ("Bob", 25)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Write to Delta format
df.write.format("delta").mode("overwrite").save("/tmp/delta-table")

# Read from Delta format
df_delta = spark.read.format("delta").load("/tmp/delta-table")
df_delta.show()
```

## Workspace, Clusters, and UI

The Databricks Workspace is a web-based environment where you manage all your Databricks assets.
- **Workspace**: Organizes notebooks, libraries, and dashboards.
- **Clusters**: The computation resources. You can create *All-Purpose Clusters* for interactive analysis or *Job Clusters* for automated workloads.
- **UI**: The user interface allows you to navigate through Data, Compute, Workflows, and Machine Learning seamlessly.

*(See original architecture diagrams below)*

![image1](../../images/image1.png)  
![image2](../../images/image2.png)
![image3](../../images/image3.png)  
![image4](../../images/image4.png)
![image5](../../images/image5.png)
"""

ch7_content = """# Chapter 7: Core Concepts

## Notebooks (Python, SQL, Scala)

Databricks notebooks allow you to write and execute code interactively. A single notebook can contain multiple languages by using "magic commands" (`%python`, `%sql`, `%scala`, `%r`, `%md`).

```python
# Cell 1 (Default Python)
print("This is Python")

# Cell 2 (SQL Magic)
# %sql
# SELECT * FROM my_table;

# Cell 3 (Markdown Magic)
# %md
# ### This is a Markdown heading!
```

## Cluster Types and Job Scheduling

1. **All-Purpose Clusters**: Used for collaborative, interactive analysis. Terminated manually or via auto-termination.
2. **Job Clusters**: Created by the Databricks job scheduler to run a specific job and terminated immediately after the job finishes, reducing costs.

**Job Scheduling Example (JSON configuration snippet):**
```json
{
  "name": "Daily ETL Job",
  "new_cluster": {
    "spark_version": "12.2.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "num_workers": 4
  },
  "notebook_task": {
    "notebook_path": "/Users/user@domain.com/ETL_Notebook"
  },
  "schedule": {
    "quartz_cron_expression": "0 0 2 * * ?",
    "timezone_id": "UTC"
  }
}
```

## Connecting to Azure Data Sources

Databricks natively integrates with Azure. To access Azure Data Lake Storage (ADLS) Gen2, you configure the Spark session with the storage account credentials or use Azure Active Directory (Azure AD) credential passthrough.

```python
# Connecting to ADLS Gen2 using an Account Key (For dev/test only)
storage_account_name = "myadlsaccount"
storage_account_key = "my_access_key"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_key
)

# Read data from ADLS Gen2
df = spark.read.csv(f"abfss://mycontainer@{storage_account_name}.dfs.core.windows.net/data.csv")
```
"""

ch8_content = """# Chapter 8: Data Engineering

## ETL with PySpark

Databricks is the premier platform for Extract, Transform, Load (ETL) operations. PySpark enables processing of massive datasets efficiently.

```python
# Basic ETL flow
# Extract
raw_df = spark.read.json("/mnt/raw_data/events.json")

# Transform
from pyspark.sql.functions import col, to_date
clean_df = raw_df.filter(col("status") == "success") \\
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
).whenMatchedUpdateAll() \\
 .whenNotMatchedInsertAll() \\
 .execute()
```

## Data Ingestion: Auto Loader and Delta Live Tables

**Auto Loader** incrementally and efficiently processes new data files as they arrive in cloud storage.
```python
# Auto Loader Example
df = spark.readStream.format("cloudFiles") \\
    .option("cloudFiles.format", "json") \\
    .load("/mnt/landing/json_data/")

df.writeStream.format("delta") \\
    .option("checkpointLocation", "/mnt/checkpoints/events") \\
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
"""

ch9_content = """# Chapter 9: Machine Learning

## ML Lifecycle and Model Training

Databricks provides a collaborative environment for the entire Machine Learning lifecycle: data preparation, feature engineering, model training, and deployment.

```python
# Basic Model Training Example
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

# Prepare data
assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
train_data = assembler.transform(df).select("features", "label")

# Train model
rf = RandomForestClassifier(numTrees=10)
model = rf.fit(train_data)
```

## MLflow for Tracking and Tuning

MLflow is deeply integrated into Databricks to track experiments, package code, and deploy models.

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

with mlflow.start_run():
    # Train scikit-learn model
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(X_train, y_train)
    
    # Evaluate
    predictions = rf.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    
    # Log parameters and metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("mse", mse)
    
    # Log the model
    mlflow.sklearn.log_model(rf, "random_forest_model")
```

## Integration with Azure ML

Databricks models tracked in MLflow can be seamlessly deployed to Azure Machine Learning (Azure ML) for serving as REST endpoints.

```python
# Conceptual snippet for Azure ML deployment
import mlflow.azureml

azure_workspace = Workspace.get(name="myworkspace", subscription_id="...", resource_group="...")
mlflow.azureml.deploy(
    model_uri="runs:/<run_id>/random_forest_model",
    workspace=azure_workspace,
    deployment_config=...,
    service_name="my-rf-service"
)
```
"""

ch10_content = """# Chapter 10: Analytics & BI

## Dashboards with Databricks SQL

Databricks SQL allows you to write queries, create visualizations, and assemble them into Dashboards directly within the Databricks Workspace. This provides a lightweight, integrated BI experience.

```sql
-- Example Dashboard Query: Monthly Revenue
SELECT 
  date_trunc('month', order_date) AS order_month,
  SUM(total_amount) AS revenue
FROM silver.orders
GROUP BY 1
ORDER BY 1 DESC;
```

## Power BI and Real-Time Analytics

For enterprise reporting, Databricks connects seamlessly to Power BI via the **Databricks SQL Connector**. 

- **DirectQuery**: Power BI can send queries directly to Databricks SQL Warehouses, ensuring users always see the latest data without importing massive datasets into Power BI.
- **Connection Details**: In Power BI, you connect using the Server Hostname and HTTP Path found in the Databricks SQL Warehouse connection details.

```text
# Example Connection String Format (Under the hood JDBC/ODBC)
jdbc:spark://<server-hostname>:443/default;transportMode=http;ssl=1;httpPath=<http-path>;AuthMech=3;UID=token;PWD=<personal-access-token>
```
"""

ch11_content = """# Chapter 11: Security & Governance

## RBAC and Unity Catalog

Databricks employs Role-Based Access Control (RBAC) for managing permissions on clusters, jobs, and workspace items. 

**Unity Catalog** is the unified governance solution for data and AI on the Lakehouse. It provides centralized access control, auditing, and data discovery across all Databricks workspaces.

```sql
-- Unity Catalog Access Control
-- Granting access to a specific catalog and table
GRANT USE CATALOG ON CATALOG main TO `data_scientists`;
GRANT SELECT ON TABLE main.default.sales TO `data_scientists`;
```

## Encryption and Azure Key Vault Integration

Security best practices dictate that credentials (passwords, connection strings) should never be hardcoded in notebooks. Databricks integrates with Azure Key Vault via **Secret Scopes**.

```python
# Fetching a secret securely in a notebook
# 'my-key-vault-scope' is configured to point to an Azure Key Vault
db_password = dbutils.secrets.get(scope="my-key-vault-scope", key="database-password")

# Use the secret to connect to an external database
jdbc_url = "jdbc:postgresql://myserver:5432/mydb"
df = spark.read \\
    .format("jdbc") \\
    .option("url", jdbc_url) \\
    .option("dbtable", "employees") \\
    .option("user", "admin") \\
    .option("password", db_password) \\
    .load()
```
"""

ch12_content = """# Chapter 12: Hands-On Projects

This chapter outlines three practical projects to solidify your understanding of Databricks and the Lakehouse architecture.

## 1. Build a Lakehouse (Medallion Architecture)

Implement the Medallion Architecture (Bronze, Silver, Gold):
1. **Bronze**: Ingest raw JSON logs using Auto Loader.
2. **Silver**: Cleanse the data, deduplicate, and enforce schema using PySpark, saving as Delta tables.
3. **Gold**: Aggregate the data for business reporting (e.g., daily active users).

```python
# Conceptual Gold Layer Aggregation
gold_df = spark.read.table("silver.user_events") \\
    .groupBy("date", "user_id") \\
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
aggregated_df = streaming_df \\
    .groupBy(window("timestamp", "1 minute"), "sensor_id") \\
    .agg(avg("temperature").alias("avg_temp"))

# Write to Delta
aggregated_df.writeStream \\
    .format("delta") \\
    .outputMode("complete") \\
    .option("checkpointLocation", "/mnt/checkpoints/iot") \\
    .table("silver.iot_aggregates")
```

## 3. Real-Time Dashboards and ML Apps

- Train a predictive maintenance model on the IoT data using MLflow.
- Deploy the model as an endpoint or apply it in a batch job to flag failing sensors.
- Connect Databricks SQL or Power BI to the resulting Delta table to create a live, real-time dashboard alerting operators of predicted failures.
"""

(module2_dir / '06_Introduction_to_Databricks.md').write_text(ch6_content, encoding='utf-8')
(module2_dir / '07_Core_Concepts.md').write_text(ch7_content, encoding='utf-8')
(module2_dir / '08_Data_Engineering.md').write_text(ch8_content, encoding='utf-8')
(module2_dir / '09_Machine_Learning.md').write_text(ch9_content, encoding='utf-8')
(module2_dir / '10_Analytics_and_BI.md').write_text(ch10_content, encoding='utf-8')
(module2_dir / '11_Security_and_Governance.md').write_text(ch11_content, encoding='utf-8')
(module2_dir / '12_Hands_On_Projects.md').write_text(ch12_content, encoding='utf-8')

# Update README.md
readme_path = base_dir / 'README.md'
readme_content = readme_path.read_text(encoding='utf-8')

import re
new_module2_section = """### Module 2 - Databricks
- [Chapter 6: Introduction to Databricks](chapters/module2/06_Introduction_to_Databricks.md)
- [Chapter 7: Core Concepts](chapters/module2/07_Core_Concepts.md)
- [Chapter 8: Data Engineering](chapters/module2/08_Data_Engineering.md)
- [Chapter 9: Machine Learning](chapters/module2/09_Machine_Learning.md)
- [Chapter 10: Analytics & BI](chapters/module2/10_Analytics_and_BI.md)
- [Chapter 11: Security & Governance](chapters/module2/11_Security_and_Governance.md)
- [Chapter 12: Hands-On Projects](chapters/module2/12_Hands_On_Projects.md)
"""

readme_content = re.sub(r'### Module 2 - Databricks.*', new_module2_section, readme_content, flags=re.DOTALL)
readme_path.write_text(readme_content, encoding='utf-8')

print("Generated Module 2 Chapters 6-12 and updated README.md")
