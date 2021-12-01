
from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class DetalleAnticipo:
    def __init__(self,id_anticipo = None):
        self.id_anticipo = id_anticipo

    def listarDetalleAnticipo (self):
         con = db().open

        cursor = con.cursor()
        
        sql = "SELECT gastos_totales from detalle_anticipo where id_anticipo = %s"

        cursor.execute(sql,[self.id_anticipo])
        data = cursir.fetchone()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No se encontraron datos'})

