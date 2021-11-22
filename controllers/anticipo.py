from flask import Blueprint, app, request, jsonify
from models.anticipo import Anticipo
from middlewares.validar_token import validate_token
import json

route_anticipo = Blueprint('ws_anticipo',__name__)

@route_anticipo.route('/anticipo/registrar',methods=['POST'])
@validate_token
def registrarAnticipo():
    if request.method == 'POST':
        estado = 1
        descripcion = request.form['descripcion']
        fechaInicio = request.form['fechaInicio']
        fechaFin = request.form['fechaFin']
        observacionJefatura = 0
        observacionAdministrativa = 0
        idUsuario = request.form['idUsuario']
        idMotivo = request.form['idMotivo']
        idSede = request.form['idSede']
        rubros = request.form['rubros']

        objAnticipo = Anticipo(idestado=estado, descripcion=descripcion,
                                fechaInicio=fechaInicio,fechaFin=fechaFin,
                                observacionJefatura=observacionJefatura,
                                observacionAdministrativa=observacionAdministrativa,
                                idUsuario=idUsuario, idMotivo=idMotivo,
                                idSede=idSede,rubros=rubros
                                )
        rptaJson = json.loads(objAnticipo.registrarAnticipo())
        return jsonify(rptaJson),200