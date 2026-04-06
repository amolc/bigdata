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

Delta Lake is an open-source stimport os
from pathlib import Path

base_dir = Path('k from patda