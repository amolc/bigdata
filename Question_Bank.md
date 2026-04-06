# Databricks & PySpark Question Bank

This question bank contains 50 questions spanning all chapters to help you review and test your knowledge of Apache Spark, Databricks, and the Lakehouse architecture.

## Module 1: PySpark

### Chapter 1: Introduction to Apache Spark
**1. What is the primary difference between Apache Spark and Hadoop MapReduce regarding data processing?**
*Answer*: Spark processes data primarily in-memory (RAM), making it up to 100x faster than Hadoop MapReduce, which writes intermediate data back to disk after every step.

**2. What are the core components of the Apache Spark ecosystem?**
*Answer*: Spark Core, Spark SQL, Spark Streaming (and Structured Streaming), MLlib (Machine Learning Library), and GraphX.

**3. True or False: Spark requires HDFS to store its data.**
*Answer*: False. Spark is a processing engine and does not have its own persistent storage system. It can read from HDFS, but also from S3, ADLS, local file systems, Cassandra, Kafka, etc.

**4. What does DAG stand for in the context of Apache Spark?**
*Answer*: Directed Acyclic Graph. It is the logical execution plan Spark creates to optimize tasks before actually executing them.

### Chapter 2: Spark Setup and Environment
**5. What is the role of the Cluster Manager in a Spark architecture?**
*Answer*: The Cluster Manager (e.g., YARN, Mesos, Kubernetes, or Standalone) is responsible for acquiring and allocating resources (CPU/memory) across the cluster for Spark applications.

**6. Which Spark cluster mode is typically used only for local development and testing?**
*Answer*: Local mode (e.g., `--master local[*]`), where everything runs inside a single JVM on one machine.

**7. In a PySpark shell, what is the default variable name for the active `SparkSession`?**
*Answer*: `spark`.

**8. What does the `spark-submit` command do?**
*Answer*: It is a script used to launch a Spark application on a cluster.

### Chapter 3: Core Spark Concepts
**9. What does RDD stand for?**
*Answer*: Resilient Distributed Dataset.

**10. What is the difference between a Transformation and an Action in Spark?**
*Answer*: Transformations (like `map`, `filter`) return a new RDD/DataFrame and are evaluated lazily. Actions (like `collect`, `count`) trigger the actual execution of the DAG and return a final value to the driver or write data to external storage.

**11. How does Spark achieve fault tolerance with RDDs?**
*Answer*: Through *lineage*. Spark remembers the sequence of transformations used to build an RDD. If a partition is lost, Spark recomputes just that partition using the lineage graph rather than replicating data across nodes.

**12. What is the primary difference between a DataFrame and a Dataset in Spark?**
*Answer*: A DataFrame is a distributed collection of data organized into named columns (untyped). A Dataset provides the same benefits but is strongly-typed and object-oriented (available in Scala/Java, but not Python/R).

### Chapter 4: Spark SQL
**13. What is the underlying optimizer that powers Spark SQL?**
*Answer*: The Catalyst Optimizer.

**14. What is the difference between a Temporary View and a Global Temporary View?**
*Answer*: A Temporary View is tied to a specific `SparkSession` and disappears when the session ends. A Global Temporary View is tied to the `global_temp` database and can be shared across multiple `SparkSession`s within the same Spark application.

**15. If you want Spark to figure out column data types when reading a CSV, what option should you pass?**
*Answer*: `inferSchema=True`.

**16. What function allows you to execute raw SQL strings programmatically in PySpark?**
*Answer*: `spark.sql("SELECT * FROM table")`.

### Chapter 5: Data Processing
**17. What DataFrame method is used to remove rows containing null values?**
*Answer*: `df.dropna()` or `df.na.drop()`.

**18. If you have an array column named "Skills" and want to create a separate row for each item in the array, what PySpark function do you use?**
*Answer*: `explode("Skills")`.

**19. Why should you prefer Spark's built-in functions over Python User Defined Functions (UDFs)?**
*Answer*: Built-in functions run natively in the JVM and are optimized by Catalyst. Python UDFs require serializing data between the JVM and the Python process, which incurs a significant performance penalty.

**20. What is the difference between `union` and `unionByName`?**
*Answer*: `union` appends rows based on the *position* of the columns. `unionByName` appends rows by matching the exact *names* of the columns, regardless of their order.

---

## Module 2: Databricks

### Chapter 6: Introduction to Databricks
**21. What is the "Lakehouse" architecture?**
*Answer*: An architecture that combines the scalable, cheap storage of a data lake with the reliability, ACID transactions, and performance optimizations of a data warehouse.

**22. What open-source storage format is the foundation of the Databricks Lakehouse?**
*Answer*: Delta Lake.

**23. Name two features that Delta Lake adds on top of standard Parquet files.**
*Answer*: ACID transactions, schema enforcement/evolution, time travel (data versioning), and DML operations (UPDATE, DELETE, MERGE).

**24. What are the three primary personas that Databricks aims to unify in one workspace?**
*Answer*: Data Engineers, Data Scientists, and Data Analysts.

### Chapter 7: Core Concepts
**25. How do you execute SQL in a Python notebook in Databricks?**
*Answer*: By using the `%sql` magic command at the top of the cell.

