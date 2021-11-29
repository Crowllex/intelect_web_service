
from flask import Blueprint, request, jsonify
from models.tipo_comprobante import Tipo_Comprobante
import json
from middlewares.validar_token import validate_token

route_tipo_comprobante = Blueprint('route_tipo_comprobante', __name__)


@route_tipo_comprobante.route('/tipo_comprobante/list', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        objTipo = Tipo_Comprobante()
        rptaJson = objTipo.listar()
        datos_tipo_comprobante = json.loads(rptaJson)
        return jsonify(datos_tipo_comprobante), 200
