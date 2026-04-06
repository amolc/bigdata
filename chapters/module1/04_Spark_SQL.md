# Chapter 4: Spark SQL

## Introduction to Spark SQL

Spark SQL is an Apache Spark module for working with structured data. Unlike the basic Spark RDD API, the interfaces provided by Spark SQL give Spark more information about the structure of both the data and the computation being performed. Internally, Spark SQL uses this extra information to perform powerful optimizations via its Catalyst optimizer.

## DataFrames and Spark SQL

The core abstraction of Spark SQL is the **DataFrame**. A DataFrame is a Dataset organized into named columns, analogous to a table in a relational database. Spark SQL enables you to seamlessly mix SQL queries with DataFrame API operations.

### Schema Inference and Manual Schema Definition

Spark can automatically infer the schema of a data source (like JSON or CSV), but explicitly defining the schema is often preferred for performance and data integrity.

```python
# PySpark Example: Schema Inference vs. Manual Schema

# 1. Schema Inference (Spark reads the data to figure out types)
df_inferred = spark.read.json("path/to/people.json")
df_inferred.printSchema()

# 2. Manual Schema Definition
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Age", IntegerType(), True),
    StructField("City", StringType(), True)
])

df_manual = spark.read.schema(schema).json("path/to/people.json")
df_manual.printSchema()
```

## Creating DataFrames from Various Sources

Spark SQL makes it simple to read and write data in multiple formats, including CSV, JSON, Parquet, ORC, and JDBC.

```python
# Reading a CSV file (with header and inferred schema)
df_csv = spark.read.csv("data/employees.csv", header=True, inferSchema=True)

# Reading a JSON file
df_json = spark.read.json("data/employees.json")

# Reading a Parquet file (Parquet preserves schema automatically)
df_parquet = spark.read.parquet("data/employees.parquet")

# Writing data back to Parquet format
df_csv.write.mode("overwrite").parquet("output/employees.parquet")
```

## DataFrame Operations

DataFrames provide a domain-specific language (DSL) for structured data manipulation, offering a programmatic way to filter, aggregate, and transform data.

```python
# PySpark Example: DataFrame Operations
from pyspark.sql.functions import col, desc

# 1. Select specific columns
df_selected = df_csv.select("Name", "City")

# 2. Filter data
df_filtered = df_csv.filter(col("Age") > 30)

# 3. GroupBy and Aggregate
# Find the average age per city
df_grouped = df_csv.groupBy("City").avg("Age")

# 4. Joins
# Assuming we have a second DataFrame 'df_departments'
df_joined = df_csv.join(df_departments, df_csv.DeptID == df_departments.ID, "inner")

# 5. OrderBy / Sort
df_sorted = df_csv.orderBy(desc("Age"))
```

## Querying Structured Data using SQL

One of the most powerful features of Spark SQL is the ability to write ANSI SQL queries directly against your data.

### Temporary and Global Views

To query a DataFrame using SQL, you must first register it as a view. 

- **Temporary Views**: Tied to the specific `SparkSession` that created them. They disappear when the session terminates.
- **Global Temporary Views**: Tied to a system preserved database `global_temp`, meaning they can be shared across multiple `SparkSession`s within the same Spark application.

```python
# PySpark Example: Temporary and Global Views

# Create a Temporary View
df_csv.createOrReplaceTempView("employees")

# Create a Global Temporary View
df_csv.createOrReplaceGlobalTempView("global_employees")
```

### SQL Queries using `spark.sql()`

Once a view is registered, you can execute SQL queries using `spark.sql()`. The result is returned as a DataFrame.

```python
# Querying a Temporary View
sql_df = spark.sql("""
    SELECT City, AVG(Age) as AvgAge 
    FROM employees 
    WHERE Age > 25 
    GROUP BY City 
    ORDER BY AvgAge DESC
""")

sql_df.show()

# Querying a Global Temporary View (requires 'global_temp.' prefix)
global_sql_df = spark.sql("SELECT * FROM global_temp.global_employees")
```

## Integrating with Hive

Spark SQL supports reading and writing data stored in Apache Hive. To use Hive features, you need to instantiate a `SparkSession` with Hive support enabled. This allows you to access Hive tables, UDFs (User Defined Functions), and the Hive Metastore.

```python
# PySpark Example: Integrating with Hive
from pyspark.sql import SparkSession

# Initialize SparkSession with Hive support
spark_hive = SparkSession.builder \
    .appName("Hive Integration Example") \
    .enableHiveSupport() \
    .getOrCreate()

# Create a Hive table
spark_hive.sql("CREATE TABLE IF NOT EXISTS hive_records (key INT, value STRING) USING hive")

# Load data into the Hive table
spark_hive.sql("LOAD DATA LOCAL INPATH 'data/kv1.txt' INTO TABLE hive_records")

# Query the Hive table
hive_results = spark_hive.sql("SELECT * FROM hive_records WHERE key < 10")
hive_results.show()
```
