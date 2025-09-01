import os
from airflow.models import Variable
Variable.set("bq_project", os.getenv("GCP_PROJECT", "YOUR_PROJECT"))
Variable.set("gcs_bronze_bucket", os.getenv("GCS_BRONZE_BUCKET", "your-bucket"))
Variable.set("gcp_region", os.getenv("GCP_REGION", "us-central1"))
