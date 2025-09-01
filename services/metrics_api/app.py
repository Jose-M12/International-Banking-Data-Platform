from fastapi import FastAPI
from google.cloud import bigquery
app = FastAPI()
client = bigquery.Client()
@app.get("/kpi/daily_volume")
def daily_volume():
    q = """
    select date(txn_ts_utc) dt, sum(amount_usd) usd
    from `PROJECT.gold.intl_transactions_fact`
    group by 1 order by 1 desc limit 30
    """
    rows = client.query(q).result()
    return [{"date": r["dt"].isoformat(), "usd": float(r["usd"])} for r in rows]
