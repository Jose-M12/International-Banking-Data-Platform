{{ config(materialized='table') }}
-- Simple static FX for demo. Replace with real API ingestion later.
select * from unnest([
  struct('MXN' as currency, date_sub(current_date(), interval 2 day) as fx_date, 0.058 as rate_to_usd),
  struct('MXN', date_sub(current_date(), interval 1 day), 0.059),
  struct('MXN', current_date(), 0.060)
])
