resource "google_bigquery_dataset" "raw" {
  dataset_id                  = "raw"
  location                    = var.location
  delete_contents_on_destroy  = true
}

resource "google_bigquery_dataset" "silver" {
  dataset_id = "silver"
  location   = var.location
}

resource "google_bigquery_dataset" "gold" {
  dataset_id = "gold"
  location   = var.location
}

resource "google_storage_bucket" "bronze" {
  name     = "${var.project}-bronze"
  location = var.location
  uniform_bucket_level_access = true
  lifecycle_rule {
    action { type = "Delete" }
    condition { age = 30 }
  }
}
