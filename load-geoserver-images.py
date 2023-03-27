import os, sys
import fnmatch
import logging

from geo.Geoserver import Geoserver
from common.logging import LoggingUtil
from urllib.parse import urlparse
#from terria_catalogV8 import TerriaCatalog
from terria_catalogV8DB import TerriaCatalogDB
from asgs_db import ASGS_DB
from zipfile import ZipFile


# format raw date from DB
def format_raw_date(raw_date):
    run_date = "N/A"
    if raw_date:
        # raw date format is YYMMDD
        date_list = [raw_date[i:i + 2] for i in range(0, len(raw_date), 2)]
        if len(date_list) == 3:
            run_date = f"{date_list[1]}-{date_list[2]}-20{date_list[0]}"

    return run_date

# build info section metadata for use in creating
# the TerriaMap data catalog
def create_cat_info(meta_dict):

    info_dict = {}

    # first add all metadata that is common for hurricane nam forecasts
    event_date = format_raw_date(meta_dict['currentdate'])
    info_dict.update({"event_date": meta_dict['currentdate']})
    info_dict.update({"event_type": meta_dict['asgs.enstorm']})
    info_dict.update({"grid_type": meta_dict['ADCIRCgrid']})
    info_dict.update({"instance_name": meta_dict['instancename']})

    # added for PSC
    info_dict.update({"meteorological_model": meta_dict['forcing.tropicalcyclone.vortexmodel']})

    # if (meta_dict['forcing.metclass'] == 'tropical'):  just get these all of the time
    # added for PSC
    info_dict.update({"advisory": meta_dict['advisory']})
    info_dict.update({"ensemble_member": meta_dict['asgs.enstorm']})

    return info_dict

# create a new workspace in geoserver if it does not already exist
def add_workspace(logger, geo, worksp):
    logger.info(f"workspace: {worksp}")
    if (geo.get_workspace(worksp) is None):
        geo.create_workspace(workspace=worksp)

# upload raster layer styles, unless they already exist
def upload_styles(logger, geo):
    # find all styles in styles dir
    styles = os.listdir("./styles")

    # for each one check and see if they already exist in GeoServer
    for style in styles:
        style_name = os.path.splitext(style)[0]

        # check to see if style exists
        if geo.get_style(style_name) is None:
            # doesn't exist - upload
            logger.info(f"uploading style: {style_name}")
            geo.upload_style(f"./styles/{style}")

# tweak the layer title to make it more readable in Terria Map
def update_layer_title(logger, geo, instance_id, worksp, layer_name):
    logger.info(f"instance_id: {instance_id} layer_name: {layer_name}")
    run_date = ''
    # first get metadata from this model run
    db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
    asgsdb = ASGS_DB(logger, db_name, instance_id)
    meta_dict = asgsdb.getRunMetadata()
    run_date = format_raw_date(meta_dict['currentdate'])

    title = "N/A"
    if (meta_dict['forcing.metclass'] == 'synoptic'):
        title = f"Date: {run_date} Cycle: {meta_dict['currentcycle']} Forecast Type: {meta_dict['asgs.enstorm']} Location: {meta_dict['monitoring.rmqmessaging.locationname']} Instance: {meta_dict['instancename']} ADCIRC Grid: {meta_dict['ADCIRCgrid']} ({layer_name.split('_')[1]})"
    else:
        title = f"Date: {run_date} Cycle: {meta_dict['currentcycle']} Storm Name: {meta_dict['forcing.tropicalcyclone.stormname']} Advisory:{meta_dict['advisory']} Forecast Type: {meta_dict['asgs.enstorm']} Location: {meta_dict['monitoring.rmqmessaging.locationname']} Instance: {meta_dict['instancename']} ADCIRC Grid: {meta_dict['ADCIRCgrid']} ({layer_name.split('_')[1]})"
    logger.debug(f"setting this coverage: {layer_name} to {title}")

    geo.set_coverage_title(worksp, layer_name, layer_name, title)

    return title, meta_dict


