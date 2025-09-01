import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from google.cloud import storage
from datetime import datetime

def write_csv_to_gcs(df, bucket, path):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(path)
    blob.upload_from_string(df.to_csv(index=False), content_type="text/csv")

def main(market):
    host = os.getenv(f"MYSQL_{market}_HOST", "mysql-mx")
    port = os.getenv(f"MYSQL_{market}_PORT", "3306")
    user = os.getenv(f"MYSQL_{market}_USER", "root")
    pw = os.getenv(f"MYSQL_{market}_PASSWORD", "example")
    db = os.getenv(f"MYSQL_{market}_DB", f"bank_{market.lower()}")
    gcs_bucket = os.getenv("GCS_BRONZE_BUCKET")
    ts = datetime.utcnow().strftime("%Y%m%d")

    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}")

    tables = ["customers", "accounts", "transactions"]
    for t in tables:
        df = pd.read_sql(f"SELECT * FROM {t}", engine)
        path = f"{market.lower()}/{t}/load_dt={ts}/{t}_{ts}.csv"
        write_csv_to_gcs(df, gcs_bucket, path)
        print(f"Wrote {len(df)} rows to gs://{gcs_bucket}/{path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--market", required=True)
    args = parser.parse_args()
    main(args.market)
