############################################################################
#
# MODULE:      SL_DTM_tindex
# AUTHOR(S):   Kim Kaiser, Anika Weinmann
# PURPOSE:     Creates a tile index of Saarland DTM files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json

import requests
from xml.etree import ElementTree as ET
from osgeo import gdal
import pathlib

# Set Parameter
BASE_URL = "https://www.shop.lvgl.saarland.de"
DSM_URL = "/cloud/public.php/dav/files/NK8ndP55qAqGEZD/OD_DGM1_2025_tif_LK/"
URL = f"{BASE_URL}{DSM_URL}"
TOKEN = "NK8ndP55qAqGEZD"

EPSG_CODE = 25832
TILE_SIZE = 1000
OUTPUT_FILE = "SL_DTM_tindex_proj.gpkg.gz"
os.chdir("DTM/SL/")

gdal.UseExceptions()

def create_tindex_by_filename(data_list):
    # create GeoJson
    geojson_dict = {
        "type": "FeatureCollection",
        "name": "tindex",
        "crs": {
            "type": "name",
            "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG_CODE}"},
        },
        "features": [],
    }

    # get coordinates from filename
    for num, file_url in enumerate(data_list):
        filename = pathlib.Path(file_url).name.replace(".tif", "")
        splitted_data_name = filename.split("_")
        x1 = int(splitted_data_name[2]) * 1000
        y1 = int(splitted_data_name[3]) * 1000
        x2 = x1 + TILE_SIZE
        y2 = y1 + TILE_SIZE
        feat = {
            "type": "Feature",
            "properties": {
                "fid": num + 1,
                "location": file_url,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]
                ],
            },
        }
        geojson_dict["features"].append(feat)

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f, indent=4)

    # create GPKG from GeoJson
    tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg


# get list of ZIP files in Nextcloud DGM1 folder
zip_list = []
response = requests.request(
    method="PROPFIND",
    url=URL,
    auth=(TOKEN, ""),
    headers={"Depth": "1"},
    timeout=30,
)
response.raise_for_status()
root = ET.fromstring(response.content)
ns = {"d": "DAV:"}

for item in root.findall("d:response", ns):
    href = item.findtext("d:href", namespaces=ns)
    zip_url = href
    if item.findtext("d:href", namespaces=ns).lower().endswith(".zip"):
        zip_list.append(zip_url)

# get TIFF data list
data_list = []
for url in zip_list:
    zip_url = f"/vsizip//vsicurl/{BASE_URL}{url}"

    # get ZIP directory
    zip_dirs = gdal.ReadDir(zip_url)
    for zip_dir in zip_dirs:
        subdir = f"{zip_url}/{zip_dir}"

        # get TIFF files
        files = gdal.ReadDir(subdir)
        for file in files:
            file_url = f"{subdir}/{file}"
            data_list.append(file_url)

# create tindex
tindex_gpkg = create_tindex_by_filename(data_list)

# verify
print("Verifying vector tile index:")
stream = os.popen(f"ogrinfo -so -al {tindex_gpkg}")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
stream = os.popen(f"gzip {tindex_gpkg}")
stream.read()
print(f"<{OUTPUT_FILE}> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile(tindex_gpkg):
    os.remove(tindex_gpkg)
