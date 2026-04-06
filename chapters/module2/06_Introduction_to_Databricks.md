# Chapter 6: Introduction to Databricks

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