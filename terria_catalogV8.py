from urllib.request import urlopen
from urllib.parse import urlparse
from common.logging import LoggingUtil
from datetime import datetime, timedelta
import logging
import json
import os


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

class TerriaCatalog:

    cat_save_path = "/projects/ees/APSViz"

    test_cat = '{' \
        '"workbench": [ \
        ],' \
        '"catalog": [' \
        '{' \
            '"id": "05-02-2022",' \
            '"name": "ADCIRC Data - Run Date: 05-02-2022",' \
            '"type": "group",' \
            '"members": [' \
            ']' \
        '},' \
        '],' \
        '"corsDomains": [' \
            '"corsproxy.com",' \
            '"programs.communications.gov.au",' \
            '"www.asris.csiro.au",' \
            '"mapsengine.google.com"' \
        '],' \
        '"homeCamera": {' \
            '"west": -96,' \
            '"south": 20,' \
            '"east": -61,' \
            '"north": 46' \
        '},' \
        '"baseMaps": {' \
            '"items": [' \
               '{' \
                '"item": {' \
                    '"id": "basemap-bing-roads",' \
                    '"name": "Bing Maps Roads",' \
               '},' \
               '"image": "build/TerriaJS/images/bing-maps-roads.png"' \
                '}' \
            ']' \
        '}' \
        '"viewerMode": "2D",' \
    '}'

    cat_group = '{' \
        '"id": "Id",' \
        '"type": "group",' \
        '"name": "Name",' \
        '"members": []' \
    '}'


    cat_wms_item = '{' \
        '"id": "Id",' \
        '"show": true,' \
        '"name": "Name",' \
        '"description": "This data is produced by the ADCIRC model and presented through the ADCIRC Prediction System Visualizer",' \
        '"dataCustodian": "RENCI",' \
        '"layers": "layers",' \
        '"type": "wms",' \
        '"url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wms",' \
        '"legends": [' \
            '{' \
                '"url": "legendUrl"' \
            '}' \
        '],' \
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
            '}' \
        ']' \
    '}'

    cat_wfs_item = '{' \
        '"id": "Id",' \
        '"show": true,' \
        '"name": "Name",' \
        '"description": "This data is produced by the ADCIRC model and presented through the ADCIRC Prediction System Visualizer",' \
        '"dataCustodian": "RENCI",' \
        '"type": "wfs",' \
        '"typeNames": "layers",' \
        '"url": "https://apsviz-geoserver.renci.org/geoserver/ADCIRC_2021/wms",' \
        '"featureInfoTemplate": {' \
            '"template": "<div class=\u2019stations\u2019><figure><img src={{imageurl}}><figcaption>{{stationname}}</figcaption></figure></div>"' \
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
            '}' \
        ']' \
    '}'



    def __init__(self, cat_url, host, userid, userpw):

        # get the log level and directory from the environment
        log_level: int = int(os.getenv('LOG_LEVEL', logging.INFO))
        log_path: str = os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs'))

        # create the dir if it does not exist
        if not os.path.exists(log_path):
           os.mkdir(log_path)

        # create a logger
        self.logger = LoggingUtil.init_logging("APSVIZ.load-geoserver-images", level=log_level, line_format='medium',
                                          log_file_path=log_path)
        # TODO: Going to have to figure out how the catalog url is set and how to use it in TerriaMap
        # self.cat_url = cat_url
        self.host = host
        self.userid = userid
        self.userpw = userpw
        self.fileserver_host = os.environ.get('FILESERVER_HOST', 'host.here.org').strip()
        self.cat_path = os.environ.get('FILESERVER_CAT_PATH', 'path').strip()
        #self.geoserver_url = os.environ.get('GEOSERVER_URL', 'url').strip()
        # try external url for now
        self.geoserver_url = "http://apsviz-geoserver-dev.apps.renci.org/geoserver/"
        self.geo_workspace = os.environ.get('GEOSERVER_WORKSPACE', 'url').strip()
        # load test json as default
        #self.cat_json = json.loads(self.test_cat)

        self.logger.info(f'cat_url: {cat_url}')
        # get json from url, if exists
        #if(cat_url is not None):
        if (self.cat_path is not None):
            # store the response of URL
            #response = urlopen(cat_url)
            #self.logger.info(f'read response: {response}')
            # storing the JSON response from url in data
            #self.cat_json = json.loads(response.read())
            self.logger.info(f'reading apsviz catalog file{self.cat_path}')
            f = open(self.cat_path)
            self.cat_json = json.load(f)
            f.close()

    # create url for legend
    # need to get just basic layername and the adcirc var name
    # from the layers var which is formatted like this:
    # ADCIRC_2021:3548-14-nhcOfcl_maxwvel.63.0.9
    # or this, in the case of the swan var:
    # ADCIRC_2021:3041-2021062306-namforecast_swan_HS_max.63.0.9
    def create_legend_url(self, layers):

        self.logger.debug(f'layers: {layers}')
        parts1 = layers.split(':')
        parts2 = parts1[1].split('_')
        if (len(parts2) > 3):
            # this is the swan var name (more dashes in name)
            # make it look like the other var names
            parts2 = [parts2[0], f"{parts2[1]}_{parts2[2]}_{parts2[3]}"]
        basic_layer_name = parts2[0]
        adcirc_var_parts = parts2[1].split('.')
        legend_url = f"http://{self.fileserver_host}/obs_pngs/{basic_layer_name}/{adcirc_var_parts[0]}.{adcirc_var_parts[1]}.colorbar.png"

        return legend_url

    # create a unique id for this catalog item
    # looks like this: 4007-2022050212-maxele
    # layername looks like this: ADCIRC_2021:4007-2022050212-namforecast_maxele.63.0.10
    def create_cat_itemid(self, layername, type):
        self.logger.debug(f'layername: {layername}  type: {type:}')
        item_id = ""
        # bunch of parsing to do
        # first get instance_id
        tmp = layername.split(':')
        str1 = tmp[1].split('-')
        id_pc1 = f"{str1[0]}-{str1[1]}"

        # if type=wms, get param name, otherwise assume "obs"
        if (type == "wms"):
            # have this in str1[2]: namforecast_maxele.63.0.10
            tmp = str1[2].split('_')
            str1 = tmp[1].split('.')
            id_pc2 = str1[0]
        else:
            id_pc2 = "obs"

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

    # create an info section for this group item
    # date_str looks like this: 05-02-2022
    # name looks like this: Maximum Water Level - Run Location: RENCI Cycle: 12 Storm Name: namforecast ADCIRC Grid: NCSC_SAB_v1.23 (maxele.63.0.10)
    # or this: NOAA Observations - Location: RENCI Cycle: 12 Storm Name: namforecast ADCIRC Grid: NCSC_SAB_v1.23
    def update_item_info(self, info, date_str, name):
        self.logger.info(f'info: {info}  date_str: {date_str}  name: {name}')
        # define search strings
        forecast_type_srch = "Storm Name:"
        grid_name_srch = "Grid:"
        # get forecast type
        forecast_idx = name.index(forecast_type_srch) + len(forecast_type_srch) + 1
        tmp = name[forecast_idx:] # gives something like this: namforecast ADCIRC Grid: NCSC_SAB_v1.23 (maxele.63.0.10)
        forecast_type = tmp.split(' ')[0]

        # get gridname
        grid_name_idx = name.index(grid_name_srch) + len(grid_name_srch) + 1
        tmp = name[grid_name_idx:] # gives something like this: NCSC_SAB_v1.23
        grid_name = tmp.split(' ')[0]

        # now update info content
        info[0]["content"] = date_str
        # event type
        info[1]["content"] = forecast_type

        info[2]["content"] = grid_name

        return info


    # should only need to update workbench array in the catalog group.
    def update_latest_results(self, latest_layer_ids):

        self.logger.info(f'latest_layer_ids: {latest_layer_ids}')

        if (len(latest_layer_ids) > 0):
            self.cat_json["workbench"] = latest_layer_ids


    # create a new catalog group for a new day.
    def create_cat_group(self, date_str):
        cat_group = {}
        cat_group = json.loads(self.cat_group)
        cat_group["id"] = date_str
        cat_group["name"] = f"ADCIRC Date - Run Date: {date_str}"

        return cat_group


    def create_wms_data_item(self,
                             item_id,
                             show,
                             name,
                             layers,
                             url,
                             legend_url):
        wms_item = {}
        wms_item = json.loads(self.cat_wms_item)
        wms_item["id"] = item_id
        wms_item["show"] = show
        wms_item["name"] = name
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
        wfs_item["typeNames"] = type_names
        wfs_item["url"] = url

        return wfs_item

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
                    name,
                    layers,
                    url=None,
                    show=True):

        new_group = False

        # create url for legend
        legend_url= self.create_legend_url(layers)
        self.logger.debug(f'legend_url: {legend_url}')
        item_id = self.create_cat_itemid(layers, "wms")
        self.logger.debug(f'id: {item_id}')
        if (url is None):
            url = f"{self.geoserver_url}{self.geo_workspace}/wms/{self.geo_workspace}?service=wms&version=1.3.0&request=GetCapabilities"
        self.logger.debug(f'url: {url}')

        # add this item to the CURRENT date group in the catalog, create/add to current date group, if it does not exist
        cat_group = self.cat_json['catalog'][0]
        date_str = self.get_datestr_from_layername(layers)
        if (date_str not in cat_group["name"]):
            # create new group
            new_group = True
            cat_group = self.create_cat_group(date_str)

        cat_item_list = cat_group["members"]

        wms_item = self.create_wms_data_item(item_id, show, name, layers, url, legend_url)
        info = self.update_item_info(wms_item["info"], date_str, name)
        wms_item["info"] = info
        cat_item_list.insert(0, wms_item)
        cat_group["members"] = cat_item_list

        # put this item list back into main catalog
        if (new_group):
            self.cat_json["catalog"].insert(0, cat_group)
        else:
            self.cat_json["catalog"][0] = cat_group

        return item_id


    # put the newest items at the top and only show the last 5 runs - not possible?
    # group is an ENUM - i.e. CatalogGroup.RECENT
    def add_wfs_item(self,
                    name,
                    typeNames,
                    url=None,
                    show=True):

        new_group = False

        item_id = self.create_cat_itemid(typeNames, "wfs")
        if (url is None):
            url = f"{self.geoserver_url}{self.geo_workspace}/wfs/{self.geo_workspace}?service=wfs&version=1.3.0&request=GetCapabilities"
        self.logger.debug(f'url: {url}')

        # add this item to the CURRENT date group in the catalog, create/add to current date group, if it does not exist
        cat_group = self.cat_json['catalog'][0]
        date_str = self.get_datestr_from_layername(typeNames)
        if (date_str not in cat_group["name"]):
            # create new group
            new_group = True
            cat_group = self.create_cat_group(date_str)

        cat_item_list = cat_group["members"]

        wfs_item = self.create_wfs_data_item(item_id, show, name, typeNames, url)
        info = self.update_item_info(wfs_item["info"], date_str, name)
        wfs_item["info"] = info
        cat_item_list.insert(0, wfs_item)
        cat_group["members"] = cat_item_list

        # put this item list back into main catalog
        if (new_group):
            self.cat_json.insert(0, cat_group)
        else:
            self.cat_json["catalog"][0] = cat_group

        return item_id


    # update the TerriaMap data catalog with a list of wms and wfs layers
    # layergrp looks like this: {'wms': [{'layername': '', 'title': ''}], 'wfs': [{'layername': '', 'title': ''}]}
    def update(self, layergrp):
        self.logger.info(f'layergrp: {layergrp}')
        # make array to save latest results maxele layer and noaa obs layer
        latest_layer_ids = []

        # first take care of the WMS layers
        for wms_layer_dict in layergrp["wms"]:
            item_id = self.add_wms_item(wms_layer_dict["title"], wms_layer_dict["layername"])
            if (("maxele" in wms_layer_dict["layername"]) and ("hsofs" in wms_layer_dict["title"])):
                latest_layer_ids.append(item_id)
        # now do WFS layers
        for wfs_layer_dict in layergrp["wfs"]:
            item_id = self.add_wfs_item(wfs_layer_dict["title"], wfs_layer_dict["layername"])
            if ("hsofs" in wfs_layer_dict["title"]):
                latest_layer_ids.append(item_id)

        self.update_latest_results(latest_layer_ids)

        # now delete the groups older than 14 days
        #self.rm_oldest_groups()

        # now save all of these updates to the catalog file
        self.save()


    # save the current version (in memory) to a local file
    # and then move that file to a remote host:/dir
    def save(self):

        tmp_path = "/data/tmp_cat.json"
        # save catalog file to local tmp file
        with open(tmp_path, 'w') as f:
            json.dump(self.cat_json, f, indent=4)

        ''' do not move anywhere until testing
        url_parts = urlparse(self.cat_url)
        to_host = self.host
        to_path = self.cat_save_path + url_parts.path

        to_path = f"{self.userid}@{to_host}:{to_path}"
        self.logger.info(f'to_path: {to_path}')
        scp_cmd = f'scp -r -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {tmp_path} {to_path}'
        os.system(scp_cmd)
        '''
