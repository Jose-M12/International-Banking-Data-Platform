from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("dbt_backfill", start_date=datetime(2024,1,1), schedule=None, catchup=False) as dag:
    run = BashOperator(
        task_id="dbt_run_backfill",
        bash_command="dbt run -s tag:timebound --vars '{backfill_date: {{ dag_run.conf.get(\"date\", \"2024-01-01\") }} }' --project-dir /opt/airflow/dags/transformations/dbt --profiles-dir /opt/airflow/dags/transformations/dbt"
    )
