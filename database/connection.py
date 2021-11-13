import pymysql as dbc
import pymysql.cursors as cursors
import os


class Connection():
    def __init__(self) -> None:
        self.db_link = dbc.connect(host=os.environ.DB_HOST, user=os.environ.DB_USER, passwd=os.environ.DB_PASSWORD,
                                   db=os.environ.DB_NAME, port=os.environ.DB_PORT, cursorclass=cursors.DictCursor)

    @property
    def open(self):
        return self.db_link
