import pandas as pd
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas
import boto3

# Initialize AWS clients for SSM and S3 in the same region
ssm = boto3.client('ssm', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

# --- Retrieve Snowflake Credentials from AWS Systems Manager ---
# NOTE: The EC2 IAM role must have ssm:GetParameter access to these resources.
sf_username = ssm.get_parameter(Name='/snowflake/username', WithDecryption=True)['Parameter']['Value']
sf_password = ssm.get_parameter(Name='/snowflake/password', WithDecryption=True)['Parameter']['Value']
sf_account  = ssm.get_parameter(Name='/snowflake/accountname', WithDecryption=True)['Parameter']['Value']


def run_script():
    """
    The main callable function executed by the Airflow PythonOperator.
    It orchestrates the truncate and load processes for titles and credits data.
    """
    # Module to create the Snowflake connection and return the connection objects
    def create_connection():
        conn = snow.connect(
            user=sf_username,
            password=sf_password,
            account=sf_account,
            warehouse="COMPUTE_WH",
            database="DBT_PROJECT_DB",  # Confirmed database name
            schema="DBT_RAW"            # Confirmed schema name
        )
        cursor = conn.cursor()
        print('SQL Connection Created')
        return cursor, conn

    # Module to truncate the tables if they exist to prevent duplicate loading
    def truncate_table():
        cur, conn = create_connection()
        
        # Note: You should check if TITLES_RAW/CREDITS_RAW are the correct table names
        sql_titles = "TRUNCATE TABLE IF EXISTS TITLES_RAW"
        sql_credits = "TRUNCATE TABLE IF EXISTS CREDITS_RAW"
        
        cur.execute(sql_titles)
        cur.execute(sql_credits)
        print('Tables truncated')
        
        cur.close()
        conn.close()

    # Module to read CSV files from S3 and load data into Snowflake
    def load_data():
        # Get S3 objects using the updated, unique bucket name
        titles_file = s3.get_object(Bucket='netflix-data-analytics-2025-etl', Key='raw_files/titles.csv')
        credits_file = s3.get_object(Bucket='netflix-data-analytics-2025-etl', Key='raw_files/credits.csv')
        
        cur, conn = create_connection()
        delimiter = ","

        # Read files directly from S3 object body into Pandas DataFrame
        titles_df = pd.read_csv(titles_file['Body'], sep=delimiter)
        print("Titles file read")
        credits_df = pd.read_csv(credits_file['Body'], sep=delimiter)
        print("Credits file read")

        # Load DataFrames into Snowflake tables, creating them if necessary
        write_pandas(conn, titles_df, "TITLES_RAW", auto_create_table=True)
        print('Titles file loaded')
        write_pandas(conn, credits_df, "CREDITS_RAW", auto_create_table=True)
        print('Credits file loaded')

        # Close your cursor and your connection
        cur.close()
        conn.close()

    print("Starting Script")
    truncate_table()
    load_data()
