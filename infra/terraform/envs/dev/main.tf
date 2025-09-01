provider "google" {
  project = var.project
  region  = var.region
}

module "bq" {
  source   = "../../modules/bq"
  project  = var.project
  location = var.location
}

resource "google_dataproc_cluster" "dp_features" {
  name   = "dp-features"
  region = var.region

  cluster_config {
    staging_bucket = "${var.project}-bronze"
    master_config { num_instances = 1; machine_type = "n2-standard-4" }
    worker_config { num_instances = 2; machine_type = "n2-standard-4" }
    software_config {
      image_version = "2.2-debian12"
      optional_components = ["JUPYTER"]
      properties = {
        "spark:spark.jars.packages" = "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1"
      }
    }
  }
}
