import os, sys
import base_db

class ASGS_DB(base_db):

    # dbname looks like this: 'asgs_dashboard'
    # instance_id looks like this: '2744-2021050618-namforecast'
    def __init__(self, logger, instance_id):

        user = os.getenv('ASGS_DB_USERNAME', 'user').strip()
        pswd = os.getenv('ASGS_DB_PASSWORD', 'password').strip()
        host = os.getenv('ASGS_DB_HOST', 'host').strip()
        port = os.getenv('ASGS_DB_PORT', '5432').strip()
        db_name = os.getenv('ASGS_DB_DATABASE', 'db').strip()

        super().__init__(logger, user, pswd, db_name, host, port)


        # save whole Id
        self.instanceId = instance_id
        self.uid = instance_id
        self.instance = instance_id

        # also save separate parts i.e. '2744' and '2021050618-namforecast'
        parts = instance_id.split("-", 1)
        if (len(parts) > 1):
            self.instance = parts[0]
            self.uid = parts[1]


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
            'suite.project_code': '',
            'forcing.stormname': '',
            'forcing.metclass': '',
            'forcing.nwp.model': '',
            'forcing.tropicalcyclone.vortexmodel': '',
            'asgs.enstorm': '',
            'forcing.tropicalcyclone.stormname': '',
            'ADCIRCgrid': '',
            'monitoring.rmqmessaging.locationname': '',
            'instancename': '',
            'stormnumber': '',
            'downloadurl': '',
            'suite.model': ''
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
            if(len(metadata_dict['suite.project_code']) < 1):
                metadata_dict['suite.project_code'] = 'asgs'
            return metadata_dict

