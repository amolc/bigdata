# Chapter 5: Data Processing

Data processing in Apache Spark involves transforming, cleaning, and extracting insights from massive datasets. Spark's DataFrame API provides a rich set of functions to handle complex data manipulation tasks efficiently.

## Aggregations and Statistics

Aggregations allow you to summarize data across the entire DataFrame or grouped by specific columns. Spark provides numerous built-in aggregation functions like `sum`, `avg`, `min`, `max`, and `count`.

```python
# PySpark Example: Aggregations
from pyspark.sql.functions import sum, avg, max, min, count

# 1. Simple Aggregation on the entire DataFrame
df.select(
    count("EmployeeID").alias("Total_Employees"),
    avg("Salary").alias("Average_Salary"),
    max("Salary").alias("Highest_Salary")
).show()

# 2. GroupBy Aggregations
# Average salary and max age per department
df.groupBy("Department").agg(
    avg("Salary").alias("Avg_Dept_Salary"),
    max("Age").alias("Max_Dept_Age")
).show()

# 3. Descriptive Statistics using describe()
df.describe(["Salary", "Age"]).show()
```

## Joins and Unions

Combining multiple DataFrames is a common requirement. Spark supports various types of joins (inner, outer, left, right, cross) and unions to append rows.

```python
# PySpark Example: Joins and Unions

# --- Joins ---
# Assuming df_employees and df_departments
# Inner Join (Default)
df_inner = df_employees.join(df_departments, df_employees.DeptID == df_departments.ID, "inner")

# Left Outer Join
df_left = df_employees.join(df_departments, df_employees.DeptID == df_departments.ID, "left_outer")

# --- Unions ---
# Assuming df_2022 and df_2023 have the exact same schema
# Union (Appends rows, retains duplicates)
df_all_years = df_2022.union(df_2023)

# UnionByName (Appends rows by column name rather than position)
df_all_years_by_name = df_2022.unionByName(df_2023)
```

## Handling Missing and Complex Data Types

Real-world data is rarely perfect. Spark provides robust methods for handling missing values (Null/NaN) and querying complex data types like arrays and structs.

### Handling Missing Data

```python
# PySpark Example: Missing Data
# 1. Drop rows with any null values
df_clean = df.dropna()

# 2. Drop rows where specific columns are null
df_clean_subset = df.dropna(subset=["Name", "Salary"])

# 3. Fill null values with a default
df_filled = df.fillna({"Salary": 0, "Name": "Unknown"})
```

### Complex Data Types (Arrays and Structs)

```python
# PySpark Example: Arrays and Structs
from pyspark.sql.functions import explode, col, struct

# 1. Arrays: Explode transforms an array column into multiple rows
# If 'Skills' is an array like ["Python", "Spark"]
df_exploded = df.select("Name", explode("Skills").alias("Skill"))

# 2. Structs: Creating and querying nested structures
df_struct = df.withColumn("Address", struct(col("City"), col("State"), col("ZipCode")))

# Accessing nested struct fields
df_struct.select("Name", "Address.City", "Address.State").show()
```

## User Defined Functions (UDFs)

While Spark's built-in functions are highly optimized, you may sometimes need custom logic. UDFs allow you to apply custom Python/Scala functions to DataFrame columns. 

*Note: In Python, UDFs can be a performance bottleneck because data must be serialized between the JVM and Python processes. Use built-in functions whenever possible.*

```python
# PySpark Example: User Defined Functions
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# 1. Define a standard Python function
def categorize_salary(salary):
    if salary is None:
        return "Unknown"
    if salary > 100000:
        return "High"
    elif salary > 50000:
        return "Medium"
    else:
        return "Low"

# 2. Register it as a UDF
categorize_salary_udf = udf(categorize_salary, StringType())

# 3. Apply the UDF to a DataFrame
df_categorized = df.withColumn("Salary_Tier", categorize_salary_udf(col("Salary")))
df_categorized.show()
```

## Working with Dates and Timestamps

Time-series data manipulation is critical in analytics. Spark SQL provides a dedicated suite of date/time functions.

```python
# PySpark Example: Dates and Timestamps
from pyspark.sql.functions import current_date, current_timestamp, date_add, datediff, year, month

df_dates = df.withColumn("Today", current_date()) \
             .withColumn("Now", current_timestamp())

# Date arithmetic
df_future = df_dates.withColumn("Next_Week", date_add(col("Today"), 7))

# Difference between dates
df_diff = df_future.withColumn("Days_Difference", datediff(col("Next_Week"), col("Today")))

# Extracting Date parts (Year, Month)
df_parts = df_dates.withColumn("Current_Year", year(col("Today"))) \
                   .withColumn("Current_Month", month(col("Today")))

df_parts.select("Today", "Next_Week", "Days_Difference", "Current_Year").show()
```
