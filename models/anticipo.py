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
            #ejecutamos el insert en la tabla anticipo
            cursor.execute(sqlAnticipo,[self.idestado,self.descripcion,self.fechaInicio,
                                self.fechaFin,self.observacionJefatura,
                                self.observacionAdministrativa,self.idUsuario,
                                self.idMotivo,self.idSede])
            #guardo el id del anticipo para el detalle
            idAnticipo = conexion.insert_id()

            #los rubros seleccionados y su calculo por dia se obtendran de la app al momento de registrar
            #y vendran como un json ejemplo [{"id_rubro":9,"cantidad_total":10},{"id_rubro":10,"cantidad_total":20}]
            jsonArrayRubros = json.loads(self.rubros)

            #se inserta en el detalle de anticipo
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
