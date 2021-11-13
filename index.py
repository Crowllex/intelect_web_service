from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)


@app.route('/welcome')
def home():
    return 'Welcome back homie!'


if __name__ == '__main__':
    app.run(port=4005, debug=True, host='0.0.0.0')
