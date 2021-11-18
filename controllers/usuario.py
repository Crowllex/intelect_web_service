
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from middlewares.validate_register_fields import validate_register_fields
from models.usuario import Usuario
from utils.util import MD5Hash
import json
import jwt
import os


route_usuario = Blueprint('route_usuario', __name__)


@route_usuario.route('/auth/register', methods=['POST'])
@validate_register_fields
def registrar_usuario():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        personal_id = request.form['personal_id']
        tipo_personal_id = request.form['tipo_personal_id']
        hash_password = MD5Hash.md5_password(password)
        token = jwt.encode({'user_email': email, 'user_password': hash_password, 'exp': datetime.utcnow(
        ) + timedelta(seconds=60*120)}, os.getenv('JWT_SECRET_KEY'))
        obj_usuario = Usuario(email, hash_password,
                              personal_id, tipo_personal_id, token)
        rpta_json = obj_usuario.insertar()
        data_usuario = json.loads(rpta_json)
        return jsonify(data_usuario), 200
