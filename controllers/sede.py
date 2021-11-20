#Importar los paquetes y clases que serán necesarios para implementar
from flask import Blueprint, app, request, jsonify
from models.sede import Sede
import json
import middlewares.validar_token

route_sede = Blueprint('route_sede', __name__)

@route_sede.route('/sede/listar', methods=['POST'])
@middlewares.validar_token.validate_token.validar_token #Función que permite validar el token antes de acceder al servicio web 
def listar():
    if request.method == 'POST':
        objProd = Sede()
        rptaJson = objProd.listarSede()
        datos_sede = json.loads(rptaJson) #Convertir una cadena JSON a objetos JSON
        return jsonify(datos_sede = json.loads(rptaJson) #Convertir una cadena JSON a objetos JSON
), 200 #200 -> OK
