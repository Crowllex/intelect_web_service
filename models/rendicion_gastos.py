from database.connection import Connection as db
import json

from utils.util import CustomJsonEncoder


class Rendicion_gastos():
    def __init__(self, id_estado_rendicion=None, id_anticipo=None, comprobantes=None) -> None:

        self.id_estado_rendicion = id_estado_rendicion
        self.id_anticipo = id_anticipo
        self.observacion_jefatura = 0
        self.observacion_administrativa = 0
        self.comprobantes = comprobantes

    def insertar(self):
        con = db().open
        con.autocommit = False
        cursor = con.cursor()
        sql_variable = "SELECT CONCAT(YEAR(NOW()),'-',id_usuario,'-',id_anticipo) AS numero_informe FROM anticipo WHERE id_anticipo=%s;"
        sql_register = "INSERT INTO rendicion_gastos (numero_informe, id_estado_rendicion, id_anticipo, observacion_jefatura, observacion_administrativa) VALUES (%s,%s,%s,%s,%s)"
        sql_check = "select * from rendicion_gastos where numero_informe=%s"
        sql_detalle = "insert into detalle_rendicion(id_rendicion_gastos,id_comprobante) values (%s,%s)"
        try:
            cursor.execute(sql_variable, [self.id_anticipo])
            numero_informe = cursor.fetchone()
            cursor.execute(sql_check, [numero_informe['numero_informe']])
            ni_exists = cursor.fetchone()
            sql_series = "select numero_serie from comprobante"
            cursor.execute(sql_series)
            values = cursor.fetchall()
            if values:
                last_serie = values.pop()
            else:
                last_serie = {'numero_serie': 0}
            jsonArrayComprobantes = json.loads(self.comprobantes)
            cursor.execute(sql_register, [numero_informe['numero_informe'], self.id_estado_rendicion,
                                          self.id_anticipo, self.observacion_jefatura, self.observacion_administrativa])
            rendicion_id = con.insert_id()

            if not ni_exists:
                for comprobante in jsonArrayComprobantes:
                    sql_comprobante = "insert into comprobante (numero_serie,numero_correlativo,fecha_emision,monto_total,descripcion,id_rubro,id_tipo_comprobante,ruc) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql_comprobante, [last_serie['numero_serie'], comprobante['numero_correlativo'], comprobante['fecha_emision'],
                                   comprobante['monto_total'], comprobante['descripcion'], comprobante['id_rubro'], comprobante['id_tipo_comprobante'], comprobante['ruc']])
                    comprobante_id = con.insert_id()

                    cursor.execute(sql_detalle, [rendicion_id, comprobante_id])

                con.commit()
                return json.dumps({'ok': True, 'message': 'Registrado correctamente!'})
            else:
                return json.dumps({'ok': False, 'message': 'Rendición de gastos ya registrada!'})

        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Ocurrio un error al realizar la operacion!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()

    def listarRendicion(self):
        con = db().open

        cursor = con.cursor()

        sql = "SELECT r.numero_informe, a.fecha_inicio, a.fecha_fin, da.gastos_totales  FROM rendicion_gastos r  INNER JOIN anticipo a ON r.id_anticipo=a.id_anticipo INNER JOIN detalle_anticipo da ON da.id_anticipo=a.id_anticipo"

        cursor.execute(sql)

        datos = cursor.fetchall()

        cursor.close()
        con.close()

        if datos:
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})
