from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv('./.env') 

def run_create_schema_sql():
    with open("./scripts/create_schema.sql", "r") as f:
        sql = f.read()
    conn = psycopg2.connect(
        host="postgres",
        database="churn_dw",
        user="airflow",
        password="airflow",
        port=5432,
    )
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def ingest_csv_to_staging():
    df = pd.read_csv('./data/customer_churn_data.csv')
    conn_str = "postgresql://airflow:airflow@postgres:5432/churn_dw"
    engine = create_engine(conn_str)
    df.to_sql('churn_raw', con=engine, schema='staging', index=False, if_exists='replace')

def create_dag():
    with DAG(
        dag_id="churn_pipeline_dag",
        schedule_interval="@hourly",
        start_date=days_ago(1),
        catchup=False,
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(seconds=10)
        }
    ) as dag:

        init_schema = PythonOperator(
            task_id="create_schema",
            python_callable=run_create_schema_sql
        )

        load_csv = PythonOperator(
            task_id="ingest_csv",
            python_callable=ingest_csv_to_staging
        )

        init_schema >> load_csv

    return dag

globals()['churn_pipeline_dag'] = create_dag()
