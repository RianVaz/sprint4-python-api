import pytest
import os
from app import create_app
import app.database as db

@pytest.fixture
def client():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client

    conn = db.get_db_connection()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE usuarios, pontos RESTART IDENTITY CASCADE")
    conn.commit()
    conn.close()
    os.environ.pop('FLASK_ENV', None)

def test_adicionar_e_remover_usuario(client):
    resp_add = client.get('/AdicionarUsuario/?email=test@example.com&nome=Test User')
    assert resp_add.status_code == 201
    resp_add_fail = client.get('/AdicionarUsuario/?email=test@example.com&nome=Test User')
    assert resp_add_fail.status_code == 409
    resp_remove = client.get('/RemoverUsuario/?email=test@example.com')
    assert resp_remove.status_code == 200
    resp_remove_fail = client.get('/RemoverUsuario/?email=nonexistent@example.com')
    assert resp_remove_fail.status_code == 404

def test_listar_usuarios(client):
    client.get('/AdicionarUsuario/?email=user1@example.com&nome=Alice')
    client.get('/AdicionarUsuario/?email=user2@example.com&nome=Bob')
    resp = client.get('/ListarUsuarios/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    nomes = {user['nome'] for user in data}
    assert 'Alice' in nomes
    assert 'Bob' in nomes