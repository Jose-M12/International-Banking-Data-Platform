# International Banking Data Platform (IBDP)

## 1. What is this?

This project is a simulation of an “International Banking Data Platform” that ingests multi-country banking data from an on-prem-like environment, migrates and operates on GCP, and delivers curated, governed, and observable data products for analytics.

![Architecture Diagram](docs/img/architecture.png)

## 2. Quickstart local

```bash
# 1. Set up environment
cp .env.sample .env

# 2. Start services
make up

# 3. Initialize Airflow
make airflow-init && make airflow-vars

# 4. Seed the database
make seed

# 5. Open services
# Airflow: http://localhost:8080 (admin/admin)
# Superset: http://localhost:8088
# Marquez: http://localhost:3000
```

## 3. Quickstart GCP

```bash
# 1. Authenticate with GCP
gcloud auth application-default login

# 2. Apply Terraform infrastructure
make tf-init && make tf-apply PROJECT=<your-gcp-project>

# 3. Upload Spark job to GCS
gsutil cp spark_jobs/features/customer_features_job.py gs://$GCS_BRONZE_BUCKET/jobs/

# 4. Set Airflow variables in Composer or local UI

# 5. Trigger the pipelines
```

## 4. Data model

See [dbt docs](transformations/dbt/target/index.html) and the entity list in `docs/data_model.md`.

## 5. DQ & Governance

See Great Expectations suites in `dq/great_expectations/expectations/` and policy tags in the Terraform configuration.

## 6. CI/CD

[![CI](.github/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)

See the CI workflow in `.github/workflows/ci.yml`.

## 7. Demo scenarios

See `docs/runbooks/` for demo scenarios.

## 8. Roadmap

- Streaming ingestion with Debezium and Kafka
- Feature store integration with Feast
- Data contracts enforcement

## 9. Security note

This project uses synthetic data and does not contain any real PII. See `SECURITY.md` for more details.
