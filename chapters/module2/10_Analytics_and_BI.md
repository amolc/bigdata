# Chapter 10: Analytics & BI

## Dashboards with Databricks SQL

Databricks SQL allows you to write queries, create visualizations, and assemble them into Dashboards directly within the Databricks Workspace. This provides a lightweight, integrated BI experience.

```sql
-- Example Dashboard Query: Monthly Revenue
SELECT 
  date_trunc('month', order_date) AS order_month,
  SUM(total_amount) AS revenue
FROM silver.orders
GROUP BY 1
ORDER BY 1 DESC;
```

## Power BI and Real-Time Analytics

For enterprise reporting, Databricks connects seamlessly to Power BI via the **Databricks SQL Connector**. 

- **DirectQuery**: Power BI can send queries directly to Databricks SQL Warehouses, ensuring users always see the latest data without importing massive datasets into Power BI.
- **Connection Details**: In Power BI, you connect using the Server Hostname and HTTP Path found in the Databricks SQL Warehouse connection details.

```text
# Example Connection String Format (Under the hood JDBC/ODBC)
jdbc:spark://<server-hostname>:443/default;transportMode=http;ssl=1;httpPath=<http-path>;AuthMech=3;UID=token;PWD=<personal-access-token>
```