from database.connection import Connection as db
import json
from utils.util import CustomJsonEncoder


class EvaluacionAnticipo:
    def __init__(self, observacion=None, fecha=None, hora=None,
                 idEstadoEvalAnticipo=None, idUsuario=None,
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
            cursor.execute(sqlEvaluacion, [self.observacion, self.fecha, self.hora,
                           self.idEstadoEvalAnticipo, self.idUsuario, self.idAnticipo])

            sqlEstadoEval = "SELECT descripcion FROM estado_evaluacion WHERE id_estado_eval_anticipo = %s"
            cursor.execute(sqlEstadoEval, [self.idEstadoEvalAnticipo])
            estado = cursor.fetchone()

            sqlEstadoAnticipo = "SELECT id_estado_anticipo as estado FROM estado_anticipo WHERE descripcion LIKE %s"
            cursor.execute(sqlEstadoAnticipo, [estado['descripcion']])
            idEstadoAnticipo = cursor.fetchone()

            sqlUpdateAnticipo = "UPDATE anticipo SET id_estado_anticipo =%s WHERE id_anticipo = %s"
            cursor.execute(sqlUpdateAnticipo, [
                           idEstadoAnticipo['estado'], self.idAnticipo])

            conexion.commit()

            return json.dumps({'status': True, 'data': 'Se registro la evaluacion de forma correcta'})

        except conexion.Error as e:
            conexion.rollback()
            return json.dumps({'status': False, 'data': format(e)}, cls=CustomJsonEncoder)
        finally:
            cursor.close()
            conexion.close()

    def listar(self, id_usuario):
        con = db().open
        cursor = con.cursor()
        sql_evaluaciones = "SELECT e.id_evaluacion, e.observacion, e.fecha, e.hora,ee.descripcion AS estado, CONCAT(p.nombres,' ',p.apellidos) AS personal , a.descripcion AS anticipo, m.descripcion AS motio, s.nombre AS sede FROM evaluacion e INNER JOIN anticipo a ON a.id_anticipo = e.id_anticipo INNER JOIN estado_evaluacion ee ON ee.id_estado_eval_anticipo = e.id_estado_eval_anticipo INNER JOIN usuario u ON u.id_usuario = e.id_usuario INNER JOIN personal p ON p.id_personal = u.id_personal INNER JOIN motivo m ON m.id_motivo = a.id_motivo INNER JOIN sede s ON s.id_sede = a.id_sede WHERE a.id_usuario = %s"
        try:
            cursor.execute(sql_evaluaciones, [id_usuario])
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