**26. What is the difference between an All-Purpose Cluster and a Job Cluster?**
*Answer*: An All-Purpose cluster is manually created for interactive workspace analysis and can be shared. A Job cluster is automatically spun up by the job scheduler to run a specific workload and terminates immediately when finished to save costs.

**27. What is "Credential Passthrough" in the context of Databricks and Azure?**
*Answer*: It allows users to authenticate automatically to Azure Data Lake Storage (ADLS) from Databricks clusters using the same Azure Active Directory (AAD) identity they used to log into the Databricks workspace.

### Chapter 8: Data Engineering
**28. What SQL command allows you to perform an "Upsert" (Insert if new, Update if existing) in Delta Lake?**
*Answer*: `MERGE INTO`.

**29. What Databricks feature is designed to incrementally and efficiently process new files as they arrive in cloud storage?**
*Answer*: Auto Loader (using `format("cloudFiles")`).

**30. What does DLT stand for in Databricks data engineering?**
*Answer*: Delta Live Tables. It is a declarative framework for building reliable, maintainable, and testable data processing pipelines.

**31. In the Medallion Architecture, what do Bronze, Silver, and Gold represent?**
*Answer*: Bronze = Raw ingested data; Silver = Cleansed, filtered, and augmented data; Gold = Business-level aggregates ready for reporting and BI.

### Chapter 9: Machine Learning
**32. What open-source tool, integrated natively into Databricks, is used to track ML experiments, package code, and manage model versions?**
*Answer*: MLflow.

**33. How do you log a hyperparameter in an MLflow run?**
*Answer*: `mlflow.log_param("param_name", value)`.

**34. How do you log a performance metric (like MSE) in an MLflow run?**
*Answer*: `mlflow.log_metric("metric_name", value)`.

**35. Can a model trained in Databricks and registered in MLflow be deployed to an external service like Azure ML?**
*Answer*: Yes, MLflow provides deployment APIs (e.g., `mlflow.azureml.deploy`) to serve models to Azure ML or AWS SageMaker.

### Chapter 10: Analytics & BI
**36. What is a Databricks SQL Warehouse?**
*Answer*: A dedicated, optimized compute resource designed specifically to run SQL queries and support BI workloads, without requiring users to manage Spark cluster configurations.

**37. If you connect Power BI to Databricks using "DirectQuery", what does that mean?**
*Answer*: Power BI does not import the data into its own memory. Instead, it translates user interactions into SQL queries, sends them directly to the Databricks SQL Warehouse, and returns the results live.

**38. Where do you find the connection details (Hostname, HTTP Path) needed to connect tools like Tableau or Power BI to Databricks?**
*Answer*: In the Connection Details tab of the specific Databricks SQL Warehouse (or Cluster) you wish to query against.

### Chapter 11: Security & Governance
**39. What is the name of the unified governance solution for data and AI on the Databricks Lakehouse?**
*Answer*: Unity Catalog.

**40. If you need to grant a user access to a specific table in Unity Catalog, what standard SQL command do you use?**
*Answer*: `GRANT SELECT ON TABLE <catalog>.<schema>.<table> TO <user/group>;`

**41. Why should you use Databricks Secret Scopes?**
*Answer*: To securely store and reference sensitive credentials (like database passwords or API keys) without hardcoding them in plain text inside notebooks.

**42. What command do you use in a notebook to retrieve a secret from a secret scope?**
*Answer*: `dbutils.secrets.get(scope="<scope_name>", key="<key_name>")`.

### Chapter 12: Hands-On Projects
**43. If you are building a streaming pipeline for IoT data, what Spark feature allows you to group data by time intervals (e.g., every 1 minute)?**
*Answer*: Windowing functions (e.g., `groupBy(window("timestamp", "1 minute"))`).

**44. When writing a streaming DataFrame to a Delta table, what option is absolutely required to ensure fault tolerance and exactly-once processing?**
*Answer*: A checkpoint location (`option("checkpointLocation", "/path/to/checkpoint")`).

**45. What is the primary benefit of using a Delta table as the sink for a streaming IoT pipeline?**
*Answer*: Delta tables support concurrent reads and writes. A streaming job can continuously append or merge data into the table while BI dashboards query the exact same table in real-time without locking or data corruption.

### Chapter 13: Databricks Mosaic AI
**46. What is Databricks Mosaic AI?**
*Answer*: A unified platform within Databricks used to build, deploy, monitor, and fine-tune generative AI and Large Language Models (LLMs) using private data governed by Unity Catalog.

**47. What built-in Databricks tool automatically synchronizes a Delta table into a searchable index for LLM retrieval?**
*Answer*: Mosaic AI Vector Search.

**48. What does RAG stand for?**
*Answer*: Retrieval-Augmented Generation. It is an AI framework where an LLM is augmented with a retriever (like Vector Search) that fetches relevant private documents to ground the model's answer in factual context.

**49. In Databricks SQL, what function allows you to prompt a Foundation Model directly from a SQL query?**
*Answer*: The `ai_query()` function.

**50. Can you fine-tune an open-source model (like Llama 3) inside Databricks using your own proprietary data?**
*Answer*: Yes, using Mosaic AI Model Training, you can securely fine-tune foundation models on data governed by Unity Catalog without data leaving the workspace.