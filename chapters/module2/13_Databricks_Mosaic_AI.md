# Chapter 13: Databricks Mosaic AI

## Introduction to Databricks Mosaic AI

Databricks Mosaic AI is a unified platform designed to build, deploy, and monitor generative AI and Large Language Models (LLMs) directly within the Databricks Lakehouse. It integrates seamlessly with your existing data, allowing you to train or fine-tune custom AI models on your private data while maintaining strict governance and security via Unity Catalog.

Mosaic AI provides tools for both consuming pre-trained foundational models (like Llama 3, DBRX, or OpenAI models) and building custom, domain-specific models from scratch.

## Core Capabilities of Mosaic AI

### 1. Mosaic AI Model Serving (Foundation Model APIs)

Databricks provides Foundation Model APIs that allow you to access state-of-the-art open-source models (like DBRX, Llama, and Mixtral) on a pay-per-token basis without managing the underlying infrastructure.

You can query these models using standard REST APIs or the MLflow Python client.

```python
# Example: Querying a Foundation Model using the MLflow Deployments API
from mlflow.deployments import get_deploy_client

# Connect to the Databricks deployment client
client = get_deploy_client("databricks")

# Send a prompt to the DBRX Instruct model
response = client.predict(
    endpoint="databricks-dbrx-instruct",
    inputs={
        "messages": [
            {"role": "user", "content": "Explain the concept of a Lakehouse in 3 sentences."}
        ],
        "temperature": 0.5,
        "max_tokens": 150
    }
)

print(response["choices"][0]["message"]["content"])
```

### 2. Mosaic AI Vector Search

Vector Search is a serverless similarity search engine built into Databricks. It automatically syncs your Delta tables to a vector index, keeping the index up-to-date as your underlying data changes. This is a critical component for building Retrieval-Augmented Generation (RAG) applications.

```python
# Example: Creating a Vector Search Index from a Delta Table
from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

# Create a Vector Search endpoint (compute resource)
vsc.create_endpoint(name="my_vector_endpoint", endpoint_type="STANDARD")

# Sync a Delta table to a Vector Index
# Assuming 'main.rag_data.documents' has a column 'content'
vsc.create_delta_sync_index(
    endpoint_name="my_vector_endpoint",
    index_name="main.rag_data.documents_index",
    source_table_name="main.rag_data.documents",
    pipeline_type="TRIGGERED",
    primary_key="doc_id",
    embedding_source_column="content",
    embedding_model_endpoint_name="databricks-bge-large-en" # Built-in embedding model
)
```

### 3. Retrieval-Augmented Generation (RAG)

With Vector Search and Foundation Models, building a RAG application is straightforward. You can chain these components together using LangChain and serve the entire chain using Mosaic AI Model Serving.

```python
# Conceptual Example: RAG with LangChain in Databricks
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.chat_models import ChatDatabricks
from langchain.chains import RetrievalQA

# Connect to the previously created Vector Index
vector_store = DatabricksVectorSearch(
    endpoint="my_vector_endpoint",
    index_name="main.rag_data.documents_index"
)

# Initialize the LLM (e.g., DBRX)
llm = ChatDatabricks(endpoint="databricks-dbrx-instruct")

# Create the RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)

# Ask a question based on your private data
answer = qa_chain.run("What are our company's Q3 revenue targets?")
print(answer)
```

### 4. Mosaic AI Model Training (Fine-Tuning)

For highly specialized tasks, prompting a generic model isn't enough. Mosaic AI Model Training allows you to securely fine-tune open-source foundation models (like Llama 3 or Mistral) using your proprietary data stored in Unity Catalog. 

This process abstracts away the complexity of distributed GPU training.

```python
# Example: Fine-tuning a model via the Databricks SDK
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Start a fine-tuning run
run = w.model_training.create(
    name="my_custom_llama3",
    model="meta-llama/Meta-Llama-3-8B",
    train_data_path="main.training_data.customer_support_logs",
    task_type="CHAT_COMPLETION",
    training_duration_epochs=3,
    learning_rate=5e-5
)

print(f"Training started. Run ID: {run.id}")
```

### 5. Mosaic AI Gateway and Governance

Because Mosaic AI is integrated with **Unity Catalog**, all AI assets—from raw training data to vector indexes, fine-tuned models, and serving endpoints—are governed by a single security model.

The **AI Gateway** provides:
- **Rate Limiting & Cost Control**: Manage how many tokens your organization consumes.
- **Auditing & Tracking**: Track who is querying which model and log prompts/responses for compliance and safety monitoring.
- **Credential Management**: Securely store API keys for external models (like OpenAI or Anthropic) in Unity Catalog, preventing key leakage in notebooks.