from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder


class Rubro():
    def __init__(self, id_rubro=None, nombre=None, monto=None, calculoxdia=None, id_sede=None):
        self.id_sede = id_rubro
        self.nombre = nombre
        self.monto = monto
        self.calculoxdia = calculoxdia
        self.id_sede = id_sede

    def listarRubro(self):
        con = db().open

        cursor = con.cursor()

        sql = "SELECT R.id_rubro, R.nombre AS descripcion, R.monto, R.calculoxdia, S.nombre AS sede FROM rubro R INNER JOIN sede S ON R.id_sede = S.id_sede"

        cursor.execute(sql)

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})