def add_s3_coveragestore(logger, geo, s3_url, instance_id, worksp, layergrp):

    logger.info(f"instance_id: {instance_id} workspace: {worksp} s3_url: {s3_url}")

    # build layer_name or store_name (same)
    store_name = str(instance_id) + "_HEC-RAS"
    logger.info(f'Adding store: {store_name} into workspace: {worksp}')

    # create the s3 geotiff coveragestore
    ret = geo.create_s3cog_coveragestore(s3_url, store_name, workspace=worksp)

    logger.debug(f"Attempted to add s3 geotiff coverage store, s3_url: {s3_url}  return value: {ret}")
    if ('successful' in ret):  # coverage store successfully created
        # now create (publish) layer based on this coveragestore
        ret = geo.publish_s3cog_coverage(s3_url, store_name, workspace=worksp)

        logger.debug(f"Attempted to add s3 geotiff layer, s3_url: {s3_url}  return value: {ret}")
        if ('successful' in ret):  # layer successfully created (published)
            # now we just need to tweak the layer title to make it more readable in Terria Map
            title, meta_dict = update_layer_title(logger, geo, instance_id, worksp, store_name)

            # set the default style for this layer - maxele style for now
            style_name = "maxele_style"
            geo.set_default_style(worksp, store_name, style_name)

            # TODO: DO WE NEED THIS?
            # update DB with url of layer for access from website NEED INSTANCE ID for this
            # layer_url = f'{url}/{worksp}/wcs?service=WCS&version=1.1.1&request=DescribeCoverage&identifiers={worksp}:{store_name}'
            # logger.debug(f"Adding coverage store to DB, instanceId: {instance_id} coveragestore url: {layer_url}")
            # db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
            # asgsdb = ASGS_DB(logger, db_name, instance_id)
            # asgsdb.saveImageURL(file, layer_url)

            # add this layer to the wms layer group dict
            full_layername = f"{worksp}:{store_name}"
            # now get create and info section for later use in the TerriaMap data catalog
            info_dict = create_cat_info(meta_dict)
            layergrp["wms"].append({"title": title, "layername": full_layername, "metclass": meta_dict['forcing.metclass'], "info": info_dict})

    return layergrp


def add_imagemosaic_coveragestore(logger, geo, url, instance_id, worksp, imagemosaic_path, layergrp):
    # format of mbtiles is ex: maxele.63.0.9.mbtiles
    # pull out meaningful pieces of file name
    # get all files in mbtiles dir and loop through
    logger.info(f"instance_id: {instance_id} imagemosaic_path: {imagemosaic_path}")

    for file in fnmatch.filter(os.listdir(imagemosaic_path), '*.zip'):
        file_path = f"{imagemosaic_path}/{file}"
        logger.debug(f"add_imagemosaic_coveragestores: file={file_path}")
        layer_name = str(instance_id) + "_" + os.path.splitext(file)[0]
        logger.info(f'Adding layer: {layer_name} into workspace: {worksp}')

        # create coverage store and associate with .mbtiles file
        # also creates layer
        ret = geo.create_imagemosaic(lyr_name=layer_name,
                                       path=file_path,
                                       workspace=worksp)
        logger.debug(f"Attempted to add imagemosaic coverage store, file path: {file_path}  return value: {ret}")
        if (ret is None):  # coverage store successfully created

            # now we just need to tweak the layer title to make it more
            # readable in Terria Map
            title, meta_dict = update_layer_title(logger, geo, instance_id, worksp, layer_name)

            # set the default style for this layer
            if "swan" in layer_name:
                style_name = f"{layer_name.split('_')[1]}_style"
            else:
                style_name = f"{layer_name.split('_')[1][:-2]}_style"
            geo.set_default_style(worksp, layer_name, style_name)

            # update DB with url of layer for access from website NEED INSTANCE ID for this
            layer_url = f'{url}/{worksp}/wcs?service=WCS&version=1.1.1&request=DescribeCoverage&identifiers={worksp}:{layer_name}'
            logger.debug(f"Adding coverage store to DB, instanceId: {instance_id} coveragestore url: {layer_url}")
            db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
            asgsdb = ASGS_DB(logger, db_name, instance_id)
            asgsdb.saveImageURL(file, layer_url)

            # add this layer to the wms layer group dict
            full_layername = f"{worksp}:{layer_name}"
            # now get create and info section for later use in the TerriaMap data catalog
            info_dict = create_cat_info(meta_dict)
            layergrp["wms"].append({"title": title, "layername": full_layername, "metclass": meta_dict['forcing.metclass'], "info": info_dict})

        else:
            return None

    return layergrp

