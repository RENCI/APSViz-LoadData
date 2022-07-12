# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

import pycurl
import os
import sys

# callback class for reading the files
class FileReader:
    def __init__(self, fp):
        self.fp = fp

    def read_callback(self, size):
        return self.fp.read(size)

def create_cog_coveragestore(instance_id, path, username, password, service_url, workspace):
    print("Creating COG coveragestore")
    content_type = 'image/tiff'
    overwrite = False
    file_name = os.path.basename(path)
    print(file_name)
    f = file_name.split(".")
    if len(f) > 0:
        file_name = f[0]
    else:
        print(f"Ilegal file name: {file_name}")
        sys.exit(0)
    lyr_name = f"{instance_id}_{file_name}"
    print(lyr_name)
    file_type = f"mbtiles?configure=first&coverageName={lyr_name}"

    try:
        file_size = os.path.getsize(path)
        c = pycurl.Curl()
        file_name = lyr_name

        c.setopt(pycurl.USERPWD, username + ':' + password)
        c.setopt(c.URL, '{0}/rest/workspaces/{1}/coveragestores/{2}/file.{3}'.format(
            service_url, workspace, file_name, file_type))
        c.setopt(pycurl.HTTPHEADER, [
                 "Content-type:{}".format(content_type)])
        c.setopt(pycurl.READFUNCTION, FileReader(
            open(path, 'rb')).read_callback)
        c.setopt(pycurl.INFILESIZE, file_size)
        if overwrite:
            c.setopt(pycurl.PUT, 1)
        else:
            c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.UPLOAD, 1)
        c.setopt(pycurl.VERBOSE, 1)
        c.perform()
        certinfo = c.getinfo_raw(pycurl.INFO_CERTINFO)
        print(certinfo)
        c.close()
    except Exception as e:
        print('Error: {}'.format(e))

def main(args):

    workspace = "ADCIRC_2021"

    # process args
    if not args.instanceId:
        print("Need instance id on command line: --instanceId <instanceid>")
        return 1
    instance_id = args.instanceId.strip()
    print(instance_id)

    if not args.dataFile:
        print("Need data file name (full path) on command line: --dataFile <datafilename>")
        return 1
    path = args.dataFile.strip()
    print(path)

    if not args.serverUrl:
        print("Need GeoServer url on command line: --serverUrl <serverurl>")
        return 1
    service_url = args.serverUrl.strip()
    print(service_url)

    if not args.userName:
        print("Need GeoServer user name on command line: --userName <username>")
        return 1
    username = args.userName.strip()
    print(username)

    if not args.password:
        print("Need GeoServer password on command line: --password <password>")
        return 1
    password = args.password.strip()
    print(password)

    create_cog_coveragestore(instance_id, path, username, password, service_url, workspace)

    content_type='application/vnd.sqlite3'
    overwrite=False
    file_name = os.path.basename(path)
    print(file_name)
    f = file_name.split(".")
    if len(f) > 0:
        file_name = f[0]
    else:
        print(f"Ilegal file name: {file_name}")
        sys.exit(0)
    lyr_name = f"{instance_id}_{file_name}" 
    print(lyr_name)
    file_type = f"mbtiles?configure=first&coverageName={lyr_name}"

    try:
        file_size = os.path.getsize(path)
        c = pycurl.Curl()
        file_name = lyr_name

        c.setopt(pycurl.USERPWD, username + ':' + password)
        c.setopt(c.URL, '{0}/rest/workspaces/{1}/coveragestores/{2}/file.{3}'.format(
            service_url, workspace, file_name, file_type))
        c.setopt(pycurl.HTTPHEADER, [
                 "Content-type:{}".format(content_type)])
        c.setopt(pycurl.READFUNCTION, FileReader(
            open(path, 'rb')).read_callback)
        c.setopt(pycurl.INFILESIZE, file_size)
        if overwrite:
            c.setopt(pycurl.PUT, 1)
        else:
            c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.UPLOAD, 1)
        c.setopt(pycurl.VERBOSE, 1)
        c.perform()
        certinfo = c.getinfo_raw(pycurl.INFO_CERTINFO)
        print(certinfo)
        c.close()
    except Exception as e:
        print('Error: {}'.format(e))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument('--instanceId', default=None, help='instance id of db entry for this model run', type=str)
    parser.add_argument('--dataFile', default=None, help='name of the data file (full path) to upload to geoserver', type=str)
    parser.add_argument('--serverUrl', default=None, help='url for the geoserver instance', type=str)
    parser.add_argument('--userName', default=None, help='user name for access to the geoserver instance', type=str)
    parser.add_argument('--password', default=None, help='password for access to the geoserver instance', type=str)

    args = parser.parse_args()

    sys.exit(main(args))

