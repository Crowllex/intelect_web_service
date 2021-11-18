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
        sql = "insert into usuario(correo, clave, estado_usuario, token, estado_token, img, tipo_personal, id_personal) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, [self.email, self.password,
                           '1', self.token, '1', '', self.tipo_personal_id, self.personal_id])
            con.commit()
            return json.dumps({'ok': True, 'message': 'Successfully register!'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Failed to insert in the database!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()
