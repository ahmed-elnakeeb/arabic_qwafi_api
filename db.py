import sqlite3
from sqlite3 import Error


class db:
    def __init__(self, db_file):
        """initialize connection with db file or create new"""
        self.db_file = db_file

    def start_connection(self):
        """ create a database connection to a SQLite database """
        self.connection = None

        try:
            self.connection = sqlite3.connect(self.db_file)
            
        except Error:
            print(Error)
    
    def start_connection2(self):
        """ create a database connection to a SQLite database """
        self.connection = None

        try:
            self.connection = sqlite3.connect(self.db_file,check_same_thread=False)
            
        except Error:
            print(Error)


    def stop_connection(self) :
        """ stop a database connection to a SQLite database """
        self.connection = None


    def qurey(self, qry):
        """executes given query """
        try:
            self.connection.execute(qry)
            self.connection.commit()
        except Error as e:
            print(e)

    def rows(self, qry) -> list:
        """ return the selected rows"""
        try:
            cur = self.connection.cursor()
            cur.execute(qry)
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)
            