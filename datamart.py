from airflow import DAG
import pandas as pd
from airflow.hooks.base import BaseHook
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from os import getenv
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.sql.ddl import CreateSchema

with DAG (
         dag_id="SIMPLE",
         description="Dag to transfer data from csv to postgres",
         schedule_interval="@hourly",
         default_args={'start_date': datetime(2020, 1, 1), 'depends_on_past': False},
         is_paused_upon_creation=True,
         max_active_runs=1,
         catchup=False
         ) as dag:
    # создаем задачи для определения порядка выполнения задач
    start_task = DummyOperator(task_id='START', dag=dag)
    end_task = DummyOperator(task_id='END', dag=dag)

customer_table_name = "customer"
# создание задачи, которая будет выполняться в DAG
load_customer_raw_task = PythonOperator(
                            dag=dag,
                            # уникальный идентификатор задачи
                            task_id=f"{DAG_ID}.RAW.{customer_table_name}",
                            # функцию, которая будет вызываться в задаче
                            python_callable=load_csv_pandas,
                            # параметры для функции
                            op_kwargs = {
                                "table_name": customer_table_name,
                                "schema": "raw",
                                "conn_id": "raw_postgres"
                            }
                        )
# функция для загрузки данных из csv-файлов в базу данных Posgres
def load_csv_pandas(table_name: str, schema: str = "raw", conn_id: str = None) -> None:
    # создание объекта соединения с базой данных
    conn_object = BaseHook.get_connection(conn_id or DEFAULT_POSTGRES_CONN_ID)
    jdbc_url = f"postgresql://{conn_object.login}:{conn_object.password}@" \
               f"{conn_object.host}:{conn_object.port}/postgres"
    df = pd.read_csv(file_path)
    # создание движка базы данных
    engine = create_engine(jdbc_url)
    df.to_sql(table_name, engine, schema=schema, if_exists="append")

create_schema_raw = PythonOperator(
                        dag=dag,
                        # уникальный идентификатор задачи
                        task_id=f"{DAG_ID}.RAW.CREATE_SCHEMA",
                        # функция, которая будет вызываться в задаче
                        python_callable=create_schema,
                        # параметры для функции
                        op_kwargs = {
                            "conn_id": "raw_postgres",
                            "schemaName": "raw"
                        }
                    )
create_schema_datamart = PythonOperator(dag=dag,
                            task_id=f"{DAG_ID}.DATAMART.CREATE_SCHEMA",
                            python_callable=create_schema,
                            op_kwargs={
                                "conn_id": "datamart_postgres",
                                "schemaName": "datamart"
                            }
                        )
# функция для создания схемы в базе данных Postgres

def create_schema(conn_id, schemaName):
    conn_object = BaseHook.get_connection(conn_id or DEFAULT_POSTGRES_CONN_ID)
    jdbc_url = f"postgresql://{conn_object.login}:{conn_object.password}@" \
               f"{conn_object.host}:{conn_object.port}/postgres"
    engine = create_engine(jdbc_url)
    if not engine.dialect.has_schema(engine, schemaName):
        engine.execute(CreateSchema(schemaName))

customer_totals_datamart_task = PythonOperator(
                                                       dag=dag,
                                                       task_id=f"{DAG_ID}.DATAMART.{datamart_table}",
                                                       python_callable=datamart_pandas,
                                                       op_kwargs = {
                                                           "table_name": datamart_table,
                                                           "schema": "datamart",
                                                           "conn_id": "datamart_postgres"
                                                       }
                                                   )
# функция для создания витрины данных datamart
def datamart_pandas(table_name: str, schema: str = "datamart", conn_id: str = None) -> None:
    conn_object = BaseHook.get_connection(conn_id or DEFAULT_POSTGRES_CONN_ID)
    jdbc_url = f"postgresql://{conn_object.login}:{conn_object.password}@" \
               f"{conn_object.host}:{conn_object.port}/{conn_object.schema}"
    engine = create_engine(jdbc_url)
    query = open(f"{AIRFLOW_HOME}/sql/datamart.sql", 'r')
    df = pd.read_sql_query(query.read(), engine)
    df.to_sql(table_name, engine, schema=schema, if_exists="append")

start_task >>
create_schema_raw >>
create_schema_datamart >> [load_customer_raw_task,
                                               load_payments_raw_task,
                                               load_instance_raw_task,
                                               load_product_raw_task,
                                               load_costed_event_raw_task] >>
customer_totals_datamart_task >>
end_task