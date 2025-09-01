# Local Onboarding

1) `cp .env.sample .env`
2) `make up`
3) `make airflow-init && make airflow-vars`
4) `make seed`
5) Open Airflow http://localhost:8080 (admin/admin)
6) Trigger intl_batch_pipeline
7) Optional: open Superset http://localhost:8088
