
from flask import Blueprint, app, request, jsonify
from models.sede import Sede
from middlewares.validar_token import validate_token
import json

route_sede = Blueprint('route_sede', __name__)


@route_sede.route('/sede/listar', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        objProd = Sede()
        rptaJson = objProd.listarSede()
        datos_sede = json.loads(rptaJson)
        return jsonify(datos_sede), 200
