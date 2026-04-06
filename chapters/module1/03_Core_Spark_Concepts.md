# Chapter 3: Core Spark Concepts

Apache Spark provides several layers of abstraction for processing distributed data. Understanding these core concepts is critical for writing efficient and reliable Spark applications.

## RDDs (Resilient Distributed Datasets)

Resilient Distributed Datasets (RDDs) are the fundamental data structure of Apache Spark. They are an immutable, distributed collection of objects that can be operated on in parallel.

### Creation and Transformations

You can create an RDD in two ways: parallelizing an existing collection in your driver program, or referencing a dataset in an external storage system (like HDFS or S3).

Once created, you apply **transformations** to RDDs. Transformations (like `map`, `filter`, and `flatMap`) return a *new* RDD and do not alter the original data.

```python
# PySpark Example: RDD Creation and Transformations
data = [1, 2, 3, 4, 5]

# Create RDD from a collection
rdd = spark.sparkContext.parallelize(data)

# Transformation 1: Multiply each element by 2
rdd_mapped = rdd.map(lambda x: x * 2)

# Transformation 2: Filter elements greater than 5
rdd_filtered = rdd_mapped.filter(lambda x: x > 5)
```

### Actions and Lazy Evaluation

Spark utilizes **lazy evaluation**. When you call a transformation on an RDD, Spark does not compute it immediately. Instead, it builds a logical execution plan (a DAG). The computation is only triggered when you call an **action** (like `collect`, `count`, or `reduce`).

```python
# Action: Trigger the computation and return the results to the driver
results = rdd_filtered.collect()
print(results)  # Output: [6, 8, 10]

# Action: Count the number of elements
count = rdd_filtered.count()
print(count)    # Output: 3
```

### Fault Tolerance and Lineage

"Resilient" means RDDs can automatically recover from node failures. Spark achieves fault tolerance through **lineage**. It remembers the sequence of transformations used to build an RDD. If a partition of an RDD is lost due to a node failure, Spark simply recomputes that specific partition using the lineage graph, without needing to replicate data across the network.

## DataFrames and Datasets

While RDDs are powerful, they are low-level. Spark SQL introduced DataFrames and Datasets to provide higher-level, optimized abstractions. 

A **DataFrame** is a distributed collection of data organized into named columns, conceptually equivalent to a table in a relational database or a data frame in R/Python. 

A **Dataset** (available in Scala/Java, but not Python/R) is a strongly-typed, object-oriented extension of DataFrames.

### Schema Definition

DataFrames require a schema. Spark can infer the schema automatically, or you can define it explicitly to prevent errors and improve parsing speed.

```python
# PySpark Example: Schema Definition
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define an explicit schema
schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Age", IntegerType(), True),
    StructField("City", StringType(), True)
])

data = [("Alice", 28, "New York"), ("Bob", 25, "San Francisco")]

# Create a DataFrame with the defined schema
df = spark.createDataFrame(data, schema=schema)
df.printSchema()
# root
#  |-- Name: string (nullable = true)
#  |-- Age: integer (nullable = true)
#  |-- City: string (nullable = true)

df.show()
# +-----+---+-------------+
# | Name|Age|         City|
# +-----+---+-------------+
# |Alice| 28|     New York|
# |  Bob| 25|San Francisco|
# +-----+---+-------------+
```

### Type-Safe Operations

*Note: Type-safe Datasets are primarily a feature of Scala and Java. Python is dynamically typed, so it only uses DataFrames.*

In Scala, Datasets provide compile-time type safety. If you try to query a column that doesn't exist, the code will fail to compile.

```scala
// Scala Example: Type-Safe Datasets
case class Person(name: String, age: Int, city: String)

// Read JSON and convert DataFrame to a typed Dataset using 'as[Person]'
val ds = spark.read.json("people.json").as[Person]

// Type-safe filtering: the compiler knows 'age' is an Int
val adults = ds.filter(person => person.age > 18)
adults.show()
```

### Interoperability with RDDs

Spark makes it easy to switch between RDDs and DataFrames/Datasets depending on your needs. You might use an RDD for complex unstructured data parsing, and then convert it to a DataFrame for optimized aggregations.

```python
# PySpark Example: Interoperability

# 1. Start with an RDD
rdd_lines = spark.sparkContext.parallelize(["Alice,28", "Bob,25"])

# 2. Parse the RDD (Transformation)
rdd_parsed = rdd_lines.map(lambda line: line.split(","))

# 3. Convert RDD to DataFrame
# We map the RDD to a Row-like structure first
from pyspark.sql import Row
rdd_rows = rdd_parsed.map(lambda p: Row(Name=p[0], Age=int(p[1])))

df_from_rdd = spark.createDataFrame(rdd_rows)
df_from_rdd.show()

# 4. Convert DataFrame back to RDD
back_to_rdd = df_from_rdd.rdd
# The result is an RDD of Row objects
print(back_to_rdd.collect())
# [Row(Name='Alice', Age=28), Row(Name='Bob', Age=25)]
```