# add a coverage store to geoserver for each .mbtiles found in the staging dir
def add_mbtiles_coveragestores(logger, geo, url, instance_id, worksp, mbtiles_path, layergrp):
    # format of mbtiles is ex: maxele.63.0.9.mbtiles
    # pull out meaningful pieces of file name
    # get all files in mbtiles dir and loop through
    logger.info(f"instance_id: {instance_id} mbtiles_path: {mbtiles_path}")

    for file in fnmatch.filter(os.listdir(mbtiles_path), '*.mbtiles'):
        file_path = f"{mbtiles_path}/{file}"
        logger.debug(f"add_mbtiles_coveragestores: file={file_path}")
        layer_name = str(instance_id) + "_" + os.path.splitext(file)[0]
        logger.info(f'Adding layer: {layer_name} into workspace: {worksp}')

        # create coverage store and associate with .mbtiles file
        # also creates layer
        fmt = f"mbtiles?configure=first&coverageName={layer_name}"
        ret = geo.create_coveragestore(lyr_name=layer_name,
                                       path=file_path,
                                       workspace=worksp,
                                       file_type=fmt,
                                       content_type='application/vnd.sqlite3')
        logger.debug(f"Attempted to add coverage store, file path: {file_path}  return value: {ret}")
        if (ret is None):  # coverage store successfully created

            # now we just need to tweak the layer title to make it more
            # readable in Terria Map
            title, meta_dict = update_layer_title(logger, geo, instance_id, worksp, layer_name)

            # update DB with url of layer for access from website NEED INSTANCE ID for this
            layer_url = f'{url}/{worksp}/wcs?service=WCS&version=1.1.1&request=DescribeCoverage&identifiers={worksp}:{layer_name}'
            logger.debug(f"Adding coverage store to DB, instanceId: {instance_id} coveragestore url: {layer_url}")
            db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
            asgsdb = ASGS_DB(logger, db_name, instance_id)
            asgsdb.saveImageURL(file, layer_url)

            # add this layer to the wms layer group dict
            full_layername = f"{worksp}:{layer_name}"
            layergrp["wms"].append({"title": title, "layername": full_layername})

    return layergrp


# add a datastore in geoserver for the stationProps.csv file
# as of 4/8/21 this feature is broken in GeoServer so going to
# add a DB datastore for this data
'''
def add_props_datastore(logger, geo, instance_id, worksp, final_path):
    #stations_filename = "stationProps.csv"
    #insets_path = f"{final_path}/insets/{stations_filename}"
    #store_name = str(instance_id) + "_station_props"
    #ret = geo.create_datastore(name=store_name, path=insets_path, workspace=worksp)
    #logger.debug(f"Attempted to add data store, file path: {insets_path}  return value: {ret}")
'''

