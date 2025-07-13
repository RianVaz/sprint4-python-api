# app/routes_point.py
from flask import Blueprint, request, jsonify # type: ignore
import app.database as db

point_bp = Blueprint('point_bp', __name__)

#ADD POINT
@point_bp.route('/AdicionarPonto/', methods=['GET'])
def endpoint_add_point():
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({"erro": "Latitude e longitude são obrigatórias e devem ser números."}), 400
    descricao = request.args.get('descricao')
    user_email = request.args.get('email')
    if not descricao or not user_email:
        return jsonify({"erro": "Descrição e email do usuário são obrigatórios."}), 400
    point_id = db.add_point(latitude, longitude, descricao, user_email)
    if point_id:
        return jsonify({"mensagem": "Ponto adicionado com sucesso!", "id_ponto": point_id}), 201
    else:
        return jsonify({"erro": "Usuário não encontrado. Não foi possível adicionar o ponto."}), 404
    
#REMOVE POINT
@point_bp.route('/RemoverPonto/', methods=['GET'])
def endpoint_remove_point():
    point_id = request.args.get('id')
    if not point_id:
        return jsonify({"erro": "O ID do ponto é obrigatório."}), 400
    if db.remove_point(point_id):
        return jsonify({"mensagem": "Ponto removido com sucesso."}), 200
    else:
        return jsonify({"erro": "Ponto não encontrado."}), 404

#LIST POINTS BY USER
@point_bp.route('/ListarPontos/', methods=['GET'])
def endpoint_list_points():
    user_email = request.args.get('email')
    if not user_email:
        return jsonify({"erro": "O email do usuário é obrigatório."}), 400
    if not db.find_user(user_email):
        return jsonify({"erro": "Usuário não encontrado."}), 404
    pontos = db.list_points_by_user(user_email)
    return jsonify(pontos), 200

#UPDATE POINTS
@point_bp.route('/AlterarPonto/', methods=['GET'])
def endpoint_update_point():
    point_id = request.args.get('id')
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({"erro": "Latitude e longitude são obrigatórias e devem ser números."}), 400
    descricao = request.args.get('descricao')
    if not all([point_id, latitude, longitude, descricao]):
        return jsonify({"erro": "ID do ponto, latitude, longitude e descrição são obrigatórios."}), 400
    if db.update_point(point_id, latitude, longitude, descricao):
        return jsonify({"mensagem": "Ponto alterado com sucesso."}), 200
    else:
        return jsonify({"erro": "Ponto não encontrado."}), 404
