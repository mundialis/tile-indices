############################################################################
#
# NAME:         BE_DSM_tindex.py
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of Berlin DOM/DSM txt files
#
# Data source:  https://www.opengeodata.nrw.de/produkte/geobasis/dop/dop/
#
# COPYRIGHT:    (C) 2023 by Markus Neteler, Anika Weinmann, mundialis
#
# REQUIREMENTS: lynx, gdal, gzip, sed
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
############################################################################
# Usage:
# Set Parameter `GDALTINDEX`
# `GDALTINDEX=True`: using `gdaltindex` (more correct limits of the tiles)
# `GDALTINDEX=False`: creating the tiles out of the file names (only small improvement in runtime, because you still have to check with `gdalinfo` whether the tiles are valid files at all )
# Then call script like this:
#   python3 DSM/BE/BE_DSM_tindex.py
# Output:
#   DSM/BE/be_dom_tindex_proj.gpkg.gz


import os
import json

from osgeo import gdal


# Parameter for Berlin DOM txt files
URL = "https://fbinter.stadt-berlin.de/fb/berlin/service_intern.jsp?id=a_dom1@senstadt&type=FEED"
GREP_STR = "https://fbinter.stadt-berlin.de/fb/atom/DOM/DOM1"
EPSG_CODE = 25833
FILE_EXTENSION = ".txt"
TILE_SIZE = 2000
OUTPUT_FILE = "be_dom_tindex_proj.gpkg.gz"
GDALTINDEX = True
VSI_PART = "/vsizip/vsicurl/"
os.chdir("DSM/BE/")


def create_tindex_by_filename(data_list):
    # create GeoJson
    geojson_dict = {
        "type": "FeatureCollection",
        "name": "tindex",
        "crs": {
            "type": "name",
            "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG_CODE}"},
        },
        "features": []
    }

    for num, data in enumerate(data_list):
        ds = gdal.Open(data)
        if ds is None:
            print(
                f"<{data}> is not a valid file and will be left out for "
                "tindex creation."
            )
            continue
        splitted_data_name = os.path.basename(
            data
        ).replace(FILE_EXTENSION, "").split("_")
        x1 = int(splitted_data_name[1]) * 1000
        y1 = int(splitted_data_name[2]) * 1000
        x2 = x1 + TILE_SIZE
        y2 = y1 + TILE_SIZE
        feat = {
            "type": "Feature", "properties": {
                "fid": num + 1,
                "location": data,
            },
            "geometry": {
                "type": "Polygon", "coordinates": [[
                    [x1, y1],
                    [x2, y1],
                    [x2, y2],
                    [x1, y2],
                    [x1, y1]
                ]],
            }
        }
        geojson_dict["features"].append(feat)

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f, indent=4)

    # create GPKG from GeoJson
    tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg


def create_tindex_by_gdaltindex(data_list):
    tiles_csv = "tiles.csv"
    tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
    with open(tiles_csv, "w") as f:
        for data in data_list:
            f.write(f"{data}\n")
    # create tile index
    tindex_cmd = (
        f"gdaltindex -f GPKG -t_srs EPSG:{EPSG_CODE} {tindex_gpkg} "
        f"--optfile {tiles_csv}"
    )
    stream = os.popen(tindex_cmd)
    stream.read()
    os.remove(tiles_csv)
    return tindex_gpkg


# check if we have lynx tool
stream = os.popen("which lynx")
output = stream.read()
if output is None or output == "":
    raise Exception("lynx required, please install lynx first")

# full tile index with 35860 NRW DOPs
get_data_cmd = f"lynx -dump -nonumbers -listonly '{URL}' | grep {GREP_STR} | grep 'zip$' | sed 's+^+{VSI_PART}+g'"
stream = os.popen(get_data_cmd)
data_str = stream.read()
data_list = []
from remotezip import RemoteZip
for data in data_str.split():
    with RemoteZip(data.replace(VSI_PART, "")) as zip:
        for zip_info in zip.infolist():
            file_name = zip_info.filename
            data_list.append(f"{data}/{file_name}")

# create tindex
if GDALTINDEX:
    tindex_gpkg = create_tindex_by_gdaltindex(data_list)
else:
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
