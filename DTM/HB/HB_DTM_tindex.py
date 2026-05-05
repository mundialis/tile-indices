############################################################################
#
# MODULE:      HB_DTM_tindex
# AUTHOR(S):   Anika Weinmann, Kim Kaiser
# PURPOSE:     Creates a tile index of Bremen and Bremerhaven DTM files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json

from remotezip import RemoteZip

# Set Parameter
# Separate URLs for Bremen und Bremerhaven
URLS = [
    "https://gdi2.geo.bremen.de/inspire/download/DGM/data/"
    "Gitternetz_DGM1_2017_HB_ASCII_XYZ.zip",
    "https://gdi2.geo.bremen.de/inspire/download/DGM/data/"
    "Gitternetz_DGM1_2015_BHV_ASCII_XYZ.zip",
]
EPSG_CODE = 25832
FILE_EXTENSION = ".xyz"
TILE_SIZE = 1000
OUTPUT_FILE = "hb_dgm1_tindex_proj.gpkg.gz"
os.chdir("DTM/HB/")


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

    for num, data in enumerate(data_list):
        splitted_data_name = (
            os.path.basename(data).replace(FILE_EXTENSION, "").split("_")
        )
        if "" in splitted_data_name:
            splitted_data_name.remove("")
        y1 = int(splitted_data_name[2]) * 1000
        x1 = int(splitted_data_name[1][2:]) * 1000
        y2 = y1 + TILE_SIZE
        x2 = x1 + TILE_SIZE
        feat = {
            "type": "Feature",
            "properties": {
                "fid": num + 1,
                "location": data,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
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
for URL in URLS:
    with RemoteZip(URL) as zip:
        for zip_info in zip.infolist():
            file_name = zip_info.filename
            if file_name.endswith(FILE_EXTENSION):
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
