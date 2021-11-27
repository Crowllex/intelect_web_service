# import MySQLdb as dbc
# import MySQLdb.cursors as cursors
import pymysql as dbc
import pymysql.cursors as cursors
import os


class Connection():
    def __init__(self) -> None:
        self.db_link = dbc.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), passwd=os.getenv('DB_PASSWORD'),
                                   db=os.getenv('DB_NAME'), port=int(os.getenv('DB_PORT')), cursorclass=cursors.DictCursor)

    @property
    def open(self):
        return self.db_link
