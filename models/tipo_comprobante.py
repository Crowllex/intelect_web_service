from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder


class Tipo_Comprobante():
    def __init__(self, descripcion=None):
        self.descripcion = descripcion

    def listar(self):
        con = db().open

        cursor = con.cursor()

        sql = "SELECT * FROM tipo_comprobante"

        cursor.execute(sql)

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})
