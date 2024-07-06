import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST')
}

def connect_to_db(params=db_params):
    conn = psycopg2.connect(**params)
    return conn