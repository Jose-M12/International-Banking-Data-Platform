# Cloud Onboarding

1) `gcloud auth application-default login`
2) `make tf-init && make tf-apply PROJECT=...`
3) `gsutil cp spark_jobs/features/customer_features_job.py gs://$GCS_BRONZE_BUCKET/jobs/`
4) Set Airflow VARs in Composer or local to your project
5) Trigger pipelines
