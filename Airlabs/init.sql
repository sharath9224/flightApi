CREATE ROLE airflow WITH LOGIN PASSWORD 'airflow_password';
ALTER ROLE airflow CREATEDB;

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    data JSONB
);
