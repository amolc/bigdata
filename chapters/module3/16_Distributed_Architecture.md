# Chapter 16: Distributed Architecture

## Cluster Setup: Master vs. Worker Nodes
A distributed big data cluster follows a Master-Worker (or Master-Slave) topology.
- **Master Node:** The "brain" of the cluster. It does not process the data itself; instead, it stores metadata, tracks where data is located, and schedules tasks for the workers.
- **Worker Nodes:** The "brawn" of the cluster. These are commodity machines that store the actual data blocks and perform the computations assigned by the Master.

## Daemons: NameNode, DataNode, ResourceManager, NodeManager
In a traditional Hadoop YARN ecosystem, specific software processes (daemons) run on these nodes to manage storage and computation.

**Storage Daemons (HDFS):**
- **NameNode (Master):** Keeps the directory tree of all files in the file system and tracks where across the cluster the file data (blocks) is kept.
- **DataNode (Worker):** Stores and retrieves the actual data blocks when told to (by clients or the NameNode).

**Compute Daemons (YARN):**
- **ResourceManager (Master):** The ultimate authority that arbitrates resources (CPU/Memory) among all the applications in the system.
- **NodeManager (Worker):** Runs on every worker node, responsible for launching application containers, monitoring their resource usage, and reporting back to the ResourceManager.

## Heartbeats and Fault Tolerance
Distributed systems assume that hardware will eventually fail. To manage this:
- **Heartbeats:** Worker nodes (DataNodes/NodeManagers) send continuous "heartbeat" signals (e.g., every 3 seconds) to the Master nodes. 
- **Fault Tolerance:** If the Master stops receiving a heartbeat from a specific Worker, it assumes the node has died. The Master will then automatically reroute the computation tasks and replicate the lost data blocks to other healthy nodes in the cluster, ensuring the job completes successfully without human intervention.
