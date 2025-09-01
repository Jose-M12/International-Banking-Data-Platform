# Schema Evolution Runbook

- Alter MySQL source to add a column (e.g., transactions.auth_code VARCHAR(12))
- Update synthetic seeder to populate it partially
- Ensure:
  - Raw BigQuery load autodetects new column
  - dbt silver model selects with safe defaults: coalesce(auth_code, 'UNKNOWN') as auth_code
  - Add dbt test for accepted length/values
