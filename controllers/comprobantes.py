#Importar los paquetes y clases que serán necesarios para implementar
from flask import Blueprint, app, request, jsonify
from models.comprobantes import Comprobante
import json
import middlewares.validar_token

route_comprobante = Blueprint('route_comprobante', __name__)

@route_comprobante.route('/comprobante/listar', methods=['POST'])
@middlewares.validar_token.validate_token.validar_token #Función que permite validar el token antes de acceder al servicio web 
def listar():
    if request.method == 'POST':
        objProd = Comprobante()
        rptaJson = objProd.listarComprobante()
        datos_comprobante = json.loads(rptaJson) #Convertir una cadena JSON a objetos JSON
        return jsonify(datos_comprobante = json.loads(rptaJson) #Convertir una cadena JSON a objetos JSON
), 200 #200 -> OK
