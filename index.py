from flask import Flask
from controllers.usuario import route_usuario
from controllers.sesion import route_sesion
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.register_blueprint(route_usuario)
app.register_blueprint(route_sesion)


@app.route('/welcome')
def home():
    return 'Welcome back homie!'


if __name__ == '__main__':
    app.run(port=4005, debug=True, host='0.0.0.0')
