
from flask import Blueprint, app, request, jsonify
from models.rendicion import Rendicion
import json
from middlewares.validar_token import validate_token

route_rendicion = Blueprint('route_rendicion', __name__)

@route_rendicion.route('/rendicion/listar', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        objProd = Rendicion()
        rptaJson = objProd.listarRendicion()
        datos_rendicion = json.loads(rptaJson) 
        return jsonify(datos_rendicion), 200 
