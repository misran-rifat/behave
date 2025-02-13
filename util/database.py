import logging
import os

import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_postgres():
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    dbname = os.environ.get('POSTGRES_DB')
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT', '5432')

    if not (user and password and dbname and host):
        logging.error("Environment variables for PostgreSQL connection are not fully set.")
        raise ValueError("Environment variables for PostgreSQL connection are not fully set.")

    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        logging.info("Successfully connected to PostgreSQL DB")
        return connection
    except psycopg2.OperationalError as e:
        logging.error(f"Error connecting to PostgreSQL DB: {e}")
        return None
