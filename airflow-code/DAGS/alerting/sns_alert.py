import boto3


def send_sns_failure_alert(context):
    """
    Publishes a failure message to SNS when a DAG fails.
    """
    dag_id = context["dag"].dag_id
    execution_date = context.get("execution_date")
    ti = context.get("task_instance")

    message = f"""
AIRFLOW DAG FAILURE 🚨

DAG: {dag_id}
Task: {ti.task_id}
Execution Time: {execution_date}
Log URL: {ti.log_url}
"""

    sns_client = boto3.client("sns", region_name="us-east-1")

    sns_client.publish(
        TopicArn="arn:aws:sns:us-east-1:143176219551:Airflow_Failure",
        Subject=f"Airflow DAG Failed: {dag_id}",
        Message=message,
    )
