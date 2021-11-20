#Importar los paquetes y clases que serán necesarios para implementar
from flask import Blueprint, app, request, jsonify
from models.rubro import Rubro
import json
import middlewares.validar_token

route_rubro = Blueprint('route_rubro', __name__)

@route_rubro.route('/rubro/listar', methods=['POST'])
@middlewares.validar_token.validate_token.validar_token #Función que permite validar el token antes de acceder al servicio web 
def listar():
    if request.method == 'POST':
        objProd = Rubro()
        rptaJson = objProd.listarRubro()
        datos_rubro = json.loads(rptaJson) #Convertir una cadena JSON a objetos JSON
        return jsonify(datos_rubro), 200 #200 -> OK
