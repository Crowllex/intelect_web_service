from database.connection import Connection as db
import json
class Rendicion_gastos():
    def __init__(self, id_estado_rendicion=None,id_anticipo=None, observacion_jefatura=None, observacion_administrativa=None) -> None:
        
        self.id_estado_rendicion = id_estado_rendicion
        self.id_anticipo = id_anticipo
        self.observacion_jefatura= 0
        self.observacion_administrativa = 0
        

    def insertar(self):
        con = db().open
        con.autocommit = False
        cursor = con.cursor()
        sql_variable="SELECT CONCAT(YEAR(NOW()),'-',id_usuario,'-',id_anticipo) AS numero_informe FROM anticipo WHERE id_anticipo=%s;"
        sql_register = "INSERT INTO rendicion_gastos (numero_informe, id_estado_rendicion, id_anticipo, observacion_jefatura, observacion_administrativa) VALUES (%s,%s,%s,%s,%s)"
        sql_check = "select * from rendicion_gastos where numero_informe=%s"
        try:
            cursor.execute(sql_variable, [self.id_anticipo])
            numero_informe = cursor.fetchone()
            cursor.execute(sql_check, [numero_informe['numero_informe']])
            ni_exists = cursor.fetchone()
            if not ni_exists:
                cursor.execute(sql_register, [numero_informe['numero_informe'],self.id_estado_rendicion,self.id_anticipo,self.observacion_jefatura,self.observacion_administrativa])
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