# add a datastore in geoserver for the stationProps.csv file
def add_props_datastore(logger, geo, instance_id, worksp, final_path, geoserver_host, layergrp):
    logger.info(f"Adding the station properties datastore for instance id: {instance_id}")
    # set up paths and datastore name
    # TODO put these in ENVs
    stations_filename = "stationProps.csv"
    csv_file_path = f"{final_path}/insets/{stations_filename}"
    store_name = str(instance_id) + "_station_props"
    dbname = "adcirc_obs"
    table_name = "stations"
    style_name = "observations_style_v2"

    logger.debug(f"csv_file_path: {csv_file_path} store name: {store_name}")

    # get asgs db connection
    asgs_obsdb = ASGS_DB(logger, dbname, instance_id)
    # save stationProps file to db
    try: # make sure this completes before moving on - observations may not exist for this grid
        asgs_obsdb.insert_station_props(logger, geo, worksp, csv_file_path, geoserver_host)
    except (IOError, OSError):
        e = sys.exc_info()[0]
        logger.warning(f"WARNING - Cannot save station data in {dbname} DB. Error: {e}")
        #return layergrp

    # ... using pre-defined postgresql JNDI feature store in Geoserver
    ret = geo.create_jndi_featurestore(store_name, worksp, overwrite=False)
    if ret is None: # successful

        logger.info(f"Added JNDI featurestore: {store_name}")
        # now publish this layer with an SQL filter based on instance_id
        sql = f"select * from stations where instance_id='{instance_id}'"
        name = f"{instance_id}_station_properies_view"

        # TODO probably need to update this name - 5/21/21 - okay updated ...
        #  but maybe need to make this a little less messy
        db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
        asgsdb = ASGS_DB(logger, db_name, instance_id)
        meta_dict = asgsdb.getRunMetadata()
        raw_date = meta_dict['currentdate']
        if raw_date:
            # raw date format is YYMMDD
            date_list = [raw_date[i:i + 2] for i in range(0, len(raw_date), 2)]
            if len(date_list) == 3:
                run_date = f"{date_list[1]}-{date_list[2]}-20{date_list[0]}"
        if (meta_dict['forcing.metclass'] == 'synoptic'):
            title = f"NOAA Observations - Date: {run_date} Cycle: {meta_dict['currentcycle']} Forecast Type: {meta_dict['asgs.enstorm']} Location: {meta_dict['monitoring.rmqmessaging.locationname']} Instance: {meta_dict['instancename']} ADCIRC Grid: {meta_dict['ADCIRCgrid']}"
        else:
            title = f"NOAA Observations - Date: {run_date} Cycle: {meta_dict['currentcycle']} Storm Name: {meta_dict['forcing.tropicalcyclone.stormname']} Advisory:{meta_dict['advisory']} Forecast Type: {meta_dict['asgs.enstorm']} Location: {meta_dict['monitoring.rmqmessaging.locationname']} Instance: {meta_dict['instancename']} ADCIRC Grid: {meta_dict['ADCIRCgrid']}"
        geo.publish_featurestore_sqlview(name, title, store_name, sql, key_column='gid', geom_name='the_geom', geom_type='Geometry', workspace=worksp)

        # now set the default style
        geo.set_default_style(worksp, name, style_name)

        # add this layer to the wfs layer group dict
        full_layername = f"{worksp}:{name}"
        # now get create and info section for later use in the TerriaMap data catalog
        info_dict = create_cat_info(meta_dict)
        layergrp["wfs"].append({"title": title, "layername": full_layername, "metclass": meta_dict['forcing.metclass'], "info": info_dict})

    return layergrp

