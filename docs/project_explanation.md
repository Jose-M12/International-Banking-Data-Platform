# International Banking Data Platform (IBDP) - Project Explanation

This document provides a thorough explanation of the International Banking Data Platform (IBDP) project.

## High-Level Goals

The main goal of this project is to showcase a modern data engineering platform on Google Cloud Platform (GCP). It simulates a real-world scenario where banking data from multiple countries is ingested, processed, and served for analytics.

The key objectives are:

- Demonstrate on-prem to cloud migration and hybrid data integration.
- Build scalable, extensible, and performant pipelines with Airflow, Spark, and dbt.
- Showcase GCP services (GCS, BigQuery, Pub/Sub, Dataproc or Dataflow, Secret Manager).
- Implement data quality, governance, lineage, and CI/CD.
- Use Docker, Kubernetes, Terraform, and GitHub Actions.
- Deliver analytics-ready “gold” data for retail/risk banking use cases.
- Provide onboarding docs, runbooks, and “community” practices that mirror an agile data engineering team.

## Architecture

The project follows a medallion architecture (Bronze, Silver, Gold) to progressively refine the data.

### On-Prem Simulation (Local Docker)

- **MySQL:** Simulates the core banking OLTP databases for different markets (e.g., MX, PE, CO). Each market has its own MySQL instance to simulate a multi-country environment.
- **Kafka + Debezium:** Used for Change Data Capture (CDC) to stream transactions, accounts, and customers data. Debezium monitors the MySQL binlogs and publishes any changes to Kafka topics.
- **Docker Compose:** Runs all the on-prem components locally. This allows for easy setup and teardown of the on-prem environment.

### Cloud Landing (GCP)

- **Pub/Sub:** Acts as the entry point for the streaming data from the on-prem simulation. A Kafka Connect sink is used to push the data from the Kafka topics to Pub/Sub topics.
- **Dataflow/Dataproc:** Processes the streaming and batch data and lands it in Google Cloud Storage (GCS) and BigQuery. You can choose to use either Dataflow or Dataproc for this purpose.
- **GCS:** Stores the raw (Bronze) and processed (Silver) data. The data is partitioned by date for efficient querying.
- **BigQuery:** The data warehouse for the raw, silver, and gold data. The data is partitioned and clustered for performance and cost optimization.

### Transformations

- **dbt:** Used for ELT (Extract, Load, Transform) in BigQuery to transform the data from Bronze to Silver and then to Gold. dbt models are defined in SQL and are easy to write and maintain.
- **Spark:** Used for heavy transformations and feature engineering that are not suitable for SQL-based transformations in dbt. For example, calculating rolling averages or other window functions over large datasets.

### Orchestration

- **Airflow:** Orchestrates the entire data pipeline, including ingestion, data quality checks, dbt runs, and Spark jobs. The DAGs are defined in Python and are highly extensible.

### Data Quality & Governance

- **Great Expectations:** Used for data quality checks and validations. The data quality checks are defined in JSON and can be run as part of the Airflow DAGs.
- **OpenLineage/Marquez:** Used for data lineage tracking. This allows you to see how data flows through the system and how it is transformed.
- **BigQuery Column-level Security:** Used to mask PII data. This ensures that only authorized users can see sensitive data.

### Serving & Analytics

- **BigQuery:** The gold data marts are served from BigQuery.
- **Superset:** Used for creating dashboards and visualizing the data.
- **FastAPI:** An optional service to expose aggregated data via an API.

### CI/CD

- **GitHub Actions:** Used for continuous integration and continuous deployment. The CI/CD pipeline runs tests, lints the code, and deploys the application to GCP.

### Infrastructure as Code (IaC)

- **Terraform:** Used to provision and manage the GCP infrastructure. The infrastructure is defined in HCL and can be version controlled.

## Data Model

The data model is divided into three layers: Bronze, Silver, and Gold.

### Bronze Layer

- **Schema:** The Bronze layer contains the raw data as it is ingested from the source systems. The schema is not enforced, and the data is stored in its original format.
- **Purpose:** The Bronze layer is used for auditing and for replaying the pipeline in case of errors.

### Silver Layer

- **Schema:** The Silver layer contains the cleaned and transformed data. The schema is enforced, and the data is stored in a structured format (e.g., Parquet). PII data is masked in this layer.
- **Purpose:** The Silver layer is used as the source for the Gold layer and for ad-hoc querying.

### Gold Layer

- **Schema:** The Gold layer contains the aggregated and enriched data that is ready for analytics. The schema is optimized for querying and for use in dashboards.
- **Purpose:** The Gold layer is used for business intelligence and for feeding machine learning models.

## Pipelines

### Streaming Pipeline

1.  Debezium captures changes from the MySQL databases and sends them to Kafka.
2.  A Kafka Connect sink pushes the data from the Kafka topics to Pub/Sub topics.
3.  A Dataflow or Spark job consumes the data from Pub/Sub and writes it to BigQuery (raw) and GCS (bronze).

