# Chapter 7: Core Concepts

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