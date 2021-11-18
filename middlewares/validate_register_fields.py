from flask import jsonify, request
from functools import wraps
from email_validator import EmailNotValidError, validate_email


def validate_register_fields(callback):
    @wraps(callback)
    def decorated(*args, **kwargs):
        try:
            if request.form.keys().__len__() == 0:
                return jsonify({'ok': False, 'message': 'No se encontraron datos en la consulta!'}), 400
            exist_email = request.form.keys().__contains__('email')
            exist_password = request.form.keys().__contains__('password')
            exist_personal_id = request.form.keys().__contains__('personal_id')
            exist_tipo_personal_id = request.form.keys().__contains__('tipo_personal_id')
            if not exist_email or not exist_password or not exist_personal_id or not exist_tipo_personal_id:
                return jsonify({'ok': False, 'message': 'Complete los campos para continuar!'}), 400
            validate_email(request.form['email'])
            if request.form['password'].__len__() < 6:
                return jsonify({'ok': False, 'message': 'La contraseña debe ser de mínimo 6 caracteres!'}), 400
        except EmailNotValidError as e:
            return jsonify({'ok': False, 'message': 'Ingrese un email valido!'}), 400
        return callback(*args, **kwargs)
    return decorated
