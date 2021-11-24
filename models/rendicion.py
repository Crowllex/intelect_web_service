from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class Rendicion():
    def __init__(self, numero_informe=None, fecha_inicio=None, fecha_fin=None, total=None):
        self.numero_informe = numero_informe
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.total = total

    def listarRendicion(self):
        con = db().open
        
        cursor = con.cursor()

        sql = "SELECT r.numero_informe, a.fecha_inicio, a.fecha_fin, da.total  FROM rendicion_gastos r  INNER JOIN anticipo a ON r.id_anticipo=a.id_anticipo INNER JOIN detalle_anticipo da ON da.id_anticipo=a.id_anticipo"

        cursor.execute(sql)

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos: 
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})

        


