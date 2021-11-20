from MySQLdb import cursors
from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class Sede():
    def __init__(self, id_sede=None, nombre=None):
        self.id_sede = id_sede
        self.nombre = nombre

    def listarSede(self):
        #Abrir conexión a la base de datos
        con = db().open
        
        #Crear un cursor 
        cursor = con.cursor()

        #Preparar la consulta SQL
        sql = "SELECT S.id_sede, R.Nombre, R.monto, R.calculoxdia, S.nombre AS sede FROM sede S INNER JOIN rubro R ON S.id_sede = R.id_sede"

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

        
