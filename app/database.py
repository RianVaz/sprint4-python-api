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
                id SERIAL PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                descricao TEXT NOT NULL,
                user_email TEXT NOT NULL REFERENCES usuarios(email) ON DELETE CASCADE,
                geom GEOMETRY(Point, 4326) NOT NULL
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

def update_user(email, new_name):
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Executa o comando SQL UPDATE
        cur.execute('UPDATE usuarios SET nome = %s WHERE email = %s', (new_name, email))
        # cur.rowcount retorna o número de linhas que foram alteradas.
        # Se for > 0, a atualização foi bem-sucedida.
        changes = cur.rowcount
    conn.commit()
    conn.close()
    return changes > 0

def find_user(email):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user = cur.fetchall()
    conn.close()
    return user

def list_all_users():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute('SELECT email, nome FROM usuarios ORDER BY nome ASC')
        users = cur.fetchall()
    conn.close()
    return [dict(user) for user in users]



# --- FUNÇÕES DE PONTOS ---


def add_point(latitude, longitude, descricao, user_email):
    if not find_user(user_email):
        return None  # Usuário não existe
    
    wkt_point = f"POINT({longitude} {latitude})"

    conn = get_db_connection()
    new_point_id = None
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO pontos (latitude, longitude, descricao, user_email, geom) VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326)) RETURNING id',
            (latitude, longitude, descricao, user_email, wkt_point)
        )
        new_point_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return new_point_id

def list_points_by_user(user_email):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        # Adicionamos a coluna wkt_point ao SELECT
        cur.execute('SELECT id, latitude, longitude, descricao, ST_AsText(geom) as geom FROM pontos WHERE user_email = %s', (user_email,))
        points = cur.fetchall()
    conn.close()
    return [dict(point) for point in points]

def update_point(point_id, latitude, longitude, descricao):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            'UPDATE pontos SET latitude = %s, longitude = %s, descricao = %s WHERE id = %s',
            (latitude, longitude, descricao, point_id)
        )
        changes = cur.rowcount
    conn.commit()
    conn.close()
    return changes > 0

def remove_point(point_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('DELETE FROM pontos WHERE id = %s', (point_id,))
        changes = cur.rowcount
    conn.commit()
    conn.close()
    return changes > 0