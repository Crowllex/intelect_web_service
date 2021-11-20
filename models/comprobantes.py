from MySQLdb import cursors
from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class Comprobante():
    def __init__(self, id_comprobante=None, numero_serie=None, numero_correlativo=None, fecha_emision=None, monto_total=None, descripcion=None, id_rendencion_gastos=None, id_rubro=None, id_tipo_comprobante=None):
        self.id_comprobante = id_comprobante
        self.numero_serie = numero_serie
        self.numero_correlativo = numero_correlativo
        self.fecha_emision = fecha_emision
        self.monto_total = monto_total
        self.descripcion = descripcion
        self.id_rendencion_gastos = id_rendencion_gastos
        self.id_rubro = id_rubro
        self.id_tipo_comprobante = id_tipo_comprobante

    def listarComprobante(self):
        #Abrir conexión a la base de datos
        con = db().open
        
        #Crear un cursor 
        cursor = con.cursor()

        #Preparar la consulta SQL
        sql = "SELECT C.id_Comprobante, C.numero_serie, C.fecha_emision, C.monto_Total, TC.descripcion FROM comprobante C INNER JOIN tipo_comprobante TC ON  C.id_tipo_comprobante = TC.id_tipo_comprobante"

        #Ejecutar la consulta SQL
        cursor.execute(sql)

        #Capturar la consulta SQL
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        con.close()

        #Retornar el resultado
        if datos: #Se le pregunta si existe registro
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})

        
