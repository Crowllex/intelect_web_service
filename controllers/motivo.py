
from flask import Blueprint, app, request, jsonify
from models.motivo import Motivo
import json
from middlewares.validar_token import validate_token

route_motivo = Blueprint('route_motivo', __name__)

@route_motivo.route('/motivo/listar', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        objProd = Motivo()
        rptaJson = objProd.listarMotivo()
        datos_motivo = json.loads(rptaJson) 
        return jsonify(datos_motivo), 200 
