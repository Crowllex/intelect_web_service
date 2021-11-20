from MySQLdb import cursors
from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class Sede():
    def __init__(self, id_sede=None, nombre=None):
        self.id_sede = id_sede
        self.nombre = nombre

    def listarSede(self):
        con = db().open
        
        cursor = con.cursor()

        sql = "SELECT * FROM sede"

        cursor.execute(sql)

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})

        
