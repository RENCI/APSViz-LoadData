import os, sys
import logging
import psycopg2
import csv

from common.logging import LoggingUtil
from urllib.parse import urlparse

class ASGS_DB:

    # dbname looks like this: 'asgs_dashboard'
    # instance_id looks like this: '2744-2021050618-namforecast'
    def __init__(self, logger, dbname, instance_id):
        self.conn = None
        self.logger = logger

        self.user = os.getenv('ASGS_DB_USERNAME', 'user').strip()
        self.pswd = os.getenv('ASGS_DB_PASSWORD', 'password').strip()
        self.host = os.getenv('ASGS_DB_HOST', 'host').strip()
        self.port = os.getenv('ASGS_DB_PORT', '5432').strip()
        # self.db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
        self.db_name = dbname

        # save whole Id
        self.instanceId = instance_id
        self.uid = instance_id
        self.instance = instance_id

        # also save separate parts i.e. '2744' and '2021050618-namforecast'
        parts = instance_id.split("-", 1)
        if (len(parts) > 1):
            self.instance = parts[0]
            self.uid = parts[1]

        try:
            # connect to asgs database
            conn_str = f'host={self.host} port={self.port} dbname={self.db_name} user={self.user} password={self.pswd}'

            self.conn = psycopg2.connect(conn_str)
            self.conn.set_session(autocommit=True)
            self.cursor = self.conn.cursor()
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot connect to ASGS_DB. error {e}")

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


    # given instance id - save geoserver url (to access this mbtiles layer) in the asgs database
    def saveImageURL(self, name, url):
        self.logger.info(f'Updating DB record - instance id: {self.instance}  uid: {self.uid} with url: {url}')

        # format of mbtiles is ex: maxele.63.0.9.mbties
        # final key value will be in this format image.maxele.63.0.9
        key_name = "image." + os.path.splitext(name)[0]
        key_value = url

        try:
            sql_stmt = 'INSERT INTO "ASGS_Mon_config_item" (key, value, instance_id, uid) VALUES(%s, %s, %s, %s)'
            params = [f"{key_name}", f"{key_value}", self.instance, f"{self.uid}"]
            self.logger.debug(f"sql statement is: {sql_stmt} params are: {params}")

            self.cursor.execute(sql_stmt, params)
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot update ASGS_DB. error {e}")

    # need to retrieve some values - related to this run - from the ASGS DB
    # currently: Date, Cycle, Storm Name (if any), and Advisory (if any)
    # if more are needed, add to metadata_dict
    def getRunMetadata(self):
        metadata_dict = {
            'currentdate': '',
            'currentcycle': '',
            'advisory': '',
            'forcing.stormname': '',
            'forcing.metclass': '',
            'asgs.enstorm': '',
            'forcing.tropicalcyclone.stormname': '',
            'ADCIRCgrid': '',
            'monitoring.rmqmessaging.locationname': '',
            'instancename': ''
        }
        self.logger.info(f'Retrieving DB record metadata - instance id: {self.instance} uid: {self.uid}')

        try:
            for key in metadata_dict.keys():
                sql_stmt = 'SELECT value FROM "ASGS_Mon_config_item" WHERE instance_id=%s AND uid=%s AND key=%s'
                params = [self.instance, self.uid, key]
                self.logger.debug(f"sql statement is: {sql_stmt} params are: {params}")
                self.cursor.execute(sql_stmt, params)
                ret = self.cursor.fetchone()
                if ret:
                    self.logger.debug(f"value returned is: {ret}")
                    metadata_dict[key] = ret[0]
        except:
             e = sys.exc_info()[0]
             self.logger.error(f"FAILURE - Cannot retrieve run properties metadata from ASGS_DB. error {e}")
        finally:
            return metadata_dict

    # find the stationProps.csv file and insert the contents
    # into the adcirc_obs db of the ASGS postgres instance
    def insert_station_props(self, logger, geo, worksp, csv_file_path, geoserver_host):

        # where to find the stationProps.csv file
        logger.info(f"Saving {csv_file_path} to DB")
        logger.debug(f"DB name is: {self.get_dbname()}")

        # get the image server host name
        host = os.environ.get('FILESERVER_HOST_URL', 'none').strip()
        # need to remove the .edc from the geoserver_host for now - 7/18/22 - this no longer apllies for k8s runs
        #if (host == 'none'):
            #host = geoserver_host.replace('.edc', '')

        # open the stationProps.csv file and save in db
        # must create the_geom from lat, lon provided in csv file
        # also add to instance id column
        # and finally, create an url where the obs chart for each station can be accessed
        #try: catch this exception in calling program instead
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row.
            for row in reader:
                try:
                    logger.debug(f"opened csv file - saving this row to db: {row}")
                    filename = os.path.basename(row[6])
                    png_url = f"{host}/obs_pngs/{self.instanceId}/{filename}"
                    filename_list = os.path.splitext(filename)
                    json_url = f"{host}/obs_pngs/{self.instanceId}/{filename_list[0]}.json"
                    sql_stmt = "INSERT INTO stations (stationid, stationname, state, lat, lon, node, filename, the_geom, instance_id, imageurl, type, jsonurl) VALUES (%s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s),4326), %s, %s, %s, %s)"
                    params = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[4], row[3], self.instanceId, png_url, row[7], json_url]
                    logger.debug(f"sql_stmt: {sql_stmt} params: {params}")
                    self.cursor.execute(sql_stmt, params)
                except (Exception):
                    self.conn.commit()
                    raise IOError

        self.conn.commit()