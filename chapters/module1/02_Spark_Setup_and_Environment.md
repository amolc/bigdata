# Chapter 2: Spark Setup and Environment

This chapter covers the foundational steps to get Apache Spark up and running, from installation and configuration to interacting with the Spark Shell and understanding how applications are executed across different cluster modes.

## Installing and Configuring Spark

Apache Spark can be run locally on a single machine or distributed across a large cluster. To install it locally for development:

1. **Install Prerequisites**: Spark runs on Java, so you must have the Java Development Kit (JDK) installed. You will also need Python if you intend to use PySpark.
2. **Download Spark**: Download the pre-built version of Spark from the [official Apache Spark website](https://spark.apache.org/downloads.html).
3. **Extract the Archive**:
   ```bash
   tar -xvf spark-3.x.x-bin-hadoop3.tgz
   mv spark-3.x.x-bin-hadoop3 /usr/local/spark
   ```

### Environment Variables

You need to configure your environment variables to access Spark executables easily. Add the following lines to your `~/.bashrc` or `~/.zshrc`:

```bash
# Set Spark Home
export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Optional: Set PySpark to use Jupyter Notebook or a specific Python version
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'
```

Apply the changes:
```bash
source ~/.bashrc
```

### Configuration Files

Spark's configurations are stored in the `$SPARK_HOME/conf` directory. You can customize them by copying the provided templates:

**1. `spark-env.sh`**: Used for setting environment-specific variables like memory allocation.
```bash
cp $SPARK_HOME/conf/spark-env.sh.template $SPARK_HOME/conf/spark-env.sh
```
*Example `spark-env.sh` configuration:*
```bash
# Set the memory for the Spark master and worker nodes
export SPARK_WORKER_MEMORY=4g
export SPARK_WORKER_CORES=2
export SPARK_MASTER_HOST=127.0.0.1
```

**2. `spark-defaults.conf`**: Used to set default Spark properties for all applications.
```bash
cp $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf
```
*Example `spark-defaults.conf` configuration:*
```properties
spark.master                     spark://127.0.0.1:7077
spark.driver.memory              2g
spark.executor.memory            4g
spark.serializer                 org.apache.spark.serializer.KryoSerializer
spark.eventLog.enabled           true
spark.eventLog.dir               file:///tmp/spark-events
```

## Working with Spark Shell

Spark provides interactive shells that allow you to write and execute code interactively. This is incredibly useful for data exploration and debugging.

- **Scala Shell**: Run `spark-shell` from your terminal.
- **Python Shell**: Run `pyspark`.
- **R Shell**: Run `sparkR`.
- **SQL Shell**: Run `spark-sql`.

### Example: Using PySpark

When you launch `pyspark`, a `SparkSession` is automatically created and available as the variable `spark`.

```python
# Launch the shell
$ pyspark

# Inside the PySpark shell:
>>> data = [("Alice", 28), ("Bob", 25), ("Charlie", 32)]
>>> df = spark.createDataFrame(data, ["Name", "Age"])
>>> df.show()
+-------+---+
|   Name|Age|
+-------+---+
|  Alice| 28|
|    Bob| 25|
|Charlie| 32|
+-------+---+

>>> df.filter(df.Age > 25).show()
+-------+---+
|   Name|Age|
+-------+---+
|  Alice| 28|
|Charlie| 32|
+-------+---+
```

## Spark Application Lifecycle

When you write a standalone Spark application, you package your code and submit it to the cluster using the `spark-submit` script.

The typical lifecycle of a Spark application looks like this:

1. **Submission**: The user submits the application via `spark-submit`.
2. **Driver Initialization**: The Driver process starts and executes the `main()` function, creating a `SparkSession` / `SparkContext`.
3. **Resource Allocation**: The Driver contacts the **Cluster Manager** to negotiate resources (CPU and memory) for the Executors.
4. **Executor Launch**: The Cluster Manager launches **Executors** on the Worker nodes.
5. **Task Execution**: The Driver translates the application's operations (transformations and actions) into a Directed Acyclic Graph (DAG) of stages and tasks. These tasks are sent to the Executors.
6. **Completion**: Once the job finishes, the Driver exits, and the Cluster Manager shuts down the Executors, releasing the resources.

### Example: Submitting an Application

```bash
spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master yarn \
  --deploy-mode cluster \
  --executor-memory 4G \
  --num-executors 10 \
  $SPARK_HOME/examples/jars/spark-examples_2.12-3.x.x.jar 100
```

## Cluster Modes: Local, Standalone, YARN, Mesos

Spark can be deployed in several cluster modes, determined by the `--master` flag when running `spark-submit` or starting a shell.

### 1. Local Mode
Everything runs in a single Java Virtual Machine (JVM) on your local machine. It's strictly for testing and development.
* **Flag**: `--master local` (uses 1 thread) or `--master local[4]` (uses 4 threads) or `--master local[*]` (uses all available logical cores).

### 2. Standalone Mode
Spark includes its own simple cluster manager. It requires you to start a Master node and one or more Worker nodes manually or via provided scripts.
* **Flag**: `--master spark://<master-ip>:7077`
* **Pros**: Easy to set up; no external dependencies.
* **Cons**: Lacks advanced resource scheduling compared to YARN or Kubernetes.

### 3. YARN (Hadoop)
YARN (Yet Another Resource Negotiator) is the resource manager used in Hadoop. Running Spark on YARN allows Spark to run alongside other Hadoop ecosystem tools and utilize HDFS data locally.
* **Flag**: `--master yarn`
* **Pros**: Centralized resource management; integrates perfectly with existing Hadoop clusters.

### 4. Mesos
Apache Mesos is a general-purpose cluster manager that can handle various types of workloads (Hadoop, Spark, Kafka, web servers).
* **Flag**: `--master mesos://<master-ip>:5050`
* **Pros**: Fine-grained resource sharing. (Note: Mesos support is officially deprecated in newer Spark versions in favor of Kubernetes).

*(Note: In modern deployments, **Kubernetes** (`--master k8s://...`) has largely replaced Mesos and Standalone modes for cloud-native containerized Spark workloads).*
