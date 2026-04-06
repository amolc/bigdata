# Chapter 9: Machine Learning

## ML Lifecycle and Model Training

Databricks provides a collaborative environment for the entire Machine Learning lifecycle: data preparation, feature engineering, model training, and deployment.

```python
# Basic Model Training Example
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

# Prepare data
assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
train_data = assembler.transform(df).select("features", "label")

# Train model
rf = RandomForestClassifier(numTrees=10)
model = rf.fit(train_data)
```

## MLflow for Tracking and Tuning

MLflow is deeply integrated into Databricks to track experiments, package code, and deploy models.

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

with mlflow.start_run():
    # Train scikit-learn model
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(X_train, y_train)
    
    # Evaluate
    predictions = rf.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    
    # Log parameters and metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("mse", mse)
    
    # Log the model
    mlflow.sklearn.log_model(rf, "random_forest_model")
```

## Integration with Azure ML

Databricks models tracked in MLflow can be seamlessly deployed to Azure Machine Learning (Azure ML) for serving as REST endpoints.

```python
# Conceptual snippet for Azure ML deployment
import mlflow.azureml

azure_workspace = Workspace.get(name="myworkspace", subscription_id="...", resource_group="...")
mlflow.azureml.deploy(
    model_uri="runs:/<run_id>/random_forest_model",
    workspace=azure_workspace,
    deployment_config=...,
    service_name="my-rf-service"
)
```