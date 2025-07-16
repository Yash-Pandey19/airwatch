from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)

from transformations import transform_raw_data, root_path, date, transform_stage_data

default_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime.now(),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="retail_data_pipeline",
    default_args=default_args,
    schedule_interval="0 16 * * *",
    max_active_runs=1,
)

# ✅ Replace validate_checkpoint with GreatExpectationsOperator
validate_retail_source_data = GreatExpectationsOperator(
    task_id="validate_retail_source_data",
    checkpoint_name="retail_source_checkpoint",
    data_context_root_dir="/opt/airflow/great_expectations",
    fail_task_on_validation_failure=True,
    do_xcom_push=False,
    dag=dag,
)

extract_load_retail_source = PostgresOperator(
    dag=dag,
    task_id="extract_load_retail_source",
    sql="./scripts/sql/extract_load_retail_source.sql",
    postgres_conn_id="postgres_source",
    params={"to_raw": f"/filesystem/raw/retail_profiling-{date}.csv"},
)

validate_retail_raw_data = GreatExpectationsOperator(
    task_id="validate_retail_raw_data",
    checkpoint_name="retail_load_checkpoint",
    data_context_root_dir="/opt/airflow/great_expectations",
    fail_task_on_validation_failure=True,
    do_xcom_push=False,
    dag=dag,
)

transform_load_retail_raw = PythonOperator(
    dag=dag,
    task_id="transform_load_retail_raw",
    python_callable=transform_raw_data,
    op_kwargs={
        "output_loc": f"{root_path}/filesystem/stage/retail_profiling-{date}.snappy.parquet",
    },
)

validate_retail_stage_data = GreatExpectationsOperator(
    task_id="validate_retail_stage_data",
    checkpoint_name="retail_transform_checkpoint",
    data_context_root_dir="/opt/airflow/great_expectations",
    fail_task_on_validation_failure=True,
    do_xcom_push=False,
    dag=dag,
)

transform_retail_stage = PythonOperator(
    dag=dag,
    task_id="transform_retail_stage",
    python_callable=transform_stage_data,
    op_kwargs={
        "output_loc": f"{root_path}/filesystem/stage/temp/retail_profiling-{date}.csv"
    },
)

load_retail_stage = PostgresOperator(
    dag=dag,
    task_id="load_retail_stage",
    sql="./scripts/sql/load_retail_stage.sql",
    postgres_conn_id="postgres_dest",
    params={"from_stage": f"/filesystem/stage/temp/retail_profiling-{date}.csv"},
)

validate_retail_warehouse_data = GreatExpectationsOperator(
    task_id="validate_retail_warehouse_data",
    checkpoint_name="retail_warehouse_checkpoint",
    data_context_root_dir="/opt/airflow/great_expectations",
    fail_task_on_validation_failure=True,
    do_xcom_push=False,
    dag=dag,
)

transform_load_retail_warehouse = PostgresOperator(
    task_id="transform_load_retail_warehouse",
    sql="./scripts/sql/transform_load_retail_warehouse.sql",
    postgres_conn_id="postgres_dest",
    dag=dag,
)

validate_retail_dest_data = GreatExpectationsOperator(
    task_id="validate_retail_dest_data",
    checkpoint_name="retail_dest_checkpoint",
    data_context_root_dir="/opt/airflow/great_expectations",
    fail_task_on_validation_failure=True,
    do_xcom_push=False,
    dag=dag,
)

end_of_data_pipeline = DummyOperator(task_id="end_of_data_pipeline", dag=dag)

# DAG Task Flow
(
    validate_retail_source_data
    >> extract_load_retail_source
    >> validate_retail_raw_data
    >> transform_load_retail_raw
    >> validate_retail_stage_data
    >> transform_retail_stage
    >> load_retail_stage
    >> validate_retail_warehouse_data
    >> transform_load_retail_warehouse
    >> validate_retail_dest_data
    >> end_of_data_pipeline
)