### Batch Pipeline

1.  An Airflow DAG pulls reference data (e.g., FX rates) from an external API.
2.  The data is written to GCS and then loaded into BigQuery.

### dbt Pipeline

1.  An Airflow DAG runs the dbt models to transform the data from the Bronze to the Silver layer.
2.  Another Airflow DAG runs the dbt models to transform the data from the Silver to the Gold layer.

### Spark Pipeline

1.  An Airflow DAG runs a Spark job on Dataproc to compute complex features from the Silver layer data.
2.  The features are written to a new table in the Gold layer.

## Code Explanation

### On-Prem Simulation (Docker)

- **`docker-compose.yml`:** This file defines the services that make up the on-prem simulation. It includes:
    - `mysql-mx`: A MySQL database for the Mexican market.
    - `airflow-webserver`: The Airflow webserver.
    - `airflow-scheduler`: The Airflow scheduler.
    - `superset`: The Superset analytics platform.
    - `marquez`: The Marquez data lineage tool.

### Orchestration (Airflow)

- **`orchestration/airflow/docker/Dockerfile`:** This file defines the Docker image for the Airflow webserver and scheduler. It installs the necessary dependencies, including the GCP providers for Airflow.
- **`orchestration/airflow/docker/requirements.txt`:** This file lists the Python dependencies that are installed in the Airflow Docker image.
- **`orchestration/airflow/dags/intl_batch_pipeline.py`:** This is the main Airflow DAG that orchestrates the batch pipeline. It performs the following steps:
    1.  `extract_mx`: Extracts data from the MySQL database for the Mexican market and uploads it to GCS.
    2.  `load_raw_txn`: Loads the raw transaction data from GCS into BigQuery.
    3.  `dq_check`: Runs data quality checks on the raw data using Great Expectations.
    4.  `dbt_run`: Runs the dbt models to transform the data.
    5.  `dbt_test`: Runs the dbt tests to ensure the data quality.
- **`orchestration/airflow/dags/scripts/extract_mysql_to_gcs.py`:** This Python script is called by the `extract_mx` task in the Airflow DAG. It connects to the MySQL database, extracts the data for a given market, and uploads it to GCS as a CSV file.

### Transformation (dbt)

- **`transformations/dbt/dbt_project.yml`:** This file is the main configuration file for the dbt project. It defines the project name, the profile to use, and the paths to the model, seed, and test files.
- **`transformations/dbt/models/`:** This directory contains the dbt models that are used to transform the data. The models are organized into subdirectories for the bronze, silver, and gold layers.

### Data Generation

- **`ingestion/data_generator/seed_mysql.py`:** This Python script is used to generate synthetic data and seed the MySQL databases. It uses the `Faker` library to generate realistic data.

### Infrastructure as Code (Terraform)

- **`infra/terraform/`:** This directory contains the Terraform code that is used to provision and manage the GCP infrastructure. The code is organized into modules for the different GCP services (e.g., BigQuery, GCS, Dataproc).

## Configuration

### What You Can Change

- **Markets:** You can add or remove markets by adding or removing MySQL instances in the `docker-compose.yml` file. You will also need to update the Airflow DAGs and dbt models to reflect the changes.
- **dbt Models:** You can add, remove, or modify the dbt models to change the transformations that are applied to the data.
- **Spark Jobs:** You can add, remove, or modify the Spark jobs to change the features that are computed.
- **Dashboards:** You can create your own dashboards in Superset to visualize the data.

### What You Should Not Change

- **Core Infrastructure:** You should not change the core infrastructure (e.g., the GCS buckets, the BigQuery datasets) unless you know what you are doing. The infrastructure is managed by Terraform, and any manual changes will be overwritten.
- **Data Contracts:** You should not change the data contracts (i.e., the schemas of the Kafka topics and the Pub/Sub topics) without careful consideration. Changing the data contracts can break the downstream pipelines.

## How to Use the Project

Please refer to the `docs/onboarding/local.md` and `docs/onboarding/cloud.md` for detailed instructions on how to set up and run the project.

## Project Structure

```
- infra/                  # Infrastructure as Code (Terraform)
- orchestration/          # Airflow DAGs and plugins
- ingestion/              # Data ingestion scripts and configurations
- transformations/        # dbt models and tests
- spark_jobs/             # Spark jobs for feature engineering
- dq/                     # Data quality configurations (Great Expectations)
- lineage/                # Data lineage configurations (Marquez)
- analytics/              # Superset dashboards and notebooks
- services/               # Optional FastAPI service
- .github/                # GitHub Actions workflows and templates
- docs/                   # Project documentation
- scripts/                # Utility scripts
- Makefile                # Makefile for common commands
- pre-commit-config.yaml  # Pre-commit hooks configuration
- CONTRIBUTING.md         # Contribution guidelines
- README.md               # Project README
```
