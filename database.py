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


# --- FUNÇÔES DE USUÁRIOS ---

def add_user(email, nome):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO usuarios (email, nome) VALUES (%s, %s)', (email, nome))
        conn.commit()
    except psycopg2.IntegrityError:
        return False  # Usuário já existe
    finally:    
        conn.close()
    return True  # Usuário adicionado com sucesso

def remove_user(email):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('DELETE FROM usuarios WHERE email = %s', (email,))
        changes = cur.rowcount
    conn.commit()
    conn.close()
    return changes > 0  # Retorna True se o usuário foi removido

def find_user(email):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT email, nome FROM ususarios ORDER BY nome ASC')
        users = cur.fetchall()
    conn.close()
    return [dict(user) for user in users]  # Retorna lista de dicionários com os usuários