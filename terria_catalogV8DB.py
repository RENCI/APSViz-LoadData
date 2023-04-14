from urllib.request import urlopen
from urllib.parse import urlparse
from common.logging import LoggingUtil
from datetime import datetime, timedelta
from apsviz_db import APSVIZ_DB
import logging
import json
import os, sys


# handles editing of TerriaMap data catalog (apsviz.json)
# assumes skeleton catalog exists, with sections
# for latest results, recent runs (last 5) and archive (everything else)
#

'''
example wms dataset:
{
          "id": "4007-2022050212-maxele",
          "show": true,
          "type": "wms",
          "name": "Maximum Water Level - Run Location: RENCI Cycle: 12 Storm Name: namforecast ADCIRC Grid: hsofs (maxele.63.0.10)",
          "show": true,
          "description": "This data is produced by the ADCIRC model and presented through the ADCIRC Prediction System Visualizer",
          "dataCustodian": "RENCI",
          "layers": "ADCIRC_2021:4007-2022050212-namforecast_maxele.63.0.10",
          "url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wms/ADCIRC_2021?service=wfs&version=1.3.0&request=GetCapabilities",
          "legends": [
            {
              "url": "https://apsviz-geoserver.renci.org/obs_pngs/4007-2022050212-namforecast/maxele.63.colorbar.png"
            }
          ],
          "info": [
            {
              "name": "Event Date",
              "content": "05-02-2022",
              "show": false
            },
            {
              "name": "Event Type",
              "content": "Namforecast",
              "show": false
            },
            {
              "name": "Grid Type",
              "content": "hsofs",
              "show": false
            }
          ]
        }
        
example wfs dataset:
{
          "id": "4007-2022050212-obs",
          "show": true,
          "name": "NOAA Observations - Location: RENCI Cycle: 12 Storm Name: namforecast ADCIRC Grid: hsofs",
          "description": "NOAA Observations",
          "dataCustodian": "RENCI",
          "typeNames": "ADCIRC_2021:4007-2022050212-namforecast_station_properies_view",
          "type":"wfs",
          "url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wfs/ADCIRC_2021?service=WFS&version=1.1.0&request=GetCapabilities",
          "featureInfoTemplate": {
            "template": "<div class=\u2019stations\u2019><figure><img src={{imageurl}}><figcaption>{{stationname}}</figcaption></figure></div>"
          },
          "info": [
            {
              "name": "Event Date",
              "content": "05-02-2022",
              "show": false
            },
            {
              "name": "Event Type",
              "content": "Namforecast",
              "show": false
            },
            {
              "name": "Grid Type",
              "content": "hsofs",
              "show": false
            }
          ]
        },
        
        workbench array defines which datasets to autoload and display on map:
        "workbench": [
            "4007-2022050212-maxele",
            "4007-2022050212-obs"
        ]
'''

