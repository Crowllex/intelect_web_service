from flask import Blueprint, request, jsonify
from models.evaluacion_rendicion_gastos import Ev_rendicion_gastos
from middlewares.validar_token import validate_token
import json


route_erg = Blueprint('route_erg', __name__)


@route_erg.route('/erg/register', methods=['POST'])
@validate_token
def registrar_erg():
    if request.method == 'POST':
        observacion = request.form['observacion']
        id_rendicion_gastos = request.form['id_rendicion_gastos']
        id_usuario = request.form['id_usuario']
        id_estado_eval_rendicion = request.form['id_estado_eval_rendicion']
        obj_erg = Ev_rendicion_gastos(
            observacion, id_rendicion_gastos, id_usuario, id_estado_eval_rendicion)
        rpta_json = obj_erg.insertar()
        data_erg = json.loads(rpta_json)
        return jsonify(data_erg), 200
