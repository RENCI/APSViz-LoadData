import os, sys
import base_db
import csv

class APSVIZ_GAUGES_DB(base_db):

    # dbname looks like this: 'apsviz_gauges'
    # instance_id looks like this: '2744-2021050618-namforecast'
    def __init__(self, logger, instance_id):

        user = os.getenv('APSVIZ_GAUGES_DB_USERNAME', 'user').strip()
        pswd = os.getenv('APSVIZ_GAUGES_DB_PASSWORD', 'password').strip()
        host = os.getenv('APSVIZ_GAUGES_DB_HOST', 'host').strip()
        port = os.getenv('APSVIZ_GAUGES_DB_PORT', '5432').strip()
        db_name = os.getenv('APSVIZ_GAUGES_DB_DATABASE', '5432').strip()

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
        # header of stationProps.csv looks like this:
        # StationId,StationName,Source,State,Lat,Lon,Node,Filename,Type
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip the header row.
            for index, row in enumerate(reader):
                try:
                    # check the row. columns that have missing data are returned
                    no_cols_data_msg: str = self.valid_csv_row(header, row, [5])

                    # if there was missing data log it
                    if no_cols_data_msg:
                        # log the failed columns
                        logger.error("Row %s had missing column data. Columns:", index+2, no_cols_data_msg)

                        # no need to process this row
                        continue

                    logger.debug(f"opened csv file - saving this row to db: {row}")
                    filename = os.path.basename(row[7])
                    png_url = f"{host}/obs_pngs/{self.instanceId}/{filename}"
                    filename_list = os.path.splitext(filename)
                    json_url = f"{host}/obs_pngs/{self.instanceId}/{filename_list[0]}.json"
                    csv_url = f"{host}/obs_pngs/{self.instanceId}/{filename_list[0]}.csv"
                    sql_stmt = "INSERT INTO stations (stationid, stationname, source, state, lat, lon, node, filename, the_geom, instance_id, imageurl, type, jsonurl, csvurl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s),4326), %s, %s, %s, %s, %s)"
                    params = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[5], row[4], self.instanceId, png_url, row[8], json_url, csv_url]
                    logger.debug(f"sql_stmt: {sql_stmt} params: {params}")
                    self.cursor.execute(sql_stmt, params)
                except (Exception):
                    self.conn.commit()
                    raise IOError

        self.conn.commit()

    def isObsRun(self):

        found = False

        try:
            sql_stmt = 'SELECT model_run_id FROM drf_apsviz_station WHERE model_run_id=%s'
            params = [self.instance]
            self.logger.debug(f"sql statement is: {sql_stmt} params are: {params}")
            self.cursor.execute(sql_stmt, params)
            ret = self.cursor.fetchone()
            if ret:
                self.logger.debug(f"value returned is: {ret}")
                found = True

        except:
            e = sys.exc_info()[0]
            self.logger.error(f"FAILURE - Cannot retrieve instance id from {self.dbname}. error {e}")
        finally:
            return found

    @staticmethod
    def valid_csv_row(header: list, row: list, optional=None) -> str:
        """
        Checks the data list to make sure there are values in each required element
        and log the missing data entry.

        :param header: The CSV data header
        :param row: The list of data
        :param optional: The list of indexes that are optional

        :return: A comma delimited string of the errant columns
        """
        # init the return
        no_data_col: list = []

        # if there are no optional values passed in just create an empty list
        if optional is None:
            optional = []

        # for each element in the row
        for index, value in enumerate(row):
            # is this a required value and doesn't have data
            if index not in optional and (value is None or len(value) == 0):
                # append the column to the list
                no_data_col.append(header[index])

        # return the failed cols
        return ','.join(no_data_col)