# This only needs to get called if the current run is for a tropical storm/cyclone or hurricane
# It will look for shapefile layers, related to the storm, in /data/<instancename>/input/shapefiles
# and create layers for them in GeoServer
# expecting to find cone.zip, track.zip and points.zip
def add_shapefile_datastores(logger, geo, instance_id, worksp, shp_path, layergrp):
    logger.info(f"add_shapefile_datastores: instance_id: {instance_id} shp_path: {shp_path}")

    new_layergrp = layergrp

    # retrieve run.properties metadata fro this instance_id
    db_name = os.getenv('ASGS_DB_DATABASE', 'asgs').strip()
    asgsdb = ASGS_DB(logger, db_name, instance_id)
    meta_dict = asgsdb.getRunMetadata()

    # now check to see if this is a tropical storm and only continue if it is
    if (meta_dict['forcing.metclass'] == 'tropical'):
        run_date = ''
        raw_date = meta_dict['currentdate']
        if raw_date:
            # raw date format is YYMMDD
            date_list = [raw_date[i:i + 2] for i in range(0, len(raw_date), 2)]
            if len(date_list) == 3:
                run_date = f"{date_list[1]}-{date_list[2]}-20{date_list[0]}"

        # find shapefile .zip files in shp_path
        print(run_date)
        try:
            for file in fnmatch.filter(os.listdir(shp_path), '*.zip'):
                param_name = os.path.splitext(file)[0]
                store_name = str(instance_id) + "_" + param_name
                zip_path = os.path.join(shp_path, file)
                logger.info(f'Adding layer: {store_name} into workspace: {worksp}')
                ret = geo.create_shp_datastore(zip_path, store_name=store_name, workspace=worksp, file_format='shp')

                if "successfully" in ret:  # successful

                    # get the filenames in the zip file to use as layer name
                    layer_name = ""
                    with ZipFile(zip_path, 'r') as zipObj:
                        # Get list of files names in zip
                        listOfiles = zipObj.namelist()
                        if listOfiles is not None:
                            layer_name = listOfiles[0].split(".")[0]

                    # create a title for the TerriaMap data catalog
                    advisory = layer_name.split("-")[1].split("_")[0]
                    title = f"- Date: {run_date} Storm Name: {meta_dict['forcing.tropicalcyclone.stormname']} Advisory: {advisory}  Instance: {meta_dict['instancename']} "
                    if param_name == 'cone':
                        title = "NHC: Cone of Uncertainty " + title
                    elif param_name == 'points':
                        title = "NHC: Forecast Points " + title
                    elif param_name == 'track':
                        title = "NHC: Forecast Track " + title
                    else:
                        title = "NHC: Unidentified Layer " + title

                    # now set the default style
                    style_name = f"storm_{param_name}_style"
                    logger.debug(f"setting style for layer {layer_name} to {style_name}")
                    geo.set_default_style(worksp, layer_name, style_name)

                    logger.debug(f"setting this coverage: {layer_name} to {title}")
                    full_layername = f"{worksp}:{layer_name}"
                    new_layergrp["nhc"].append({"title": title, "layername": full_layername})
        except:
            e = sys.exc_info()[0]
            logger.error(f"Error encountered while trying to create NHC shapefile layers in GeoServer: {e}")
            return new_layergrp

    logger.debug(f"add_shapefile_datastores: returning updated layer_grp: {new_layergrp}")
    return new_layergrp

# copy all .csv station files to the fileserver host to serve them from there
def copy_csvs(logger, geoserver_proj_path, instance_id, final_path):

    from_path = f"{final_path}/insets/"
    to_path = f"{geoserver_proj_path}/{instance_id}/"

    logger.info(f"Copying insets .csv files from: {from_path} to: {to_path}")

    # first create new directory if not already existing
    new_dir = f"{geoserver_proj_path}/{instance_id}"
    logger.debug(f"copy_csvs: Creating to path directory: {new_dir}")

    mkdir_cmd = f"mkdir -p {new_dir}"

    logger.debug(f"copy_csvs: mkdir_cmd={mkdir_cmd}")
    os.system(mkdir_cmd)

    # now go through any .json files in the insets dir, if it exists
    if (os.path.isdir(from_path)):
        for file in fnmatch.filter(os.listdir(from_path), '*.csv'):
            from_file_path = from_path + file
            to_file_path = to_path + file
            logger.debug(f"Copying .csv file from: {from_file_path}  to: {to_file_path}")
            scp_cmd = f"cp {from_file_path} {to_file_path}"
            os.system(scp_cmd)

