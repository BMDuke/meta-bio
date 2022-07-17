#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

	CREATE DATABASE $POSTGRES_NAME;
	GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_NAME TO $POSTGRES_USER;
	CREATE USER $GRAFANA_USER WITH PASSWORD '$POSTGRES_PASSWORD';
	GRANT CONNECT ON DATABASE $POSTGRES_NAME TO $GRAFANA_USER;
	GRANT SELECT ON ALL TABLES IN SCHEMA public TO $GRAFANA_USER;

EOSQL