class TerriaCatalogDB:

    MAXELE_STYLE = 'maxele'
    MAXWVEL_STYLE = 'maxwvel'
    SWAN_STYLE = 'swan'

    cat_wms_item = '{' \
        '"id": "Id",' \
        '"show": true,' \
        '"name": "Name",' \
        '"description": "This data is produced by the ADCIRC model and presented through the ADCIRC Prediction System Visualizer",' \
        '"dataCustodian": "RENCI",' \
        '"styles": "maxele_style",' \
        '"layers": "layers",' \
        '"legends": [' \
            '{' \
                '"url": "url",' \
                '"urlMimeType": "image/png"' \
            '}' \
        '],' \
        '"type": "wms",' \
        '"url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wms",' \
        '"featureInfoTemplate": {' \
            '"template": "<div><b>Value:</b>  {{GRAY_INDEX}}</div>",' \
            '"formats": {' \
                '"GRAY_INDEX": {' \
                    '"type": "number",' \
                    '"maximumFractionDigits": 3' \
                '}' \
            '}' \
        '},' \
        '"info": [' \
            '{' \
                '"name": "Event Date",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Event Type",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Grid Type",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Instance Name",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Meteorological Model",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Advisory",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Ensemble Member",' \
                '"content": "Content",' \
                '"show": false' \
            '}' \
        ']' \
    '}'

    cat_wfs_item = '{' \
        '"id": "Id",' \
        '"show": true,' \
        '"name": "Name",' \
        '"description": "This data is produced by the ADCIRC model and presented through the ADCIRC Prediction System Visualizer",' \
        '"dataCustodian": "RENCI",' \
        '"type": "wms",' \
        '"layers": "layers",' \
        '"url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wms",' \
        '"featureInfoTemplate": {' \
            '"template": "<div class=\u2019stations\u2019><p><h3>{{stationname}}, {{state}}</h3></p><chart sources=\u0027{{csvurl}}\u0027 column-units=\u0027Forecast:Meters,Nowcast:Meters,NOAA NOS:Meters,NOAA Tidal:Meters,Difference:Meters\u0027 column-titles=\u0027Forecast:Forecast,NOAA NOS:NOAA NOS,NOAA Tidal:NOAA Tidal\u0027 title=\u0027{{stationname}}\u0027></chart></div>"' \
        '},' \
        '"info": [' \
            '{' \
                '"name": "Event Date",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Event Type",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Grid Type",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Instance Name",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Meteorological Model",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Advisory",' \
                '"content": "Content",' \
                '"show": false' \
            '},' \
            '{' \
                '"name": "Ensemble Member",' \
                '"content": "Content",' \
                '"show": false' \
            '}' \
        ']' \
    '}'

    cat_nhc_item = '{' \
         '"id": "Id",' \
         '"show": true,' \
         '"name": "Name",' \
         '"description": "This data is provided by the National Hurricame Center",' \
         '"dataCustodian": "NHC",' \
         '"type": "wms",' \
         '"layers": "layers",' \
         '"url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wms"' \
     '}'


    def __init__(self, data_directory, host, userpw):

        # get the log level and directory from the environment
        log_level: int = int(os.getenv('LOG_LEVEL', logging.INFO))
        log_path: str = os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs'))

        # create the dir if it does not exist
        if not os.path.exists(log_path):
           os.mkdir(log_path)

        # create a logger
        self.logger = LoggingUtil.init_logging("APSVIZ.load-geoserver-images", level=log_level, line_format='medium',
                                          log_file_path=log_path)

        self.data_directory = data_directory
        self.host = host
        # self.userid = userid
        self.userpw = userpw
        self.fileserver_host = os.environ.get('FILESERVER_HOST', 'host.here.org').strip()
        self.geoserver_url = os.environ.get('GEOSERVER_URL_EXT', 'url').strip()
        self.geo_workspace = os.environ.get('GEOSERVER_WORKSPACE', 'url').strip()

        # create apsviz db object
        self.apsviz_db = APSVIZ_DB(self.logger)


    # create url for wms legend
    # from the layers var which is formatted like this:
    # ADCIRC_2021:3548-14-nhcOfcl_maxwvel.63.0.9
    # or this, in the case of the swan var:
    # ADCIRC_2021:3041-2021062306-namforecast_swan_HS_max.63.0.9
    def create_legend_url(self, layers):

        self.logger.debug(f'layers: {layers}')
        parts1 = layers.split(':')
        workspace = parts1[0]
        layer_name = parts1[1]

        # need to use geoserver provided legend, but make it horizontal and transparent
        legend_url = f"{self.geoserver_url}/{workspace}/ows?service=WMS&request=GetLegendGraphic&TRANSPARENT=TRUE&LEGEND_OPTIONS=layout:horizontal&format=image%2Fpng&width=20&height=20&layer={layer_name}"

        return legend_url


    # get and return the cycle name in the title, if any
    def getCycle(self, name):
        self.logger.debug(f'getCycle name: {name}')
        srch_str = 'Cycle: '

        try:
            idx = name.index(srch_str)
            start_idx = idx + len(srch_str)
            cycle = name[start_idx:start_idx+2]

            return cycle

        except ValueError:
            return ''

    # get and return the storm name in the title, if any
    # looks like this in Title: Storm Name: {meta_dict['forcing.tropicalcyclone.stormname']} Advisory:
    def getStormName(self, name):
            self.logger.debug(f'getStormName name: {name}')
            srch_start_str = 'Storm Name: '
            srch_end_str = ' Advisory:'

            try:
                idx = name.index(srch_start_str)
                start_idx = idx + len(srch_start_str)
                end_idx = name.index(srch_end_str)
                storm_name = name[start_idx:end_idx]

                return storm_name

            except ValueError:
                return ''


    # create a unique id for this catalog item
    # looks like this: 4007-2022050212-namforecast-maxele
    # layername looks like this: ADCIRC_2021:4007-2022050212-namforecast_maxele63
    def create_cat_itemid(self, layername, type):
        self.logger.debug(f'layername: {layername}  type: {type:}')
        item_id = ""

        # bunch of parsing to do
        # first get instance_id
        tmp = layername.split(':')
        # if the instance id is not split from string
        # assume this layer is different because it is in storm format
        # ie 55555-13-nhcOfcl_maxwvel63
        # so just return whole string for id
        if (len(tmp) == 1):
            return(layername)

        # otherwise go ahead and parse as normal
        str1 = tmp[1].split('-')
        id_pc1 = f"{str1[0]}-{str1[1]}"

        # if type=wms, get param name, otherwise assume "obs"
        if (type == "wms"):
            # have this in str1[2]: namforecast_maxele63
            str1 = str1[2].split('_')
            id_pc2 = f"{str1[0]}-{str1[1]}"
        elif (type == "wfs"):
            # have this in str1[2]: nowcast_station_properies_view
            id_pc2 = f"{str1[2].split('_')[0]}-obs"
        else:  # NHC
            id_pc2 = f"{str1[0]}-nhc"

        item_id = f"{id_pc1}-{id_pc2}"

        return item_id

    # need date in format MM-DD-YYYY
    # layername look like this: ADCIRC_2021:4014-2022050218-namforecast_maxele.63.0.10
    def get_datestr_from_layername(self, layername):
        date_str = ""

        str_array = layername.split('-')
        time_pc = str_array[1]
        # now have 2022050218 in time_pc
        date_str = f"{time_pc[4:6]}-{time_pc[6:8]}-{time_pc[0:4]}"

        return date_str

    def get_datestr_from_title(self, title):
        date_str = ""
        srch_str = "Date:"
        str_len = len(srch_str)
        date_len = len("mm-dd-yyyy")

        # Find the first index of the srch_str
        index = title.index(srch_str)
        # now find start position of actual date string
        # need to add 1 to account for space
        date_idx = index + str_len + 1
        # collect full date string
        date_str = title[date_idx:date_idx + date_len]

        return date_str

    # return layer style appropriate for this layer
    # currently there are three styles:
    # maxele_style - default
    # maxwvel_style
    # swan_style
    def get_wms_style(self, layername):

        if self.MAXWVEL_STYLE in layername:
            return f'{self.MAXWVEL_STYLE}_style'
        elif self.SWAN_STYLE in layername:
            return f'{self.SWAN_STYLE}_style'
        else:
            return f'{self.MAXELE_STYLE}_style'


    # create an info section for this group item
    # date_str looks like this: 05-02-2022
    # name looks like this: Maximum Water Level - Run Location: RENCI Cycle: 12 Storm Name: namforecast ADCIRC Grid: NCSC_SAB_v1.23 (maxele.63.0.10)
    # or this: NOAA Observations - Location: RENCI Cycle: 12 Storm Name: namforecast ADCIRC Grid: NCSC_SAB_v1.23
    # def update_item_info(self, info, date_str, name):
    #     self.logger.info(f'info: {info}  date_str: {date_str}  name: {name}')
    #     # define search strings
    #     forecast_type_srch = "Forecast Type:"
    #     grid_name_srch = "Grid:"
    #     inst_name_srch = "Instance:"
    #
    #     # get forecast type
    #     forecast_idx = name.index(forecast_type_srch) + len(forecast_type_srch) + 1
    #     tmp = name[forecast_idx:] # gives something like this: 'nameforecast Location: PSC Instance: ec95d-al01-bob-psc ADCIRC Grid: ec95d'
    #     forecast_type = tmp.split(' ')[0]
    #
    #     # get gridname
    #     grid_name_idx = name.index(grid_name_srch) + len(grid_name_srch) + 1
    #     tmp = name[grid_name_idx:] # gives something like this: NCSC_SAB_v1.23
    #     grid_name = tmp.split(' ')[0]
    #
    #     # get instance name
    #     inst_name_idx = name.index(inst_name_srch) + len(inst_name_srch) + 1
    #     tmp = name[inst_name_idx:] # gives something like this: ec95d-nam-bob3
    #     inst_name = tmp.split(' ')[0]
    #
    #
    #     # now update info content
    #     info[0]["content"] = date_str
    #     # event type
    #     info[1]["content"] = forecast_type
    #     # grid name
    #     info[2]["content"] = grid_name
    #     # instance name
    #     info[3]["content"] = inst_name
    #
    #     return info

    # populate the info section for this group item
    def update_item_info(self, info, layer_info):
        self.logger.info(f'info: {info}')

        # update info content
        info[0]["content"] = layer_info["event_date"]
        # event type
        info[1]["content"] = layer_info["event_type"]
        # grid name
        info[2]["content"] = layer_info["grid_type"]
        # instance name
        info[3]["content"] = layer_info["instance_name"]

        # following info items added for PSC
        # meteorological model
        info[4]["content"] = layer_info["meteorological_model"]
        # advisory
        info[5]["content"] = layer_info["advisory"]
        # ensemble member
        info[6]["content"] = layer_info["ensemble_member"]

        return info

        # should only need to update workbench array in the catalog group.
        # select value from "ASGS_Mon_config_item" where uid like '2022070712-%' and key='adcirc.gridname';

    def update_latest_results(self, latest_layer_ids, metclass):
        self.logger.info(f'latest_layer_ids:{latest_layer_ids} metclass:{metclass}')

        # if this is not tropical run, just and see if the last tropical run takes prority
        if (metclass != 'tropical'):
            # check to see if there is already a tropical run for today
            todays_date = datetime.utcnow().strftime('%Y-%m-%d')
            self.logger.debug(f'todays_date:{todays_date}')
            member_ids = self.apsviz_db.get_tropical_run(todays_date)
            self.logger.debug(f'member_ids:{member_ids}')
            # are there any tropical runs already existing today?
            # if not, go ahead and add this run to the workbench
            # else just skip update of workbench
            if (member_ids is None):
                if (len(latest_layer_ids) > 0):
                    self.apsviz_db.update_workbench(latest_layer_ids)

        # if this is a tropical run, just put these layers in the workbench
        else:
            if (len(latest_layer_ids) > 0):
                self.apsviz_db.update_workbench(latest_layer_ids)


    # create a new catalog group for a new day.
    def create_cat_group(self, date_str):

        cat_name = f"ADCIRC Data - Run Date: {date_str}"
        self.apsviz_db.create_new_catalog(date_str, cat_name, False)



    def create_wms_data_item(self,
                             item_id,
                             show,
                             name,
                             style,
                             layers,
                             url,
                             legend_url):
        wms_item = {}
        wms_item = json.loads(self.cat_wms_item)
        wms_item["id"] = item_id
        wms_item["show"] = show
        wms_item["name"] = name
        wms_item["styles"] = style
        wms_item["layers"] = layers
        wms_item["url"] = url
        wms_item["legends"][0]["url"] = legend_url

        return wms_item

    def create_wfs_data_item(self,
                             item_id,
                             show,
                             name,
                             type_names,
                             url):
        wfs_item = {}
        wfs_item = json.loads(self.cat_wfs_item)
        wfs_item["id"] = item_id
        wfs_item["show"] = show
        wfs_item["name"] = name
        wfs_item["layers"] = type_names
        wfs_item["url"] = url

        return wfs_item

    def create_nhc_data_item(self,
                             item_id,
                             show,
                             name,
                             type_names,
                             url):
        nhc_item = {}
        nhc_item = json.loads(self.cat_nhc_item)
        nhc_item["id"] = item_id
        nhc_item["show"] = show
        nhc_item["name"] = name
        nhc_item["layers"] = type_names
        nhc_item["url"] = url

        return nhc_item

    # remove any groups 14 days older than the newest one
    def rm_oldest_groups(self):
        new_group_list = []

        # get list of current groups
        cat_group_list = self.cat_json['catalog']
        newest_date_str = cat_group_list[0]["id"]
        newest_date_obj = datetime.strptime(newest_date_str, '%m-%d-%Y')


        for group in cat_group_list:
            current_date_obj = datetime.strptime(group["id"], '%m-%d-%Y')
            delta = newest_date_obj - current_date_obj
            # delta is less than 14 days, add back into group list
            if delta <= timedelta(days=14):
                new_group_list.append(group)

        self.cat_json["catalog"] = new_group_list


    # put the newest items at the top and only show the last 5 runs
    # workspace, date, cycle, runtype, stormname, advisory, grid):
    # group is an ENUM - i.e. CatalogGroup.RECENT
    def add_wms_item(self,
                    metclass,
                    name,
                    layers,
                    wms_info,
                    project_code,
                    product_type,
                    url=None,
                    show=True):

        new_group = False

        # create url for legend
        legend_url= "N/A"
        legend_url= self.create_legend_url(layers)
        self.logger.debug(f'legend_url: {legend_url}')
        item_id = self.create_cat_itemid(layers, "wms")
        self.logger.debug(f'id: {item_id}')
        if (url is None):
            url = f"{self.geoserver_url}/{self.geo_workspace}/wms/{self.geo_workspace}?service=wms&version=1.3.0&request=GetCapabilities"
        self.logger.debug(f'url: {url}')

        # add to correct catalog date group, if that group does not exist, create a new one
        date_str = self.get_datestr_from_title(name)
        # check to see if this catalog group already exists
        if (not self.apsviz_db.find_cat_group(date_str)):
            # create new group
            self.create_cat_group(date_str)

        # set the correct style for this layer
        style = self.get_wms_style(layers)

        wms_item = self.create_wms_data_item(item_id, show, name, style, layers, url, legend_url)
        info = self.update_item_info(wms_item["info"], wms_info)
        wms_item["info"] = info

        # now add this member item to the catalog group
        grid_type = info[2]["content"]
        event_type = info[1]["content"]
        run_date = info[0]["content"]
        instance_name = info[3]["content"]
        advisory = info[5]["content"]
        # make sure this advisory is a real storm advisory number, if not (is a date) use empty string
        if (len(advisory) > 3):
            advisory = ''
        storm_name = self.getStormName(name)
        cycle = self.getCycle(name)
        if (len(cycle) < 1):
            cycle = advisory

        self.apsviz_db.add_cat_item(grid_type, event_type, run_date, instance_name, wms_item, metclass, storm_name, cycle, advisory, project_code, product_type)

        return item_id


    # put the newest items at the top and only show the last 5 runs - not possible?
    # group is an ENUM - i.e. CatalogGroup.RECENT
    def add_wfs_item(self,
                    metclass,
                    name,
                    typeNames,
                    wfs_info,
                    project_code,
                    product_type,
                    url=None,
                    show=True):

        item_id = self.create_cat_itemid(typeNames, "wfs")
        if (url is None):
            url = f"{self.geoserver_url}/{self.geo_workspace}/wfs/{self.geo_workspace}?service=wfs&version=1.3.0&request=GetCapabilities"
        self.logger.debug(f'url: {url}')

        # add to correct catalog date group, if that group does not exist, create a new one
        date_str = self.get_datestr_from_title(name)
        # check to see if this catalog group already exists
        if (not self.apsviz_db.find_cat_group(date_str)):
            # create new group
            self.create_cat_group(date_str)

        wfs_item = self.create_wfs_data_item(item_id, show, name, typeNames, url)
        info = self.update_item_info(wfs_item["info"], wfs_info)
        wfs_item["info"] = info

        # now add this member item to the catalog group
        grid_type = info[2]["content"]
        event_type = info[1]["content"]
        run_date = info[0]["content"]
        instance_name = info[3]["content"]
        advisory = info[5]["content"]
        # make sure this advisory is a real storm advisory number, if not (is a date) use empty string
        if (len(advisory) > 3):
            advisory = ''
        storm_name = self.getStormName(name)
        cycle = self.getCycle(name)
        if (len(cycle) < 1):
            cycle = advisory

        self.apsviz_db.add_cat_item(grid_type, event_type, run_date, instance_name, wfs_item, metclass, storm_name, cycle, advisory, project_code, product_type)

        return item_id

    # put the newest items at the top and only show the last 5 runs - not possible?
    # group is an ENUM - i.e. CatalogGroup.RECENT
    def add_nhc_item(self,
                     name,
                     typeNames,
                     url=None,
                     show=True):

        item_id = self.create_cat_itemid(typeNames, "nhc")
        if (url is None):
            url = f"{self.geoserver_url}/{self.geo_workspace}/wfs/{self.geo_workspace}?service=wfs&version=1.3.0&request=GetCapabilities"
        self.logger.debug(f'url: {url}')

        # add to correct catalog date group, if that group does not exist, create a new one
        date_str = self.get_datestr_from_title(name)
        # check to see if this catalog group already exists
        if (not self.apsviz_db.find_cat_group(date_str)):
            # create new group
            self.create_cat_group(date_str)

        nhc_item = self.create_nhc_data_item(item_id, show, name, typeNames, url)
        #self.apsviz_db.add_cat_item(grid_type, event_type, run_date, instance_name, wfs_item)
        self.apsviz_db.add_cat_item("NA", "NA", date_str, "NA", nhc_item)

        return item_id


    # update the TerriaMap data catalog with a list of wms and wfs layers
    # layergrp looks like this: {'wms': [{'layername': '', 'title': ''}], 'wfs': [{'layername': '', 'title': ''}]}
    def update(self, layergrp):
        self.logger.info(f'layergrp: {layergrp}')
        # make array to save latest results maxele layer and noaa obs layer
        latest_layer_ids = []
        metclass = ""

        # do nhc storm layers if any
        for nhc_layer_dict in layergrp["nhc"]:
            item_id = self.add_nhc_item(nhc_layer_dict["title"], nhc_layer_dict["layername"])

        # next take care of the WMS layers
        for wms_layer_dict in layergrp["wms"]:
            item_id = self.add_wms_item(wms_layer_dict["metclass"], wms_layer_dict["title"], wms_layer_dict["layername"], wms_layer_dict["info"], wms_layer_dict["project_code"], wms_layer_dict["product_type"])
            if ("maxele" in wms_layer_dict["layername"]):
                latest_layer_ids.append(item_id)
                metclass = wms_layer_dict["metclass"]
        # now do WFS layers
        for wfs_layer_dict in layergrp["wfs"]:
            item_id = self.add_wfs_item(wfs_layer_dict["metclass"], wfs_layer_dict["title"], wfs_layer_dict["layername"], wfs_layer_dict["info"], wfs_layer_dict["project_code"], wfs_layer_dict["product_type"])
            # if ("ec95d" in wfs_layer_dict["title"]):
            # put this layer on top
            latest_layer_ids.insert(0, item_id)

        self.update_latest_results(latest_layer_ids, metclass)

        # now delete the groups older than 14 days
        #self.rm_oldest_groups()
