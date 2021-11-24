
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

    def listarComprobante(self, id_usuario):
        con = db().open

        cursor = con.cursor()

        sql = "SELECT R.nombre AS Rubro, C.fecha_emision AS FechaEmision, C.numero_serie AS comprobante, TP.descripcion AS TipoComprobante, C.monto_total AS Monto FROM comprobante C INNER JOIN detalle_rendicion DR  ON DR.id_comprobante = C.id_comprobante INNER JOIN rendicion_gastos RG ON RG.id_rendicion_gastos = DR.id_rendicion_gastos INNER JOIN rubro R ON R.id_rubro = C.id_rubro INNER JOIN tipo_comprobante TP ON TP.id_tipo_comprobante = C.id_tipo_comprobante INNER JOIN anticipo A ON A.id_anticipo = RG.id_anticipo WHERE A.id_usuario = %s"

        cursor.execute(sql, [id_usuario])

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})
