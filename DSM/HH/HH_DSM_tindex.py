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
# COPYRIGHT:    (C) 2024 Anika Weinmann, mundialis
#
# REQUIREMENTS: RemoteZip
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
# `GDALTINDEX=False`: creating the tiles out of the file names (only small
#                     improvement in runtime, because you still have to check
#                     with `gdalinfo` whether the tiles are valid files at all)
# Then call script like this:
#   python3 DSM/HH/HH_DSM_tindex.py
# Output:
#   DSM/HH/hh_dom_tindex_proj.gpkg.gz


import os
import json

from remotezip import RemoteZip


# Parameter for Berlin DOM txt files
URL = (
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/"
    "digitales_hoehenmodell_bdom/DOM1_XYZ_HH_2020_04_30.zip"
)
EPSG_CODE = 25832
FILE_EXTENSION = ".xyz"
TILE_SIZE = 1000
OUTPUT_FILE = "hh_dom_tindex_proj.gpkg.gz"
VSI_PART = "/vsizip/vsicurl/"
os.chdir("DSM/HH/")


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
        splitted_data_name = os.path.basename(
            data
        ).replace(FILE_EXTENSION, "").split("_")
        x1 = int(splitted_data_name[2]) * 1000
        y1 = int(splitted_data_name[3]) * 1000
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


# get XYZ data list
data_list = []
with RemoteZip(URL) as zip:
    for zip_info in zip.infolist():
        file_name = zip_info.filename
        # data_list.append(f"{VSI_PART}{URL}/{file_name}")
        data_list.append(file_name)

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
