{{ config(
  materialized='table',
  partition_by={'field': 'txn_ts_utc', 'data_type': 'timestamp'},
  cluster_by=['market','account_id']
) }}

with src as (
  select
    market,
    txn_id,
    account_id,
    customer_id,
    TIMESTAMP(txn_ts_local, {{ get_market_tz('market') }}) as txn_ts_utc,
    amount_local,
    currency,
    mcc,
    channel
  from {{ ref('raw_transactions') }}
),

fx as (
  select currency, rate_to_usd, fx_date from {{ ref('ref_fx_rates') }}
)

select
  s.market,
  s.txn_id,
  s.account_id,
  s.customer_id,
  s.txn_ts_utc,
  s.amount_local,
  s.currency,
  s.mcc,
  s.channel,
  f.rate_to_usd,
  round(s.amount_local * f.rate_to_usd, 2) as amount_usd
from src s
left join fx f
  on f.currency = s.currency
  and date(s.txn_ts_utc) = f.fx_date
