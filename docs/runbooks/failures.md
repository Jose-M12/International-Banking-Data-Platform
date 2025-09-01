# Common Failures and Fixes

- GCS permission denied -> check service account roles
- BigQuery “Not found: Dataset” -> Terraform apply missing
- Airflow import error -> dag bag check and requirements mismatch
- dbt authentication -> keyfile path and profiles.yml env
- DQ failures -> check GE output; triage thresholds
