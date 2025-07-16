# Airflow Data Pipeline Validation with Great Expectations


**Repo directory structure:**

    .
    ├── dags
    │   ├── scripts
    │   │   ├── python
    │   │   │   ├── retail_dest.py
    │   │   │   ├── retail_load.py
    │   │   │   ├── retail_source.py
    │   │   │   ├── retail_transform.py
    │   │   │   ├── retail_warehouse.py
    │   │   │   └── utils.py   
    │   │   └── sql
    │   │       ├── extract_json_column.sql
    │   │       ├── extract_load_retail_source.sql
    │   │       ├── load_retail_stage.sql
    │   │       └── transform_load_retail_warehouse.sql
    │   ├── retail_data_pipeline.py
    │   └── transformations.py
    ├── database-setup
    │   ├── destinationdb.sql
    │   ├── sourcedb.sql
    │   └── storedb.sql
    ├── debugging
    │   └── logging.ini
    ├── dest-data
    │   └── .gitkeep
    ├── filesystem
    │   ├── raw
    │   │   └── .gitkeep
    │   └── stage
    │       ├── temp
    │       │   └── .gitkeep
    │       └── .gitkeep
    ├── great_expectations
    │   ├── checkpoints
    │   │   ├── retail_dest_checkpoint.yml
    │   │   ├── retail_load_checkpoint.yml
    │   │   ├── retail_source_checkpoint.yml
    │   │   ├── retail_transform_checkpoint.yml
    │   │   └── retail_warehouse_checkpoint.yml
    │   ├── expectations
    │   │   ├── .ge_store_backend_id
    │   │   ├── retail_dest_suite.json
    │   │   ├── retail_load_suite.json
    │   │   ├── retail_source_suite.json
    │   │   ├── retail_transform_suite.json
    │   │   ├── retail_warehouse_suite.json
    │   │   └── test_suite.json
    │   ├── uncommitted
    │   │   └── config_variables.yml
    │   ├── .gitignore
    │   ├── great_expectations.yml
    │   └── validations.json
    ├── source-data
    │   ├── retail_profiling.csv
    │   └── retail_validating.csv
    ├── .dockerignore
    ├── .gitattributes
    ├── .gitignore
    ├── airflow_conn.sh
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    └── setup.sh

