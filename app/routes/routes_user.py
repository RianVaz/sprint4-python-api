from flask import Blueprint, request, jsonify
import app.database as db

user_bp = Blueprint('user_bp', __name__)

#ADICIONAR USERS
@user_bp.route('/AdicionarUsuario/', methods=['GET'])
def endpoint_add_user():
    email = request.args.get('email')
    nome = request.args.get('nome')
    if not email or not nome:
        return jsonify({"erro": "Email e nome são obrigatórios."}), 400
    if db.add_user(email, nome):
        return jsonify({"mensagem": f"Usuário {nome} adicionado com sucesso."}), 201
    else:
        return jsonify({"erro": "Usuário com este email já existe."}), 409

#REMOVER USERS
@user_bp.route('/RemoverUsuario/', methods=['GET'])
def endpoint_remove_user():
    email = request.args.get('email')
    if not email:
        return jsonify({"erro": "Email é obrigatório."}), 400
    if db.remove_user(email):
        return jsonify({"mensagem": f"Usuário {email} e seus pontos foram removidos."}), 200
    else:
        return jsonify({"erro": "Usuário não encontrado."}), 404


#UPDATE USERS
@user_bp.route('/AlterarUsuario/', methods=['GET'])
def endpoint_update_user():
    """Altera o nome de um usuário existente."""
    email = request.args.get('email')
    # O novo nome virá pelo parâmetro 'nome'
    new_name = request.args.get('nome')

    # Validação para garantir que ambos os parâmetros foram enviados
    if not email or not new_name:
        return jsonify({"erro": "O email do usuário e o novo nome são obrigatórios."}), 400

    # Chama a função do banco de dados
    if db.update_user(email, new_name):
        return jsonify({"mensagem": "Usuário alterado com sucesso."}), 200
    else:
        # Se update_user retorna False, significa que o email não foi encontrado
        return jsonify({"erro": "Usuário não encontrado."}), 404


#LISTAR USERS
@user_bp.route('/ListarUsuarios/', methods=['GET'])
def endpoint_list_users():
    try:
        all_users = db.list_all_users()
        return jsonify(all_users), 200
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao buscar os usuários: {e}"}), 500