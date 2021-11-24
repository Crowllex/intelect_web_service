from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder

class EvaluacionAnticipo:
    def __init__(self,observacion=None,fecha=None,hora=None,
                idEstadoEvalAnticipo=None,idUsuario=None,
                idAnticipo=None):

        self.observacion = observacion
        self.fecha = fecha
        self.hora = hora
        self.idEstadoEvalAnticipo = idEstadoEvalAnticipo
        self.idUsuario = idUsuario
        self.idAnticipo = idAnticipo
    
    def registrarEvaluacionAnticipo(self):
        conexion = db().open
        conexion.autocommit = False
        cursor = conexion.cursor()
        sqlEvaluacion = "INSERT INTO evaluacion (observacion,fecha,hora,id_estado_eval_anticipo,id_usuario,id_anticipo) VALUES (%s,%s,%s,%s,%s,%s)"

        try:
            cursor.execute(sqlEvaluacion, [self.observacion, self.fecha, self.hora, self.idEstadoEvalAnticipo,self.idUsuario,self.idAnticipo])

            sqlEstadoEval = "SELECT descripcion FROM estado_evaluacion WHERE id_estado_eval_anticipo = %s"
            cursor.execute(sqlEstadoEval,[self.idEstadoEvalAnticipo])
            estado = cursor.fetchone()

            sqlEstadoAnticipo = "SELECT id_estado_anticipo as estado FROM estado_anticipo WHERE descripcion LIKE %s"
            cursor.execute(sqlEstadoAnticipo,[estado['descripcion']])
            idEstadoAnticipo = cursor.fetchone()

            sqlObtenerTipoUsuario = "SELECT u.tipo_personal FROM usuario AS u INNER JOIN tipo_personal AS tp ON u.tipo_personal=tp.id_tipoPersonal WHERE u.id_usuario = %s"
            cursor.execute(sqlObtenerTipoUsuario,[self.idUsuario])
            tipoUsuario = cursor.fetchone()

            sqlObsJef = "SELECT observacion_jefatura FROM anticipo WHERE id_anticipo = %s"
            cursor.execute(sqlObsJef,[self.idAnticipo])
            obsJefatura = cursor.fetchone()
            
            if tipoUsuario["tipo_personal"] == 1:
                sqlUpdateAnticipo = "UPDATE anticipo SET id_estado_anticipo =%s observacion_jefatura=1 observacion_administrativa =%s WHERE id_anticipo = %s"
            
            if tipoUsuario["tipo_personal"] == 3 and obsJefatura["observacion_jefatura"]== 1:
                sqlUpdateAnticipo = "UPDATE anticipo SET id_estado_anticipo =%s observacion_administrativa =1 WHERE id_anticipo = %s"
            else:
                conexion.rollback()
                return json.dumps({'status': False, 'data':'Este anticipo debe ser observado primero por la jefatura'})

            cursor.execute(sqlUpdateAnticipo,[idEstadoAnticipo['estado'],self.idAnticipo])

            conexion.commit()

            return json.dumps({'status':True,'data':'Se registro la evaluacion de forma correcta'})

        except conexion.Error as e:
            conexion.rollback()
            return json.dumps({'status':False, 'data':format(e)},cls=CustomJsonEncoder)
        finally:
            cursor.close()
            conexion.close()
        