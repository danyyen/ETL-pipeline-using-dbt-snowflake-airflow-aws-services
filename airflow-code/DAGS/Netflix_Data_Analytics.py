# =========================
# IMPORTS
# =========================
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from alerting.slack_alert import task_fail_slack_alert, task_success_slack_alert
from alerting.sns_alert import send_sns_failure_alert

import sys
sys.path.append('/home/airflow/airflow-code/DAGS')

from source_load.data_load import run_script
from alerting.slack_alert import (
    task_fail_slack_alert,
    task_success_slack_alert
)

# =========================
# DEFAULT ARGS
# =========================
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# =========================
# DAG DEFINITION
# (SLACK ALERTS LIVE HERE)
# =========================

dag = DAG(
    dag_id="Netflix_Data_Analytics",
    default_args=default_args,
    description='End-to-end ELT pipeline using Airflow, Snowflake, dbt, and AWS',
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=lambda context: (
        task_fail_slack_alert(context),
        send_sns_failure_alert(context),
    ),                                             # 🔴 DAG FAILURE
    on_success_callback=task_success_slack_alert,  # 🟢 DAG SUCCESS
)

# =========================
# TASKS
# =========================
start_task = DummyOperator(
    task_id='start_task',
    dag=dag
)

credits_sensor = S3KeySensor(
    task_id='credits_rawfile_sensor',
    bucket_key='raw_files/credits.csv',
    bucket_name='netflix-data-analytics-2025-etl',
    aws_conn_id='aws_default',
    poke_interval=300,
    timeout=60 * 60 * 24 * 7,
    mode='reschedule',
    dag=dag
)

titles_sensor = S3KeySensor(
    task_id='titles_rawfile_sensor',
    bucket_key='raw_files/titles.csv',
    bucket_name='netflix-data-analytics-2025-etl',
    aws_conn_id='aws_default',
    poke_interval=300,
    timeout=60 * 60 * 24 * 7,
    mode='reschedule',
    dag=dag
)

load_data_snowflake = PythonOperator(
    task_id='Load_Data_Snowflake',
    python_callable=run_script,
    dag=dag
)

run_stage_models = BashOperator(
    task_id='run_stage_models',
    bash_command=(
        '/home/airflow/dbt-env/bin/dbt run '
        '--select tag:"DIMENSION" '
        '--project-dir /home/airflow/dbt_etl_code '
        '--profile Netflix '
        '--target dev'
    ),
    retries=2,
    retry_delay=timedelta(minutes=3),
    dag=dag
)

run_fact_dim_models = BashOperator(
    task_id='run_fact_dim_models',
    bash_command=(
        '/home/airflow/dbt-env/bin/dbt run '
        '--select tag:"FACT" '
        '--project-dir /home/airflow/dbt_etl_code '
        '--profile Netflix '
        '--target prod'
    ),
    retries=2,
    retry_delay=timedelta(minutes=3),
    dag=dag
)

run_test_cases = BashOperator(
    task_id='run_test_cases',
    bash_command=(
        '/home/airflow/dbt-env/bin/dbt test '
        '--select tag:"TEST" '
        '--project-dir /home/airflow/dbt_etl_code '
        '--profile Netflix '
        '--target prod'
    ),
    retries=2,
    retry_delay=timedelta(minutes=3),
    dag=dag
)

from airflow.exceptions import AirflowFailException
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule


def force_fail():
    raise AirflowFailException("Upstream task failed — failing DAG")


end_task = PythonOperator(
    task_id="end_task",
    python_callable=force_fail,
    trigger_rule=TriggerRule.ONE_FAILED,
    dag=dag,
)

# =========================
# DEPENDENCIES
# =========================
start_task >> [credits_sensor, titles_sensor] \
>> load_data_snowflake \
>> run_stage_models \
>> run_fact_dim_models \
>> run_test_cases \
>> end_task

