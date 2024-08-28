from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.email import send_email
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../models")))
from teddy360 import Teddy360


def fetch_data(**kwargs):
    url = "https://jsonplaceholder.typicode.com/todos/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ValueError("Failed to fetch data from API")


def store_data(**kwargs):
    data = kwargs["task_instance"].xcom_pull(task_ids="fetch_data")

    connection = BaseHook.get_connection("postgres_conn")

    connection_string = (
        f"postgresql://{connection.login}:{connection.password}@"
        f"{connection.host}:{connection.port}/{connection.schema}"
    )
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)

    session = Session()

    for item in data:
        if item["completed"]:
            teddy_item = Teddy360(
                id=item["id"],
                userId=item["userId"],
                title=item["title"],
                completed=item["completed"],
            )
            session.merge(teddy_item)

    session.commit()
    session.close()


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    "teddy_dag",
    default_args=default_args,
    description="A DAG to fetch data from API and store it in Postgres using SQLAlchemy",
    catchup=False,
) as dag:

    fetch_data_task = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_data,
        provide_context=True,
    )

    store_data_task = PythonOperator(
        task_id="store_data",
        python_callable=store_data,
        provide_context=True,
    )

    fetch_data_task >> store_data_task
