import pycurl
import os
import sys

# Creates the COG coveragestore; Data will uploaded to the server.
def main(args):

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

    workspace = "ADCIRC_TEST"
    overwrite=False
    file_type: str = "GeoTIFF"
    content_type: str = "image/tiff"

    file_name = os.path.basename(path)
    print(file_name)
    f = file_name.split(".")
    if len(f) > 0:
        file_name = f[0]
    else:
        print(f"Ilegal file name: {file_name}")
        sys.exit(0)
    layer_name = f"{instance_id}_{file_name}"
    print(layer_name)

    file_type = file_type.lower()

    url = '{0}/rest/workspaces/{1}/coveragestores/{2}/file.{3}?coverageName={2}'.format(
            service_url, workspace, layer_name, file_type)
    print(url)

    headers = {
        "content-type": content_type
    }

    r = None
    try:
        with open(path, 'rb') as f:
            r = requests.put(url, data=f, auth=(
                self.username, self.password), headers=headers)

        if r.status_code != 201:
            print('{}: The coveragestore can not be created!'.format(r.status_code))

    except Exception as e:
        print("Error: {}".format(e))


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