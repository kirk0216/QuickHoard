import pymysql.cursors
from flask import current_app, g
from flaskext.mysql import MySQL


class Database(object):
    conn = None

    def open(self):
        if self.conn is not None:
            return self.conn

        self.conn = MySQL(current_app)

        self.conn.connect()

    def close(self):
        self.conn.get_db().close()

    def execute(self, sql, args):
        self.conn.get_db().cursor().execute(sql, args)

    def insert(self, sql, args):
        cursor = self.conn.get_db().cursor()
        cursor.execute(sql, args)
        self.conn.get_db().commit()

        return cursor.lastrowid

    def query(self, sql, args):
        cursor = self.conn.get_db().cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, args)
        return cursor

    def commit(self):
        self.conn.get_db().commit()
