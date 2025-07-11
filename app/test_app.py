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

def test_gerenciamento_de_pontos(client):
    client.get('/AdicionarUsuario/?email=ponto.user@example.com&nome=Ponto User')
    resp_add = client.get('/AdicionarPonto/?latitude=-19.9167&longitude=-43.9345&descricao=Praca Sete&email=ponto.user@example.com')
    assert resp_add.status_code == 201
    point_id = resp_add.get_json()['id_ponto']
    resp_list = client.get('/ListarPontos/?email=ponto.user@example.com')
    assert len(resp_list.get_json()) == 1
    client.get(f'/AlterarPonto/?id={point_id}&latitude=-19.9200&longitude=-43.9400&descricao=Mercado Central')
    resp_list_after = client.get('/ListarPontos/?email=ponto.user@example.com')
    assert resp_list_after.get_json()[0]['descricao'] == 'Mercado Central'
    resp_remove = client.get(f'/RemoverPonto/?id={point_id}')
    assert resp_remove.status_code == 200
    assert len(client.get('/ListarPontos/?email=ponto.user@example.com').get_json()) == 0
