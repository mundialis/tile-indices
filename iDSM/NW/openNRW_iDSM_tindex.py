############################################################################
#
# MODULE:       openNRW_iDSM_tindex.py
# AUTHOR(S):    Lina Krisztian
# PURPOSE:      Create tile index of openNRW iDSM .laz files from
#               https://www.opengeodata.nrw.de/produkte/geobasis/hm/bdom50_las/bdom50_las/
# SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
############################################################################

# Usage:
#   python3 iDSM/NW/openNRW_iDSM_tindex.py
# Output:
#   iDSM/NW/nrw_iDSM_tindex_proj.gpkg.gz

import os
import json

# Bildbasiertes Digitales Oberflächenmodell 50 - Paketierung: Einzelkacheln
URL = "https://www.opengeodata.nrw.de/produkte/geobasis/hm/bdom50_las/bdom50_las/"

os.chdir("iDSM/NW/")

# check if we have lynx tool
stream = os.popen("which lynx")
output = stream.read()
if output is None or output == "":
    raise Exception("lynx required, please install lynx first")

# full tile index with NW iDSM
get_idsm_cmd = f"lynx -dump -nonumbers -listonly {URL} | grep {URL} | grep 'laz$'"
stream = os.popen(get_idsm_cmd)
idsm_str = stream.read()
idsm_list = idsm_str.split()

# create GeoJson
num_idsms = len(idsm_list)
geojson_dict = {
  "type": "FeatureCollection",
  "name": "tindex",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
  "features": []
}

for num, idsm in enumerate(idsm_list):
    splitted_idsm_name = os.path.basename(idsm).split("_")
    print(splitted_idsm_name)
    x1 = int(splitted_idsm_name[1][2:]) * 1000
    y1 = int(splitted_idsm_name[2]) * 1000
    x2 = x1 + 1000
    y2 = y1 + 1000
    feat = {
        "type": "Feature", "properties": {
            "fid": num + 1,
            "location": idsm
        },
        "geometry": {
            "type": "Polygon", "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
        }
    }
    geojson_dict["features"].append(feat)
# For debugging:
# print(geojson_dict)

with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr nw_idsm_tindex_proj.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al nw_idsm_tindex_proj.gpkg")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile("nw_idsm_tindex_proj.gpkg.gz"):
    os.remove("nw_idsm_tindex_proj.gpkg.gz")
stream = os.popen("gzip nw_idsm_tindex_proj.gpkg")
create_gz = stream.read()
print("<nw_idsm_tindex_proj.gpkg.gz> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("nw_idsm_tindex_proj.gpkg"):
    os.remove("nw_idsm_tindex_proj.gpkg")
