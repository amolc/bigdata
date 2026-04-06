# Chapter 15: Distributed Processing Frameworks

## Why Distributed Processing is Essential
As data volume grows into the terabyte and petabyte scale, it becomes physically impossible (and economically unfeasible) to store and process it on a single machine. Distributed processing divides a massive dataset into smaller blocks, distributes them across a cluster of computers (nodes), and processes them in parallel. This dramatically reduces computation time and prevents single points of failure.

## Introduction to Hadoop: HDFS + MapReduce
Apache Hadoop was the first major open-source framework to popularize distributed computing. It consists of two main core components:
1. **HDFS (Hadoop Distributed File System):** The storage layer. It breaks large files into blocks (typically 128MB) and replicates them across different nodes for fault tolerance.
2. **MapReduce:** The processing layer. It splits a computation into two phases:
   - *Map phase:* Filters and sorts data across the distributed nodes.
   - *Reduce phase:* Aggregates the results back together.

## Limitations of MapReduce vs. Spark Advantages
While Hadoop MapReduce revolutionized big data, it has significant limitations that Apache Spark was designed to solve:

**MapReduce Limitations:**
- **Disk-Bound:** MapReduce writes intermediate data back to the physical disk after *every* map and reduce step. This constant disk I/O makes it very slow, especially for iterative algorithms (like machine learning).
- **Strict Paradigm:** Developers must force all logic into the rigid map-then-reduce paradigm.
- **Batch Only:** It is designed strictly for batch processing, not real-time streaming.

**Spark Advantages:**
- **In-Memory Processing:** Spark processes data in RAM, only spilling to disk when memory is full. This makes it up to 100x faster than MapReduce for certain workloads.
- **Rich APIs:** Spark provides high-level APIs in Python, Scala, Java, and R, along with over 80 operators (not just map and reduce).
- **Unified Engine:** Spark handles batch, real-time streaming, SQL, and machine learning all within the same framework.
