{{ config(materialized='table', partition_by={'field':'date','data_type':'date'}, cluster_by=['account_id']) }}

with daily as (
  select
    account_id,
    date(txn_ts_utc) as date,
    sum(case when amount_usd > 0 then amount_usd else 0 end) as inflow_usd,
    sum(case when amount_usd < 0 then -amount_usd else 0 end) as outflow_usd
  from {{ ref('silver_transactions') }}
  group by 1,2
)
select
  d.*,
  sum(d.inflow_usd - d.outflow_usd) over (partition by account_id order by date rows between unbounded preceding and current row) as end_balance_usd
from daily d
