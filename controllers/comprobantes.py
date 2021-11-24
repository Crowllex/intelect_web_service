
from flask import Blueprint, app, request, jsonify
from models.comprobantes import Comprobante
import json
from middlewares.validar_token import validate_token


route_comprobante = Blueprint('route_comprobante', __name__)


@route_comprobante.route('/comprobante/listar', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        objProd = Comprobante()
        rptaJson = objProd.listarComprobante(id_usuario)
        datos_comprobante = json.loads(rptaJson)
        print(datos_comprobante)
        return jsonify(datos_comprobante), 200
