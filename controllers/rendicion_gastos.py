
from flask import Blueprint, request, jsonify
from models.rendicion_gastos import Rendicion_gastos
from middlewares.validar_token import validate_token
import json


route_rg = Blueprint('route_rg', __name__)


@route_rg.route('/rg/register', methods=['POST'])
@validate_token
def registrar_rg():
    if request.method == 'POST':
        id_estado_rendicion = request.form['id_estado_rendicion']
        id_anticipo = request.form['id_anticipo']
        obj_rg = Rendicion_gastos(id_estado_rendicion, id_anticipo)
        rpta_json = obj_rg.insertar()
        data_rg = json.loads(rpta_json)
        return jsonify(data_rg), 200
