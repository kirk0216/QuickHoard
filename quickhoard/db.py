import pymysql.cursors
from flask import current_app, g
from flaskext.mysql import MySQL


# Class for managing a database connection and performing queries.
class Database(object):
    conn = None

    # Opens the connection to the database
    def open(self):
        # If a connection is already open, reuse it
        if self.conn is not None:
            return self.conn

        self.conn = MySQL(current_app)

        self.conn.connect()

    # Closes the connection to the database
    def close(self):
        self.conn.get_db().close()

    # Executes a SQL statement that does not return any information.
    # - sql: The parameterized SQL statement to execute.
    # - args: A dictionary object that contains parameter values.
    def execute(self, sql, args=None):
        self.conn.get_db().cursor().execute(sql, args)

    # Executes an insert SQL statement and returns the ID for the inserted object.
    # - sql: The parameterized SQL statement to execute.
    # - args: A dictionary object that contains parameter values.
    # Returns: The ID of the newly inserted object.
    def insert(self, sql, args):
        cursor = self.conn.get_db().cursor()
        cursor.execute(sql, args)
        self.conn.get_db().commit()

        return cursor.lastrowid

    # Executes a SQL statement and returns a cursor for parsing the results.
    # - sql: The parameterized SQL statement to execute.
    # - args: A dictionary object that contains parameter values.
    # Returns: A cursor object containing the SQL query results.
    def query(self, sql, args=None):
        cursor = self.conn.get_db().cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, args)
        return cursor

    # Commits the outstanding transaction.
    def commit(self):
        self.conn.get_db().commit()
