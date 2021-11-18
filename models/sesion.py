from database.connection import Connection as db
import json


class Sesion():
    def __init__(self, email=None, password=None) -> None:
        self.email = email
        self.password = password

    def login(self):
        con = db().open
        cursor = con.cursor()
        sql = "select p.nombres, p.apellidos, u.id_usuario, u.estado_usuario, u.correo from personal p inner join usuario u on (u.id_usuario = p.id_personal) where correo=%s and clave=%s"
        try:
            cursor.execute(sql, [self.email, self.password])
            data = cursor.fetchone()
            if data:
                if data['estado_usuario'] == 1:
                    return json.dumps({'ok': True, 'user': data})
                else:
                    return json.dumps({'ok': False, 'message': 'Usuario inactivo! Contacte con el administrador'})
            else:
                return json.dumps({'ok': False, 'message': 'Credenciales incorrectaas!'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Error al autenticar!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()

    def update_token(self, token, user_id):
        con = db().open
        con.autocommit = False
        cursor = con.cursor()
        sql = "update usuario set token=%s, estado_token='1' where id_usuario=%s"
        try:
            cursor.execute(sql, [token, user_id])
            con.commit()
        except con.Error as error:
            con.rollBack()
            return json.dumps({'status': True, 'message': 'Ocurrió un error al actualizar el token!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()

    def validate_token(self, usuario_id):
        con = db().open
        cursor = con.cursor()
        sql = "select estado_token from usuario where id_usuario=%s"
        try:
            cursor.execute(sql, [usuario_id])
            data = cursor.fetchone()
            if data:
                return json.dumps({'ok': True, 'data': data})
            else:
                return json.dumps({'ok': False, 'message': 'No se encontró datos con el usuario ingresado!'})
        except con.Error as error:
            con.rollBack()
            return json.dumps({'status': True, 'message': 'Ocurrió un error al validar el token!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()