# copy all .json station files to the fileserver host to serve them from there
def copy_jsons(logger, geoserver_proj_path, instance_id, final_path):

    from_path = f"{final_path}/insets/"
    to_path = f"{geoserver_proj_path}/{instance_id}/"

    logger.info(f"Copying insets .json files from: {from_path} to: {to_path}")

    # first create new directory if not already existing
    new_dir = f"{geoserver_proj_path}/{instance_id}"
    logger.debug(f"copy_jsons: Creating to path directory: {new_dir}")

    mkdir_cmd = f"mkdir -p {new_dir}"

    logger.debug(f"copy_jsons: mkdir_cmd={mkdir_cmd}")
    os.system(mkdir_cmd)

    # now go through any .json files in the insets dir, if it exists
    if (os.path.isdir(from_path)):
        for file in fnmatch.filter(os.listdir(from_path), '*.json'):
            from_file_path = from_path + file
            to_file_path = to_path + file
            logger.debug(f"Copying .json file from: {from_file_path}  to: {to_file_path}")
            scp_cmd = f"cp {from_file_path} {to_file_path}"
            os.system(scp_cmd)

# copy all .png files to the fileserver host to serve them from there
# if ssh_host is 'none' cp files to PV in k8s,
# instead of using /projects mounted on the geoserver host
def copy_pngs(logger, geoserver_host, geoserver_proj_path, instance_id, final_path):

    from_path = f"{final_path}/insets/"
    to_path = f"{geoserver_proj_path}/{instance_id}/"

    logger.info(f"Copying insets png files from: {from_path} to: {to_path}")

    # first create new directory if not already existing
    new_dir = f"{geoserver_proj_path}/{instance_id}"
    logger.debug(f"copy_pngs: Creating to path directory: {new_dir}")

    mkdir_cmd = f"mkdir -p {new_dir}"
    logger.debug(f"copy_pngs: mkdir_cmd={mkdir_cmd}")
    os.system(mkdir_cmd)

    # now go through any .png files in the insets dir, if it exists
    if (os.path.isdir(from_path)):
        for file in fnmatch.filter(os.listdir(from_path), '*.png'):
            from_file_path = from_path + file
            to_file_path = to_path + file
            logger.debug(f"Copying .png file from: {from_file_path}  to: {to_file_path}")
            scp_cmd = f"cp {from_file_path} {to_file_path}"
            os.system(scp_cmd)

    # also now pick up legend .png files in the tiff directory
    from_path = f"{final_path}/tiff/"
    if (os.path.isdir(from_path)):
        for file in fnmatch.filter(os.listdir(from_path), '*.png'):
            from_file_path = from_path + file
            to_file_path = to_path + file
            logger.debug(f"Copying .png file from: {from_file_path}  to: {to_file_path}")
            scp_cmd = f"cp {from_file_path} {to_file_path}"
            os.system(scp_cmd)


# given an instance id and an input dir (where to find mbtiles)
# add the mbtiles to the specified GeoServer (configured with env vars)
# then update the specified DB with the access urls (configured with env vars)

