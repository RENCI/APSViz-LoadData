import os, sys
import psycopg2

class BASE_DB:

    def __init__(self, logger, user, pswd, db, host, port):
        self.conn = None
        self.logger = logger

        self.user = user
        self.pswd = pswd
        self.dbname = db
        self.host = host
        self.port = port

        try:
            # connect to the database
            conn_str = f'host={self.host} port={self.port} dbname={self.dbname} user={self.user} password={self.pswd}'

            self.conn = psycopg2.connect(conn_str)
            self.conn.set_session(autocommit=True)
            self.cursor = self.conn.cursor()
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot connect to {self.dbname} DB. error {e}")

    def __del__(self):
        """
            close up the DB
            :return:
        """
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            self.logger.error(f'Error detected closing cursor or connection. {e}')
            #sys.exc_info()[0]

    def get_user(self):
        return self.user

    def get_password(self):
        return self.pswd

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_dbname(self):
        return self.dbname

    def get_conn(self):
        return self.conn

    def get_cursor(self):
        return self.cursor