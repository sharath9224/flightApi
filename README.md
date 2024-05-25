# Real-Time ETL Pipeline with Docker, Python, PostgreSQL, Airflow, Kafka, and Flink

## Overview

This project implements a real-time ETL (Extract, Transform, Load) pipeline using various technologies including Docker, Python, PostgreSQL, Airflow, Kafka, and Flink. The pipeline fetches real-time flight data from the Airlabs API, processes the data using Flink, and stores the processed data in a PostgreSQL database. Airflow orchestrates the entire process.

## Project Structure

etl_project/
├── docker-compose.yaml
├── .env
├── dags/
│ └── load_kafka_to_postgres.py
├── scripts/
│ └── fetch_airlabs_data.py
├── flink/
│ └── flink_job.py
├── init.sql
├── logs/
├── plugins/
├── README.md
└── requirements.txt

## Prerequisites

- Docker and Docker Compose installed
- Python 3.x installed
- An API key from aviationstack API([(https://aviationstack.com/)]

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/etl_project.git
cd etl_project
2. Create a .env File
Create a .env file in the root directory with the following content:

env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=airlabs
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

# Backend DB - update your username and password
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgres:your_postgres_password@postgres/airlabs
AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=False

# Airflow Init
_AIRFLOW_DB_UPGRADE=True
_AIRFLOW_WWW_USER_CREATE=True
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin_password

# Airflow UID
AIRFLOW_UID=50000  # or any appropriate UID for your setup
3. Initialize PostgreSQL
Ensure init.sql contains the necessary SQL commands to set up your database:
CREATE ROLE airflow WITH LOGIN PASSWORD 'airflow_password';
ALTER ROLE airflow CREATEDB;

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    data JSONB
);
docker-compose up -d
Usage
1. Run Data Fetching Script
Run the data fetching script to fetch data from the Airlabs API and send it to Kafka:

sh
Copy code
python scripts/fetch_airlabs_data.py
2. Monitor Airflow
Access the Airflow web interface at http://localhost:8080 and ensure your DAG (load_kafka_to_postgres) is running. Enable the DAG if it is not already enabled.

3. Deploy and Monitor Flink Job
Submit the Flink job via the Flink Web UI at http://localhost:8081.


Components
1. Docker Compose
The docker-compose.yaml file defines the setup for all services including Zookeeper, Kafka, PostgreSQL, Flink, and Airflow.

2. Airflow DAG
The Airflow DAG (dags/load_kafka_to_postgres.py) loads data from Kafka to PostgreSQL.

3. Data Fetching Script
The script (scripts/fetch_airlabs_data.py) fetches data from the Airlabs API and sends it to Kafka.

4. Flink Job
The Flink job (flink/flink_job.py) processes data from Kafka.