def main(args):

    # define main data dir
    data_directory = "/data"

    # define dict to hold all of the layers created in this run
    # arrays contain sub-dicts like this: {"title": "", "layername": ""}
    layergrp = {
                 "wms": [],
                 "wfs": [],
                 "nhc": []
               }

    # get the log level and directory from the environment
    log_level: int = int(os.getenv('LOG_LEVEL', logging.INFO))
    log_path: str = os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs'))

    # create the dir if it does not exist
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # create a logger
    logger = LoggingUtil.init_logging("APSVIZ.load-geoserver-images", level=log_level, line_format='medium',
                                      log_file_path=log_path)

    # process args
    if not args.instanceId:
        print("Need instance id on command line: --instanceId <instanceid>")
        return 1
    instance_id = args.instanceId.strip()

    if args.HECRAS_URL:
        hecras_url = args.HECRAS_URL.strip()
    else:
        hecras_url = None

    # collect needed info from env vars
    user = os.getenv('GEOSERVER_USER', 'user').strip()
    pswd = os.environ.get('GEOSERVER_PASSWORD', 'password').strip()
    url = os.environ.get('GEOSERVER_URL', 'url').strip()
    worksp = os.environ.get('GEOSERVER_WORKSPACE', 'ADCIRC').strip()
    geoserver_host = os.environ.get('GEOSERVER_HOST', 'host.here.org').strip()
    geoserver_proj_path = os.environ.get('FILESERVER_OBS_PATH', '/obs_pngs').strip()
    logger.debug(f"Retrieved GeoServer env vars - url: {url} workspace: {worksp} geoserver_host: {geoserver_host} geoserver_proj_path: {geoserver_proj_path}")

    logger.info(f"Connecting to GeoServer at host: {url}")
    # create a GeoServer connection
    geo = Geoserver(url, username=user, password=pswd)

    # create a new workspace in geoserver if it does not already exist
    add_workspace(logger, geo, worksp)

    # upload raster styles, if they don't already exist
    upload_styles(logger, geo)

    if (hecras_url):
        final_layergrp = add_s3_coveragestore(logger, geo, hecras_url, instance_id, worksp, layergrp)
    else:
        # final dir path needs to be well defined
        # dir structure looks like this: /data/<instance id>/mbtiles/<parameter name>.<zoom level>.mbtiles
        final_path = f"{data_directory}/{instance_id}/final"
        #mbtiles_path = final_path + "/mbtiles"
        imagemosaic_path = final_path + "/cogeo"
        shp_path = f"{data_directory}/{instance_id}/input/shapefiles"

        # add a coverage store to geoserver for each .mbtiles found in the staging dir
        #new_layergrp = add_mbtiles_coveragestores(logger, geo, url, instance_id, worksp, mbtiles_path, layergrp)
        new_layergrp = add_imagemosaic_coveragestore(logger, geo, url, instance_id, worksp, imagemosaic_path, layergrp)
        # if add image mosaic failed exit program with an error
        if(new_layergrp is None):
            logger.info("Error encountered while loading image mosaic into GeoServer - program exiting")
            raise SystemExit()

        # now put NOAA OBS .csv file into geoserver
        next_layergrp = add_props_datastore(logger, geo, instance_id, worksp, final_path, geoserver_host, new_layergrp)
        if (new_layergrp is None):
            logger.info("Error encountered while loading noaa observation layer into GeoServer - program exiting")
            raise SystemExit()

        # check to see if this is a tropical storm, and if so, add storm related shapefiles to GeoServer
        final_layergrp = add_shapefile_datastores(logger, geo, instance_id, worksp, shp_path, next_layergrp)

        # finally copy all .png & .json files to the fileserver host to serve them from there
        copy_pngs(logger, geoserver_host, geoserver_proj_path, instance_id, final_path)
        copy_jsons(logger, geoserver_proj_path, instance_id, final_path)
        copy_csvs(logger, geoserver_proj_path, instance_id, final_path)

    # update TerriaMap data catalog
    #tc = TerriaCatalog(data_directory, geoserver_host, pswd)
    #tc.update(final_layergrp)

    # save TerriaMap data catalog to DB
    tc_db = TerriaCatalogDB(data_directory, geoserver_host, pswd)
    tc_db.update(final_layergrp)

    # geo.upload_style("./st.xml", "maxele_style", "ADCIRC_2022", sld_version='1.0.0', overwrite=False)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument('--instanceId', default=None, help='instance id of db entry for this model run', type=str)
    parser.add_argument('--HECRAS_URL', default=None, help='link to COG GeoTIFF in s3 indicating this is a HEC/RAS model run', type=str)

    args = parser.parse_args()

    sys.exit(main(args))
