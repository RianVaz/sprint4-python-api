import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import uuid

load_dotenv() #carrega variáveis de ambiente do arquivo .env

def get_db_connection():
    is_testing = os.getenv('FLASK_ENV') == 'testing'
    db_name = os.getenv('TEST_DB_NAME') if is_testing else os.getenv('DB_NAME')
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=db_name,
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    return conn

def init_db():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios ( 
                email TEXT PRIMARY KEY,
                nome TEXT NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pontos (
                id TEXT PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                descricao TEXT NOT NULL,
                user_email TEXT NOT NULL REFERENCES usuarios(email) ON DELETE CASCADE
            )
        ''')
    conn.commit()
    conn.close()
