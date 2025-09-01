{{ config(materialized='table') }}

select
  t.txn_id,
  t.account_id,
  t.customer_id,
  t.market,
  t.txn_ts_utc,
  t.amount_local,
  t.amount_usd,
  t.currency,
  t.mcc as merchant_category,
  t.channel,
  case when t.amount_usd > 5000 then true else false end as high_value_flag
from {{ ref('silver_transactions') }} t
