import argparse, random
from datetime import datetime, timedelta
from faker import Faker
import pymysql

def main(host, user, password, db, days, customers):
    conn = pymysql.connect(host=host, user=user, password=password, database=db, autocommit=True)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
      customer_id VARCHAR(36) PRIMARY KEY,
      name VARCHAR(128), email VARCHAR(128), phone VARCHAR(32), market VARCHAR(4)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
      account_id VARCHAR(36) PRIMARY KEY,
      customer_id VARCHAR(36), type VARCHAR(16), currency VARCHAR(8), market VARCHAR(4)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
      txn_id VARCHAR(36) PRIMARY KEY,
      account_id VARCHAR(36), customer_id VARCHAR(36),
      txn_ts_local DATETIME, amount_local DECIMAL(18,2),
      currency VARCHAR(8), market VARCHAR(4), mcc VARCHAR(8), channel VARCHAR(16)
    )""")
    fk = Faker()
    market = "MX"
    currency = "MXN"

    cust_ids = []
    for _ in range(customers):
      cid = fk.uuid4()
      cust_ids.append(cid)
      cur.execute("INSERT INTO customers VALUES (%s,%s,%s,%s,%s)", (cid, fk.name(), fk.email(), fk.phone_number(), market))

    acct_ids = []
    for cid in cust_ids:
      for _ in range(random.randint(1,3)):
        aid = fk.uuid4()
        acct_ids.append((aid, cid))
        cur.execute("INSERT INTO accounts VALUES (%s,%s,%s,%s,%s)", (aid, cid, random.choice(['checking','credit']), currency, market))

    now = datetime.now()
    mccs = ['5411','5812','6011','4111']
    channels = ['pos','ecom','atm']
    for (aid, cid) in acct_ids:
      n = random.randint(50, 300)
      for _ in range(n):
        ts = now - timedelta(days=random.randint(0,days), hours=random.randint(0,23), minutes=random.randint(0,59))
        amt = round(random.uniform(-3000, 5000), 2)
        tid = fk.uuid4()
        cur.execute("INSERT INTO transactions VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (tid, aid, cid, ts, amt, currency, market, random.choice(mccs), random.choice(channels)))
    cur.close(); conn.close()

if __name__ == "__main__":
  p = argparse.ArgumentParser()
  p.add_argument("--market", default="MX")
  p.add_argument("--host", default="mysql-mx")
  p.add_argument("--user", default="root")
  p.add_argument("--password", default="example")
  p.add_argument("--db", default="bank_mx")
  p.add_argument("--days", type=int, default=60)
  p.add_argument("--customers", type=int, default=2000)
  args = p.parse_args()
  main(args.host, args.user, args.password, args.db, args.days, args.customers)
