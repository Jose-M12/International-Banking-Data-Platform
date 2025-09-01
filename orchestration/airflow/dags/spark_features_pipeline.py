from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

PROJECT = "{{ var.value.bq_project }}"
REGION = "{{ var.value.gcp_region }}"
CLUSTER = "dp-features"

pyspark_job = {
    "reference": {"project_id": PROJECT},
    "placement": {"cluster_name": CLUSTER},
    "pyspark_job": {
        "main_python_file_uri": "gs://{{ var.value.gcs_bronze_bucket }}/jobs/customer_features_job.py",
        "args": [],
        "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.36.1.jar"]
    },
}

with DAG("spark_features_pipeline", start_date=datetime(2024,1,1), schedule="@daily", catchup=False) as dag:
    submit = DataprocSubmitJobOperator(
        task_id="compute_customer_features",
        job=pyspark_job,
        region=REGION,
        project_id=PROJECT
    )
