
from airflow.hooks.base import BaseHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

def task_fail_slack_alert(context):
    ti = context["task_instance"]

    SlackWebhookOperator(
        task_id="slack_failed_alert",
        slack_webhook_conn_id="Slack_Connection",
        message=f"""
:red_circle: *Airflow Task Failed*
*DAG*: {ti.dag_id}
*Task*: {ti.task_id}
*Execution Time*: {context.get('execution_date')}
*Log URL*: {ti.log_url}
""",
    ).execute(context=context)


def task_success_slack_alert(context):
    ti = context["task_instance"]

    SlackWebhookOperator(
        task_id="slack_success_alert",
        slack_webhook_conn_id="Slack_Connection",
        message=f"""
:large_green_circle: *Airflow Task Succeeded*
*DAG*: {ti.dag_id}
*Task*: {ti.task_id}
*Execution Time*: {context.get('execution_date')}
""",
    ).execute(context=context)

