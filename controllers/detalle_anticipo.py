
from flask import Blueprint, app, request, jsonify
from models.detalle_anticipo import DetalleAnticipo
import json
from middlewares.validar_token import validate_token

route_detalleAnt = Blueprint('route_detalle_anticipo', __name__)


@route_comprobante.route('/anticipo/detalle', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        id_anticipo = request.form['id_anticipo']
        objProd = DetalleAnticipo(id_anticipo)
        rptaJson = objProd.listarDetalleAnticipo()
        datos_comprobante = json.loads(rptaJson)
        return jsonify(datos_comprobante), 200