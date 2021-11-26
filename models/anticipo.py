from database.connection import Connection as db
from utils.util import CustomJsonEncoder
import json


class Anticipo:
    def __init__(self, idestado=None, descripcion=None, fechaInicio=None, fechaFin=None,
                 observacionJefatura=None, observacionAdministrativa=None, idUsuario=None,
                 idMotivo=None, idSede=None, rubros=None):

        self.idestado = idestado
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.observacionJefatura = observacionJefatura
        self.observacionAdministrativa = observacionAdministrativa
        self.idUsuario = idUsuario
        self.idMotivo = idMotivo
        self.idSede = idSede
        self.rubros = rubros

    def registrarAnticipo(self):
        conexion = db().open
        conexion.autocommit = False
        cursor = conexion.cursor()
        sqlAnticipo = "INSERT INTO anticipo (id_estado_anticipo,descripcion,fecha_inicio,fecha_fin,observacion_jefatura,observacion_administrativa,id_usuario,id_motivo,id_sede)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            cursor.execute(sqlAnticipo, [self.idestado, self.descripcion, self.fechaInicio,
                                         self.fechaFin, self.observacionJefatura,
                                         self.observacionAdministrativa, self.idUsuario,
                                         self.idMotivo, self.idSede])

            idAnticipo = conexion.insert_id()
            jsonArrayRubros = json.loads(self.rubros)

            for rubro in jsonArrayRubros:
                sqlDetalleAnticipo = "INSERT INTO detalle_anticipo (id_rubro,id_anticipo,gastos_totales) VALUES (%s,%s,%s)"
                idRubro = rubro["id_rubro"]
                cantidad_total = rubro["cantidad_total"]
                cursor.execute(sqlDetalleAnticipo, [
                               idRubro, idAnticipo, cantidad_total])

            conexion.commit()
            return json.dumps({'status': True, 'data': 'Anticipo registrado correctamente'})

        except conexion.Error as e:
            conexion.rollback()
            return json.dumps({'status': False, 'data': format(e)}, cls=CustomJsonEncoder)
        finally:
            cursor.close()
            conexion.close()

    def listarAnticipoPendientePorDocente(self, id_personal):
        con = db().open

        cursor = con.cursor()

        sql = "SELECT a.descripcion, a.fecha_inicio, a.fecha_fin, da.gastos_totales FROM anticipo a INNER JOIN detalle_anticipo da ON da.id_anticipo=a.id_anticipo inner join usuario u ON u.id_usuario=a.id_usuario WHERE (a.id_estado_anticipo= 1 OR a.id_estado_anticipo= 2 OR a.id_estado_anticipo= 3) AND u.id_personal=%s"

        cursor.execute(sql, [id_personal])

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})

    def listar(self, id_usuario):
        con = db().open
        cursor = con.cursor()
        sql_docente = "SELECT a.id_anticipo, a.descripcion, a.fecha_inicio, a.fecha_fin, CONCAT(p.nombres, ' ', p.apellidos) AS docente, m.descripcion AS motivo, s.nombre AS sede, ea.descripcion AS estado FROM anticipo a INNER JOIN motivo m ON m.id_motivo = a.id_motivo INNER JOIN usuario u ON u.id_usuario = a.id_usuario INNER JOIN personal p ON p.id_personal = u.id_personal INNER JOIN sede s ON s.id_sede = a.id_sede INNER JOIN estado_anticipo ea ON ea.id_estado_anticipo = a.id_estado_anticipo WHERE a.id_usuario = %s"
        sql_personal = "select tipo_personal from usuario where id_usuario=%s"
        sql_all = "SELECT a.id_anticipo, a.descripcion, a.fecha_inicio, a.fecha_fin, CONCAT(p.nombres, ' ', p.apellidos) AS docente, m.descripcion AS motivo, s.nombre AS sede, ea.descripcion AS estado FROM anticipo a INNER JOIN motivo m ON m.id_motivo = a.id_motivo INNER JOIN usuario u ON u.id_usuario = a.id_usuario INNER JOIN personal p ON p.id_personal = u.id_personal INNER JOIN sede s ON s.id_sede = a.id_sede INNER JOIN estado_anticipo ea ON ea.id_estado_anticipo = a.id_estado_anticipo WHERE a.id_estado_anticipo = %s"
        sql_detalle = "select sum(gastos_totales) as total from detalle_anticipo where id_anticipo=%s"
        try:
            cursor.execute(sql_personal, [id_usuario])
            data_personal = cursor.fetchone()
            if not data_personal:
                return json.dumps({'ok': False, 'message': 'Usuario incorrecto!'})

            if data_personal['tipo_personal'] == 2:
                cursor.execute(sql_docente, [id_usuario])
                data = cursor.fetchall()
            else:
                cursor.execute(sql_all, [self.idestado])
                data = cursor.fetchall()

            for detalle_data in data:
                cursor.execute(sql_detalle, [detalle_data['id_anticipo']])
                detalle_info = cursor.fetchall()
                for totals in detalle_info:
                    detalle_data['total'] = totals['total']

            if data:
                return json.dumps({'ok': True, 'anticipos': data}, cls=CustomJsonEncoder)
            else:
                return json.dumps({'ok': False, 'message': 'No se encontraron resultados!'})
        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Ocurrió un error al realizar la consulta!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()
