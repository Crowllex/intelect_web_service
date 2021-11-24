from flask import Blueprint, app, request, jsonify
from models.evaluacionAnticipo import EvaluacionAnticipo
import json
from middlewares.validar_token import validate_token

route_evaluacionAnticipo = Blueprint('ws_evalAnticipo',__name__)

@route_evaluacionAnticipo.route('/anticipo/evaluacion', methods=['POST'])
@validate_token
def eval_anticipo():
    if request.method == 'POST':
        observacion = request.form['observacion']
        fecha = request.form['fecha']
        hora = request.form['hora']
        idEstado = request.form['idEstado']
        idUsuario = request.form['idUsuario']
        idAnticipo = request.form['idAnticipo']

        objEvaluacion = EvaluacionAnticipo(observacion=observacion,fecha=fecha,
                                            hora=hora,idEstadoEvalAnticipo=idEstado,
                                            idUsuario=idUsuario,idAnticipo=idAnticipo)
        rptaJson = json.loads(objEvaluacion.registrarEvaluacionAnticipo())
        return jsonify(rptaJson),200