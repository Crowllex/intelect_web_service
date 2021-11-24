from database.connection import Connection as db
import json
class Ev_rendicion_gastos():
    def __init__(self, observacion=None,id_rendicion_gastos=None, id_usuario=None, id_estado_eval_rendicion=None) -> None:
        
        self.observacion = observacion
        self.id_rendicion_gastos = id_rendicion_gastos
        self.id_usuario= id_usuario
        self.id_estado_eval_rendicion = id_estado_eval_rendicion
        

    def insertar(self):
        con = db().open
        con.autocommit = False
        cursor = con.cursor()
        sql_register = "INSERT INTO evaluacion_rendicion_gastos (observacion, id_rendicion_gastos, id_usuario, id_estado_eval_rendicion) VALUES (%s,%s,%s,%s)"
        sql_check = "select * from evaluacion_rendicion_gastos where id_usuario=%s and id_rendicion_gastos=%s"
        try:
            cursor.execute(sql_check, [self.id_usuario,self.id_rendicion_gastos])
            erg_exists = cursor.fetchone()
            if not erg_exists:
                cursor.execute(sql_register, [self.observacion,self.id_rendicion_gastos,self.id_usuario,self.id_estado_eval_rendicion])
                con.commit()
                return json.dumps({'ok': True, 'message': 'Registrado correctamente!'})
            else:
                return json.dumps({'ok': False, 'message': 'El usuario ya registró su evaluación de rendicion de gastos'})

        except con.Error as error:
            con.rollback()
            return json.dumps({'ok': False, 'message': 'Ocurrio un error al realizar la operacion!', 'Internal error': format(error)})
        finally:
            cursor.close()
            con.close()