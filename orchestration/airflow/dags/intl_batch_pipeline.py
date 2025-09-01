from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

default_args = {"owner": "data-eng", "retries": 2, "retry_delay": timedelta(minutes=5)}

with DAG(
    "intl_batch_pipeline",
    start_date=datetime(2024,1,1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["intl","batch"],
) as dag:

    extract_mx = BashOperator(
        task_id="extract_mx",
        bash_command="python /opt/airflow/dags/scripts/extract_mysql_to_gcs.py --market MX",
        env={"GCS_BRONZE_BUCKET": "{{ var.value.gcs_bronze_bucket }}"},
    )

    load_raw_txn = GCSToBigQueryOperator(
        task_id="load_raw_txn",
        bucket="{{ var.value.gcs_bronze_bucket }}",
        source_objects=["mx/transactions/*/*.csv"],
        destination_project_dataset_table="{{ var.value.bq_project }}.raw.transactions",
        source_format="CSV",
        write_disposition="WRITE_APPEND",
        autodetect=True,
        time_partitioning={"type":"DAY"}  # no field -> ingestion-time partitioning
    )

    dq_check = BashOperator(
        task_id="dq_check",
        bash_command="great_expectations --v3-api checkpoint run raw_transactions_checkpoint",
        cwd="/opt/airflow/dags/dq",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /opt/airflow/dags/transformations/dbt --profiles-dir /opt/airflow/dags/transformations/dbt",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /opt/airflow/dags/transformations/dbt --profiles-dir /opt/airflow/dags/transformations/dbt",
    )

    extract_mx >> load_raw_txn >> dq_check >> dbt_run >> dbt_test
