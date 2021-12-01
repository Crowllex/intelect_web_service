from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder


class EvaluacionAnticipo:
    def __init__(self, observacion=None,
                 idEstadoEvalAnticipo=None, idUsuario=None,
                 idAnticipo=None):

        self.observacion = observacion
        self.idEstadoEvalAnticipo = idEstadoEvalAnticipo
        self.idUsuario = idUsuario
        self.idAnticipo = idAnticipo

    def registrarEvaluacionAnticipo(self):
        conexion = db().open
        conexion.autocommit = False
        cursor = conexion.cursor()
        sqlEvaluacion = "INSERT INTO evaluacion (observacion,id_estado_eval_anticipo,id_usuario,id_anticipo) VALUES (%s,%s,%s,%s)"
        sql_check_user = "select * from evaluacion where id_usuario = %s and id_anticipo = %s"
        try:
            cursor.execute(sql_check_user, [self.idUsuario, self.idAnticipo])
            result = cursor.fetchone()
            if not result:
                cursor.execute(sqlEvaluacion, [self.observacion,
                                               self.idEstadoEvalAnticipo, self.idUsuario, self.idAnticipo])

                sqlEstadoEval = "SELECT descripcion FROM estado_evaluacion WHERE id_estado_eval_anticipo = %s"
                cursor.execute(sqlEstadoEval, [self.idEstadoEvalAnticipo])
                estado = cursor.fetchone()

                sqlEstadoAnticipo = "SELECT id_estado_anticipo as estado FROM estado_anticipo WHERE descripcion LIKE %s"
                cursor.execute(sqlEstadoAnticipo, [estado['descripcion']])
                idEstadoAnticipo = cursor.fetchone()

                sqlObtenerTipoUsuario = "SELECT u.tipo_personal FROM usuario AS u INNER JOIN tipo_personal AS tp ON u.tipo_personal=tp.id_tipoPersonal WHERE u.id_usuario = %s"
                cursor.execute(sqlObtenerTipoUsuario, [self.idUsuario])
                tipoUsuario = cursor.fetchone()

                sqlObsJef = "SELECT observacion_jefatura FROM anticipo WHERE id_anticipo = %s"
                cursor.execute(sqlObsJef, [self.idAnticipo])
                obsJefatura = cursor.fetchone()

                if tipoUsuario["tipo_personal"] == 1:
                    sqlUpdateAnticipo = "UPDATE anticipo SET id_estado_anticipo =%s, observacion_jefatura=1 WHERE id_anticipo = %s"

                elif tipoUsuario["tipo_personal"] == 3 and obsJefatura["observacion_jefatura"] == 1:
                    sqlUpdateAnticipo = "UPDATE anticipo SET id_estado_anticipo =%s, observacion_administrativa =1 WHERE id_anticipo = %s"

                else:
                    conexion.rollback()
                    return json.dumps({'status': True, 'data': 'Este anticipo debe ser observado primero por la jefatura'})

                cursor.execute(sqlUpdateAnticipo, [
                    idEstadoAnticipo['estado'], self.idAnticipo])
                conexion.commit()
                return json.dumps({'status': True, 'data': 'Evaluacion registrada correctamente!'})
            else:
                return json.dumps({'status': True, 'data': 'Evaluacion de anticipo ya registrada!'})
        except conexion.Error as e:
            conexion.rollback()
            return json.dumps({'status': False, 'data': format(e)}, cls=CustomJsonEncoder)
        finally:
            cursor.close()
            conexion.close()

    def listar(self, id_usuario, id_anticipo):
        con = db().open
        cursor = con.cursor()
        sql_evaluaciones = "SELECT e.id_evaluacion, e.observacion, e.fecha_registro,ee.descripcion AS estado, CONCAT(p.nombres,' ',p.apellidos) AS personal,tp.descripcion as tipo_personal , a.descripcion AS anticipo, m.descripcion AS motivo, s.nombre AS sede FROM evaluacion e INNER JOIN anticipo a ON a.id_anticipo = e.id_anticipo INNER JOIN estado_evaluacion ee ON ee.id_estado_eval_anticipo = e.id_estado_eval_anticipo INNER JOIN usuario u ON u.id_usuario = e.id_usuario INNER JOIN personal p ON p.id_personal = u.id_personal INNER JOIN tipo_personal tp on tp.id_tipoPersonal = p.tipo_personal INNER JOIN motivo m ON m.id_motivo = a.id_motivo INNER JOIN sede s ON s.id_sede = a.id_sede WHERE a.id_usuario = %s AND a.id_anticipo = %s"
        try:
            cursor.execute(sql_evaluaciones, [id_usuario, id_anticipo])
            data = cursor.fetchall()
            if data:
                return json.dumps({'ok': True, 'evaluacion_anticipos': data}, cls=CustomJsonEncoder, default=str)
            else:
                return json.dumps({'ok': False, 'message': 'No se encontraron resultados!'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Ocurrió un error al realizar la consulta!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()
