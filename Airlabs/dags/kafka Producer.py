from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import psycopg2
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('load_kafka_to_postgres', default_args=default_args, schedule_interval=timedelta(minutes=1))

def load_to_postgres():
    consumer = KafkaConsumer('processed_airlabs_data', bootstrap_servers='localhost:9092', auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    conn = psycopg2.connect("dbname='airlabs' user='postgres' host='postgres' password='postgres'")
    cur = conn.cursor()
    
    for message in consumer:
        data = message.value
        # Insert data into PostgreSQL (adjust the SQL based on your data structure)
        cur.execute("INSERT INTO flights (data) VALUES (%s)", (json.dumps(data),))
        conn.commit()
    cur.close()
    conn.close()

load_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag,
)

load_task
