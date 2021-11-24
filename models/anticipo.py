from database.connection import Connection as db
from utils.util import CustomJsonEncoder
import json

class Anticipo :
    def __init__(self,idestado=None,descripcion=None,fechaInicio=None,fechaFin=None,
    observacionJefatura=None,observacionAdministrativa=None,idUsuario=None,
    idMotivo=None,idSede=None,rubros=None):

        self.idestado = idestado
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.observacionJefatura =observacionJefatura
        self.observacionAdministrativa = observacionAdministrativa
        self.idUsuario = idUsuario
        self.idMotivo = idMotivo
        self.idSede = idSede
        self.rubros =rubros

    def registrarAnticipo(self):
        conexion = db().open
        conexion.autocommit = False
        cursor = conexion.cursor()
        sqlAnticipo = "INSERT INTO anticipo (id_estado_anticipo,descripcion,fecha_inicio,fecha_fin,observacion_jefatura,observacion_administrativa,id_usuario,id_motivo,id_sede)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            cursor.execute(sqlAnticipo,[self.idestado,self.descripcion,self.fechaInicio,
                                self.fechaFin,self.observacionJefatura,
                                self.observacionAdministrativa,self.idUsuario,
                                self.idMotivo,self.idSede])

            idAnticipo = conexion.insert_id()
            jsonArrayRubros = json.loads(self.rubros)

            for rubro in jsonArrayRubros:
                sqlDetalleAnticipo ="INSERT INTO detalle_anticipo (id_rubro,id_anticipo,gastos_totales) VALUES (%s,%s,%s)"
                idRubro = rubro["id_rubro"]
                cantidad_total = rubro["cantidad_total"]
                cursor.execute(sqlDetalleAnticipo,[idRubro,idAnticipo,cantidad_total])
        
            conexion.commit()
            return json.dumps({'status':True,'data':'Anticipo registrado correctamente'})

        except conexion.Error as e:
            conexion.rollback()
            return json.dumps({'status':False, 'data':format(e)},cls=CustomJsonEncoder)
        finally:
            cursor.close()
            conexion.close()
            
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
