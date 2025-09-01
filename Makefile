up:
	docker compose up -d

down:
	docker compose down -v

seed:
	docker compose exec mysql-mx python /seed/seed_mysql.py --market MX --days 60 --customers 2000

airflow-init:
	docker compose exec airflow-webserver airflow db init && docker compose exec airflow-webserver airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

airflow-vars:
	docker compose exec airflow-webserver python /opt/airflow/dags/scripts/set_airflow_vars.py

dbt-docs:
	cd transformations/dbt && dbt docs generate && python -m http.server 8088

tf-init:
	cd infra/terraform/envs/dev && terraform init

tf-apply:
	cd infra/terraform/envs/dev && terraform apply -auto-approve

test:
	pytest -q
