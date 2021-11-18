from flask import jsonify, request
from functools import wraps
from models.sesion import Sesion
import jwt
import os
import json


def validate_token_status(user_id):
    obj_sesion = Sesion()
    rpta_json = obj_sesion.validate_token(user_id)
    data = json.loads(rpta_json)
    if data['ok'] == True:
        token_status = data['data']['estado_token']
        if token_status == None:
            return False
        else:
            if token_status == 0:
                return False
            else:
                return True
    else:
        return False


def validate_token(callback):
    @wraps(callback)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'ok': False, 'message': 'No se encontró token en la petición!'}), 403
        auth_token = token.split(" ")[1]
        try:
            user_info = jwt.decode(auth_token, os.getenv('JWT_SECRET_KEY'),
                                   algorithms='HS256')
            user_id = user_info['user_id']
            token_info = validate_token_status(user_id)
            if token_info == False:
                return jsonify({'ok': False, 'message': 'Token inactivo!'})
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as error:
            return jsonify({'ok': False, 'message': 'Token inválido!', 'Internal token error': format(error)}), 400
        except (Exception) as error:
            return jsonify({'ok': False, 'message': format(error)}), 403
        return callback(*args, **kwargs)
    return decorated
