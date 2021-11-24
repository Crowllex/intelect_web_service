
from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class Anticipo():
    def __init__(self,descripcion=None, fecha_inicio=None, fecha_fin=None, total=None):
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.total = total
        
    def listarAnticipoPendientePorDocente(self,id_personal):
        con = db().open
        
        cursor = con.cursor()

        sql = "SELECT a.descripcion, a.fecha_inicio, a.fecha_fin, da.total FROM anticipo a INNER JOIN detalle_anticipo da ON da.id_anticipo=a.id_anticipo inner join usuario u ON u.id_usuario=a.id_usuario WHERE (a.id_estado_anticipo= 1 OR a.id_estado_anticipo= 2 OR a.id_estado_anticipo= 3) AND u.id_personal=%s"

        cursor.execute(sql,[id_personal])

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos: 
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})

        
