#!/bin/bash

PROJECT_NAME="airflow_gex_data_pipeline"
CONTAINER_NAME="${PROJECT_NAME}_airflow-webserver_1"

# Add source database connection
docker exec -it $CONTAINER_NAME \
    airflow connections add 'postgres_source' \
    --conn-type 'postgres' \
    --conn-login 'sourcedb1' \
    --conn-password 'sourcedb1' \
    --conn-host 'postgres-source' \
    --conn-port 5432 \
    --conn-schema 'sourcedb'

# Add destination database connection
docker exec -it $CONTAINER_NAME \
    airflow connections add 'postgres_dest' \
    --conn-type 'postgres' \
    --conn-login 'destdb1' \
    --conn-password 'destdb1' \
    --conn-host 'postgres-dest' \
    --conn-port 5432 \
    --conn-schema 'destdb'

# Add store database connection (optional, for GE checkpoints)
docker exec -it $CONTAINER_NAME \
    airflow connections add 'postgres_store' \
    --conn-type 'postgres' \
    --conn-login 'storedb1' \
    --conn-password 'storedb1' \
    --conn-host 'postgres-store' \
    --conn-port 5432 \
    --conn-schema 'storedb'
