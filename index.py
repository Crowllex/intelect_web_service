from flask import Flask
from controllers.usuario import route_usuario
from controllers.sesion import route_sesion
from controllers.sede import route_sede
from controllers.rubro import route_rubro
from controllers.comprobantes import route_comprobante
from controllers.motivo import route_motivo
from controllers.rendicion import route_rendicion
from controllers.anticipo import route_anticipo
from controllers.evaluacionAnticipo import route_evaluacionAnticipo
from controllers.rendicion_gastos import route_rg
from controllers.evaluacion_rendicion_gastos import route_erg
import pymysql
pymysql.install_as_MySQLdb()



app = Flask(__name__)
app.register_blueprint(route_usuario)
app.register_blueprint(route_sesion)
app.register_blueprint(route_sede)
app.register_blueprint(route_rubro)
app.register_blueprint(route_comprobante)
app.register_blueprint(route_motivo)
app.register_blueprint(route_rendicion)
app.register_blueprint(route_anticipo)
app.register_blueprint(route_evaluacionAnticipo)
app.register_blueprint(route_rg)
app.register_blueprint(route_erg)


@app.route('/welcome')
def home():
    return 'Welcome back homie!'


if __name__ == '__main__':
    app.run(port=3000, debug=True, host='0.0.0.0')
