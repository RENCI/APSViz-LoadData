import os, sys
import base_db
import psycopg2
import json

from common.logging import LoggingUtil
from urllib.parse import urlparse

class APSVIZ_DB(base_db):

    # dbname looks like this: 'asgs_dashboard'
    # instance_id looks like this: '2744-2021050618-namforecast'
    def __init__(self, logger):

        user = os.getenv('APSVIZ_DB_USERNAME', 'user').strip()
        pswd = os.getenv('APSVIZ_DB_PASSWORD', 'password').strip()
        db_name = os.getenv('APSVIZ_DB_DATABASE', 'database').strip()
        host = os.getenv('APSVIZ_DB_HOST', 'host').strip()
        port = os.getenv('APSVIZ_DB_PORT', '5432').strip()

        super().__init__(logger, user, pswd, db_name, host, port)

    def find_cat_group(self, date_str):
        exists = False

        try:
            sql_stmt = 'SELECT name FROM catalog WHERE id=%s'
            params = [f"{date_str}",]
            self.logger.debug(f"APSVIZ_DB: sql statement is: {sql_stmt} params are: {params}")

            self.cursor.execute(sql_stmt, params)
            ret = self.cursor.fetchone()
            if ret:
                self.logger.debug(f"value returned is: {ret}")
                exists = True
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot retrieve catalog id. error {e}")

        self.logger.info(f'APSVIZ_DB: Found catalog group? {exists}')
        return exists

    # retrieve the catalog type id, given the type name - i.e. "group"
    def get_catalog_type_id(self, cat_type):
        self.logger.info(f'APSVIZ_DB: get_catalog_type_id, cat_type:{cat_type}')

        cat_type_id = -1

        try:
            sql_stmt = 'SELECT id FROM catalog_type_lu WHERE name=%s'
            params = [f"{cat_type}",]
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
            json_wb = json.dumps(workbench_list)
            self.cursor.callproc('update_catalog_workbench', [json_wb, ])
        except Exception as e:
            self.logger.error(f'Error detected updating apsviz catalog workbench. {e}')

    # create a catalog for a new day, using the insert_catalog SP
    def create_new_catalog(self, run_date, name, external, cat_type="group"):
        self.logger.info(f'APSVIZ_DB: Creating new catalog, name:{name} external:{external} run_date:{run_date} cat_type:{cat_type}')

        # first, lookup catalog type id
        cat_type_id = self.get_catalog_type_id(cat_type)

        # now get the catalog base_id
        # for now just grab first one
        cat_base_id = self.get_catalog_base_id()

        # now add new catalog entry
        try:
            self.cursor.callproc('insert_catalog', (run_date, name, external, cat_type_id, cat_base_id))
        except Exception as e:
            self.logger.error(f'Error detected creating new catalog. {e}')


    # stored proc looks like this:
    # insert_catalog_member(_catalog_id text, _grid_type text, _event_type text, _instance_name text, _run_date date, _member_def json,
    # _met_class text DEFAULT ''::text, _storm_name text DEFAULT ''::text, _cycle text DEFAULT ''::text, _advisory_number text DEFAULT ''::text,
    # _member_id text DEFAULT NULL::text, _project_code text DEFAULT ''::text, _product_type text DEFAULT ''::text, _group_id integer DEFAULT NULL::integer) returns integer

    def add_cat_item(self, grid_type, event_type, run_date, instance_name, member_json, met_class, storm_name, cycle, advisory, project_code, product_type):
        self.logger.info(f'APSVIZ_DB: Creating new catalog member, grid_type:{grid_type} event_type:{event_type} run_date:{run_date} instance_name:{instance_name} met_class:{met_class} storm_name:{storm_name} cycle:{cycle} advisory:{advisory} , project_code:{project_code}, product_type:{product_type}')

        # convert json to a string for DB
        member_str = json.dumps(member_json)

        # now add new catalog entry
        try:
            self.cursor.callproc('insert_catalog_member', (run_date, grid_type, event_type, instance_name, run_date, member_str, met_class, storm_name, cycle, advisory, project_code, product_type))
        except Exception as e:
            self.logger.error(f'Error detected creating new catalog member. {e}')

    # check to see if a tropical run already exists for a given date
    def get_tropical_run(self, run_date):
        self.logger.info(f'APSVIZ_DB: retrieving tropical run ids for given date, run_date: {run_date}')
        tropical_member_ids = []

        try:
            self.cursor.callproc('get_tropical_member_id', (run_date, ))
            ret = self.cursor.fetchone()
            if ret:
                self.logger.debug(f"value returned is: {ret}")
                tropical_member_ids = ret[0]

        except Exception as e:
            self.logger.error(f'Error retrieving any tropical runs for today. {e}')

        self.logger.debug(f'returning ret={ret}')
        return tropical_member_ids
