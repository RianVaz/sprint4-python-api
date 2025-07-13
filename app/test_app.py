import pytest # type: ignore
import os
from app import create_app
from app import database as db

@pytest.fixture
def client():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client

    # Código de limpeza executado após cada teste
    conn = db.get_db_connection()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE usuarios, pontos RESTART IDENTITY CASCADE")
    conn.commit()
    conn.close()
    os.environ.pop('FLASK_ENV', None)



# ----------------- Testes de Usuário -----------------

#def test_adicionar_usuario(client):
#    """Testa se um usuário pode ser adicionado com sucesso e se duplicatas são rejeitadas."""
#    # Act
#    resp = client.get('/AdicionarUsuario/?email=test@example.com&nome=Test User')
#    # Assert
#    assert resp.status_code == 201
#    # Act 2 (tentar adicionar o mesmo email)
#   resp_fail = client.get('/AdicionarUsuario/?email=test@example.com&nome=Another User')
#    # Assert 2
#    assert resp_fail.status_code == 409 # Conflict

def test_adicionar_usuario(client):#Teste POST
    """Testa se um usuário pode ser adicionado com sucesso via POST com JSON."""
    # Arrange
    user_data = {
        'email': 'test@example.com',
        'nome': 'Test User'
    }
    # Act: Faz a chamada POST para a nova URL '/usuarios',
    resp = client.post('/AdicionarUsuario', json=user_data) # passando os dados no parâmetro 'json'.
    # Assert:(201 Created)
    assert resp.status_code == 201
    # Act 2: Tenta adicionar o mesmo usuário novamente
    resp_fail = client.post('/AdicionarUsuario', json=user_data)
    # Assert 2:(409 Conflict)
    assert resp_fail.status_code == 409

def test_listar_usuarios(client):
    """Testa se a lista de usuários é retornada corretamente."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=user1@example.com&nome=Alice')
    #client.get('/AdicionarUsuario/?email=user2@example.com&nome=Bob')
    client.post('/AdicionarUsuario', json={'email': 'user1@example.com', 'nome': 'Alice'})
    client.post('/AdicionarUsuario', json={'email': 'user2@example.com', 'nome': 'Bob'})
    # Act
    resp = client.get('/ListarUsuarios/')
    # Assert
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    assert data[0]['nome'] == 'Alice' # A lista é ordenada por nome
    assert data[1]['nome'] == 'Bob'

def test_alterar_usuario(client):
    """Testa se o nome de um usuário pode ser alterado."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=user.to.update@example.com&nome=Nome Antigo')
    client.post('/AdicionarUsuario', json={'email': 'user.to.update@example.com', 'nome': 'Nome Antigo'})
    # Act
    resp = client.get('/AlterarUsuario/?email=user.to.update@example.com&nome=Nome Novo')
    # Assert
    assert resp.status_code == 200
    # Assert 2 (Verificar se a alteração realmente aconteceu)
    resp_list = client.get('/ListarUsuarios/')
    data = resp_list.get_json()
    assert len(data) == 1
    assert data[0]['nome'] == 'Nome Novo'
    
def test_remover_usuario(client):
    """Testa se um usuário pode ser removido."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=user.to.delete@example.com&nome=ToDelete')
    client.post('/AdicionarUsuario', json={'email': 'user.to.delete@example.com', 'nome': 'ToDelete'})
    # Act
    resp = client.get('/RemoverUsuario/?email=user.to.delete@example.com')
    # Assert
    assert resp.status_code == 200
    # Assert 2 (Verificar se o usuário foi mesmo removido)
    resp_list = client.get('/ListarUsuarios/')
    assert len(resp_list.get_json()) == 0



# ----------------- Testes de Ponto -----------------

def test_adicionar_ponto(client):
    """Testa se um ponto pode ser adicionado a um usuário existente."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=ponto.user@example.com&nome=Ponto User')
    client.post('/AdicionarUsuario', json={'email': 'ponto.user@example.com', 'nome': 'Ponto User'})
    # Act
    resp = client.get('/AdicionarPonto/?latitude=-19.9&longitude=-43.9&descricao=Meu Ponto&email=ponto.user@example.com')
    # Assert
    assert resp.status_code == 201
    assert 'id_ponto' in resp.get_json()

def test_listar_pontos(client):
    """Testa a listagem de pontos de um usuário."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=ponto.user@example.com&nome=Ponto User')
    client.post('/AdicionarUsuario', json={'email': 'ponto.user@example.com', 'nome': 'Ponto User'})
    client.get('/AdicionarPonto/?latitude=1&longitude=1&descricao=Ponto 1&email=ponto.user@example.com')
    client.get('/AdicionarPonto/?latitude=2&longitude=2&descricao=Ponto 2&email=ponto.user@example.com')
    # Act
    resp = client.get('/ListarPontos/?email=ponto.user@example.com')
    # Assert
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2

def test_alterar_ponto(client):
    """Testa a alteração de um ponto existente."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=ponto.user@example.com&nome=Ponto User')
    client.post('/AdicionarUsuario', json={'email': 'ponto.user@example.com', 'nome': 'Ponto User'})
    resp_add = client.get('/AdicionarPonto/?latitude=1&longitude=1&descricao=Descricao Antiga&email=ponto.user@example.com')
    point_id = resp_add.get_json()['id_ponto']
    # Act
    resp_update = client.get(f'/AlterarPonto/?id={point_id}&latitude=1.1&longitude=1.1&descricao=Descricao Nova')
    # Assert
    assert resp_update.status_code == 200
    # Assert 2 (Verificar se a alteração realmente aconteceu)
    resp_list = client.get('/ListarPontos/?email=ponto.user@example.com')
    data = resp_list.get_json()
    assert data[0]['descricao'] == 'Descricao Nova'

def test_remover_ponto(client):
    """Testa a remoção de um ponto."""
    # Arrange
    #client.get('/AdicionarUsuario/?email=ponto.user@example.com&nome=Ponto User')
    client.post('/AdicionarUsuario', json={'email': 'ponto.user@example.com', 'nome': 'Ponto User'})
    resp_add = client.get('/AdicionarPonto/?latitude=1&longitude=1&descricao=Ponto a ser deletado&email=ponto.user@example.com')
    point_id = resp_add.get_json()['id_ponto']
    # Act
    resp_remove = client.get(f'/RemoverPonto/?id={point_id}')
    # Assert
    assert resp_remove.status_code == 200
    # Assert 2 (Verificar se o ponto foi mesmo removido)
    resp_list = client.get('/ListarPontos/?email=ponto.user@example.com')
    assert len(resp_list.get_json()) == 0
