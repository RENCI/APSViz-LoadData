import os, sys
import logging
import psycopg2

from common.logging import LoggingUtil
from urllib.parse import urlparse

class APSVIZ_DB:

    db_name = "apsviz"

    # dbname looks like this: 'asgs_dashboard'
    # instance_id looks like this: '2744-2021050618-namforecast'
    def __init__(self, logger):
        self.conn = None
        self.logger = logger

        self.user = os.getenv('ASGS_DB_USERNAME', 'user').strip()
        self.pswd = os.getenv('ASGS_DB_PASSWORD', 'password').strip()
        self.host = os.getenv('ASGS_DB_HOST', 'host').strip()
        self.port = os.getenv('ASGS_DB_PORT', '5432').strip()

        try:
            # connect to asgs database
            conn_str = f'host={self.host} port={self.port} dbname={self.db_name} user={self.user} password={self.pswd}'

            self.conn = psycopg2.connect(conn_str)
            self.conn.set_session(autocommit=True)
            self.cursor = self.conn.cursor()
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot connect to APSVIZ DB. error {e}")

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
        return self.db_name

    def find_cat_group(self, date_str):
        exists = False

        try:
            sql_stmt = 'SELECT name FROM catalog WHERE id=%s'
            params = [f"{date_str}"]
            self.logger.debug(f"APSVIZ_DB: sql statement is: {sql_stmt} params are: {params}")

            self.cursor.execute(sql_stmt, params)
            ret = self.cursor.fetchone()
            if ret:
                self.logger.debug(f"value returned is: {ret}")
                exists = True
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot retrieve catalog id. error {e}")

        self.logger.info(f'APSVIZ_DB: catalog type id is: {cat_type_id}')
        return exists

    # retrieve the catalog type id, given the type name - i.e. "group"
    def get_catalog_type_id(self, type):

        cat_type_id = -1

        try:
            sql_stmt = 'SELECT id FROM catalog_type_lu WHERE name=%s'
            params = [f"{type}"]
            self.logger.debug(f"APSVIZ_DB: sql statement is: {sql_stmt} params are: {params}")

            self.cursor.execute(sql_stmt, params)
            ret = self.cursor.fetchone()
            if ret:
                self.logger.debug(f"value returned is: {ret}")
                cat_type_id = ret[0]
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot retrieve catalog type id. error {e}")

        self.logger.info(f'APSVIZ_DB: catalog type id is: {cat_type_id}')
        return cat_type_id

    # retrieve the catalog base id
    # don't know what to search for, so for
    # now just returning the first one
    def get_catalog_base_id(self):

        cat_base_id = -1

        try:
            sql_stmt = 'SELECT id FROM catalog_base'
            self.logger.debug(f"APSVIZ_DB: sql statement is: {sql_stmt}")

            self.cursor.execute(sql_stmt)
            ret = self.cursor.fetchone()
            if ret:
                self.logger.debug(f"value returned is: {ret}")
                cat_base_id = ret[0]
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot retrieve catalog base id. error {e}")

        self.logger.info(f'APSVIZ_DB: catalog base id is: {cat_base_id}')
        return cat_base_id

    # update catalog workbench entry using the update_catalog_workbench SP
    def update_workbench(self, workbench_list):
        self.logger.info(f'APSVIZ_DB: Updating workbench list: {workbench_list}')

        try:
            self.cursor.callproc('update_catalog_workbench', [workbench_list, ])
        except Exception as e:
            self.logger.error(f'Error detected updating apsviz catalog workbench. {e}')

    # create a catalog for a new day, using the insert_catalog SP
    def create_new_catalog(self, id, name, external, run_date, type="group"):
        self.logger.info(f'APSVIZ_DB: Creating new catalog, id:{id} name:{name} external:{external} run_date:{run_date} type:{type}')

        # first, lookup catalog type id
        cat_type_id = self.get_catalog_type_id(type)

        # now get the catalog base_id
        # for now just grab first one
        cat_base_id = self.get_catalog_base_id()

        # now add new catalog entry
        try:
            self.cursor.callproc('insert_catalog', (run_date, name, external, cat_type_id, cat_base_id))
        except Exception as e:
            self.logger.error(f'Error detected creating new catalog. {e}')

    #
    def add_cat_item(self, grid_type, event_type, run_date, instance_name, member_json):
        self.logger.info(f'APSVIZ_DB: Creating new catalog member, grid_type:{grid_type} event_type:{event_type} run_date:{run_date} instance_name:{instance_name}')

        # first, lookup catalog type id
        cat_type_id = self.get_catalog_type_id(type)

        # now get the catalog base_id
        # for now just grab first one
        cat_base_id = self.get_catalog_base_id()

        # now add new catalog entry
        try:
            self.cursor.callproc('insert_catalog', (cat_base_id, grid_type, event_type, run_date, instance_name, member_json))
        except Exception as e:
            self.logger.error(f'Error detected creating new catalog. {e}')