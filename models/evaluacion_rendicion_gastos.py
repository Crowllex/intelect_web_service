from database.connection import Connection as db
import json


class Ev_rendicion_gastos():
    def __init__(self, observacion=None, id_rendicion_gastos=None, id_usuario=None, id_estado_eval_rendicion=None) -> None:

        self.observacion = observacion
        self.id_rendicion_gastos = id_rendicion_gastos
        self.id_usuario = id_usuario
        self.id_estado_eval_rendicion = id_estado_eval_rendicion

    def insertar(self):
        con = db().open
        con.autocommit = False
        cursor = con.cursor()
        sql_register = "INSERT INTO evaluacion_rendicion_gastos (observacion, id_rendicion_gastos, id_usuario, id_estado_eval_rendicion) VALUES (%s,%s,%s,%s)"
        sql_check = "select * from evaluacion_rendicion_gastos where id_usuario=%s and id_rendicion_gastos=%s"
        sql_check_user = "SELECT * FROM usuario  WHERE tipo_personal=2 AND id_usuario=%s"
        sql_tpersonal = "SELECT tipo_personal from usuario WHERE id_usuario=%s"
        sql_update1 = "UPDATE rendicion_gastos SET observacion_jefatura=1 WHERE id_rendicion_gastos=%s"
        sql_update2 = "UPDATE rendicion_gastos SET observacion_administrativa=1 WHERE id_rendicion_gastos=%s"
        sql_update_rendicion = "update rendicion_gastos set id_estado_rendicion=%s where id_rendicion_gastos=%s"
        sql_get_anticipo = "select id_anticipo from rendicion_gastos where id_rendicion_gastos=%s"
        sql_update_anticipo = "update anticipo set id_estado_anticipo=%s where id_anticipo=%s"
        try:
            cursor.execute(
                sql_check, [self.id_usuario, self.id_rendicion_gastos])
            erg_exists = cursor.fetchone()
            if not erg_exists:
                cursor.execute(sql_check_user, [self.id_usuario])
                erg_exists_user = cursor.fetchone()
                if not erg_exists_user:
                    cursor.execute(sql_register, [
                                   self.observacion, self.id_rendicion_gastos, self.id_usuario, self.id_estado_eval_rendicion])
                    cursor.execute(sql_tpersonal, [self.id_usuario])
                    tpersonal = cursor.fetchone()
                    if tpersonal['tipo_personal'] == 1:
                        cursor.execute(
                            sql_update1, [self.id_rendicion_gastos])

                        if self.id_estado_eval_rendicion == '2':
                            print('llego aqui')
                            cursor.execute(sql_update_rendicion, [3,
                                                                  self.id_rendicion_gastos])
                            cursor.execute(sql_get_anticipo, [
                                self.id_rendicion_gastos])
                            anticipo = cursor.fetchone()
                            cursor.execute(sql_update_anticipo, [6,
                                                                 anticipo['id_anticipo']])
                    else:
                        cursor.execute(sql_update2, [self.id_rendicion_gastos])
                        if self.id_estado_eval_rendicion == '2':
                            cursor.execute(sql_update_rendicion, [3,
                                                                  self.id_rendicion_gastos])
                            cursor.execute(sql_get_anticipo, [
                                self.id_rendicion_gastos])
                            anticipo = cursor.fetchone()
                            cursor.execute(sql_update_anticipo, [6,
                                                                 anticipo['id_anticipo']])
                        else:
                            cursor.execute(sql_update_rendicion, [1,
                                                                  self.id_rendicion_gastos])
                            cursor.execute(sql_get_anticipo, [
                                self.id_rendicion_gastos])
                            anticipo = cursor.fetchone()
                            cursor.execute(sql_update_anticipo, [7,
                                                                 anticipo['id_anticipo']])

                    con.commit()
                    return json.dumps({'ok': True, 'message': 'Registrado correctamente!'})
                else:
                    return json.dumps({'ok': False, 'message': 'Tipo de personal no autorizado para registrar la evaluaci??n de rendici??n de gastos'})
            else:
                return json.dumps({'ok': False, 'message': 'El usuario ya registr?? su evaluaci??n de rendicion de gastos'})

        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Ocurrio un error al realizar la operacion!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()
