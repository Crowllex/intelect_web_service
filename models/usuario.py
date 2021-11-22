from database.connection import Connection as db
import json


class Usuario():
    def __init__(self, email=None, password=None, personal_id=None, tipo_personal_id=None, token=None) -> None:
        self.email = email
        self.password = password
        self.token = token
        self.personal_id = personal_id
        self.tipo_personal_id = tipo_personal_id

    def insertar(self):
        con = db().open
        con.autocommit = False
        cursor = con.cursor()
        sql_register = "insert into usuario(correo, clave, estado_usuario, token, estado_token, img, tipo_personal, id_personal) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_check = "select * from usuario where correo=%s"
        try:
            cursor.execute(sql_check, [self.email])
            user_exists = cursor.fetchone()
            if not user_exists:
                cursor.execute(sql_register, [self.email, self.password,
                                              '1', self.token, '1', '', self.tipo_personal_id, self.personal_id])
                con.commit()
                return json.dumps({'ok': True, 'message': 'Registrado correctamente!'})
            else:
                return json.dumps({'ok': False, 'message': 'Usuario ya registrado!'})

        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Ocurrio un error al realizar la operacion!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()
