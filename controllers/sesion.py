from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from middlewares.validate_login_fields import validate_login_fields
from models.sesion import Sesion
from utils.util import MD5Hash
import json
import jwt
import os

route_sesion = Blueprint('route_sesion', __name__)


@route_sesion.route('/auth/login', methods=['POST'])
@validate_login_fields
def auth_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hash_password = MD5Hash.md5_password(password)
        obj_session = Sesion(email, hash_password)
        rpta_json = obj_session.login()
        sesion_data = json.loads(rpta_json)
        if sesion_data['ok'] == True:
            user_id = sesion_data['user']['id_usuario']
            token = jwt.encode({'user_email': sesion_data['user']['correo'], 'user_id': sesion_data['user']['id_usuario'], 'user_name': sesion_data['user']['nombres'], 'exp': datetime.utcnow(
            ) + timedelta(seconds=60*120)}, os.getenv('JWT_SECRET_KEY'))
            obj_session.update_token(token, user_id)
            sesion_data['user']['token'] = token
            return jsonify(sesion_data), 200
        else:
            return jsonify(sesion_data), 400
