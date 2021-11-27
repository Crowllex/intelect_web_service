from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder


class Motivo():
    def __init__(self, id_motivo=None, descripcion=None):
        self.id_motivo = id_motivo
        self.descripcion = descripcion

    def listarMotivo(self):
        con = db().open

        cursor = con.cursor()

        sql = "SELECT M.id_motivo, M.descripcion FROM motivo M "

        cursor.execute(sql)

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})
