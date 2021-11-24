
from flask import Blueprint, app, request, jsonify
from models.anticipo import Anticipo
import json
from middlewares.validar_token import validate_token

route_anticipo = Blueprint('route_anticipo', __name__)

@route_anticipo.route('/anticipo/listarAnticipoPendientePorDocente', methods=['POST'])
@validate_token
def listar():
    if request.method == 'POST':
        id_personal = request.form['id_personal']
        objProd = Anticipo()
        rptaJson = objProd.listarAnticipoPendientePorDocente(id_personal)
        datos_anticipo = json.loads(rptaJson) 
        return jsonify(datos_anticipo), 200 
