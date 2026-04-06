# Chapter 11: Security & Governance

## RBAC and Unity Catalog

Databricks employs Role-Based Access Control (RBAC) for managing permissions on clusters, jobs, and workspace items. 

**Unity Catalog** is the unified governance solution for data and AI on the Lakehouse. It provides centralized access control, auditing, and data discovery across all Databricks workspaces.

```sql
-- Unity Catalog Access Control
-- Granting access to a specific catalog and table
GRANT USE CATALOG ON CATALOG main TO `data_scientists`;
GRANT SELECT ON TABLE main.default.sales TO `data_scientists`;
```

## Encryption and Azure Key Vault Integration

Security best practices dictate that credentials (passwords, connection strings) should never be hardcoded in notebooks. Databricks integrates with Azure Key Vault via **Secret Scopes**.

```python
# Fetching a secret securely in a notebook
# 'my-key-vault-scope' is configured to point to an Azure Key Vault
db_password = dbutils.secrets.get(scope="my-key-vault-scope", key="database-password")

# Use the secret to connect to an external database
jdbc_url = "jdbc:postgresql://myserver:5432/mydb"
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "employees") \
    .option("user", "admin") \
    .option("password", db_password) \
    .load()
```