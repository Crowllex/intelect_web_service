
from flask import Blueprint, app, request, jsonify
from models.rubro import Rubro
import json
from middlewares.validar_token import validate_token

route_rubro = Blueprint('route_rubro', __name__)


@route_rubro.route('/rubro/listar', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        objProd = Rubro()
        rptaJson = objProd.listarRubro()
        datos_rubro = json.loads(rptaJson)
        return jsonify(datos_rubro), 200
