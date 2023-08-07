############################################################################
#
# NAME:         openNRW_nDSM_tindex.py
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of openNRW nDSM imagery files
#
# Data source:  https://www.opengeodata.nrw.de/produkte/geobasis/ndom50_tiff/ndom50_tiff/
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
#   python3 nDSM/NRW/openNRW_nDSM_tindex.py
# Output:
#   nDSM/NW/nrw_ndom_tindex_proj.gpkg.gz

import os
import json

# Digitale Orthophotos (10-fache Kompression) - Paketierung: Einzelkacheln
URL = "https://www.opengeodata.nrw.de/produkte/geobasis/hm/ndom50_tiff/ndom50_tiff/"

os.chdir("nDSM/NRW/")

# check if we have lynx tool
stream = os.popen("which lynx")
output = stream.read()
if output is None or output == "":
    raise Exception("lynx required, please install lynx first")

# full tile index with 35860 NRW nDSMs
get_ndsm_cmd = f"lynx -dump -nonumbers -listonly {URL} | grep www.opengeodata.nrw.de/produkte/geobasis/hm/ndom50_tiff/ndom50_tiff/ | grep 'tif$'"
stream = os.popen(get_ndsm_cmd)
ndsm_str = stream.read()
ndsm_list = ndsm_str.split()

# create GeoJson
num_ndsms = len(ndsm_list)
geojson_dict = {
  "type": "FeatureCollection",
  "name": "tindex",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
  "features": []
}

for num, ndsm in enumerate(ndsm_list):
    splitted_ndsm_name = os.path.basename(ndsm).split("_")
    x1 = int(splitted_ndsm_name[1][2:]) * 1000
    y1 = int(splitted_ndsm_name[2]) * 1000
    x2 = x1 + 1000
    y2 = y1 + 1000
    feat = {
        "type": "Feature", "properties": {
            "fid": num + 1,
            "location": ndsm
        },
        "geometry": {
            "type": "Polygon", "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
        }
    }
    geojson_dict["features"].append(feat)

with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr nrw_ndom_tindex_proj.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al nrw_ndom_tindex_proj.gpkg")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile("nrw_ndom_tindex_proj.gpkg.gz"):
    os.remove("nrw_ndom_tindex_proj.gpkg.gz")
stream = os.popen("gzip nrw_ndom_tindex_proj.gpkg")
create_gz = stream.read()
print("<nrw_ndom_tindex_proj.gpkg.gz> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("nrw_ndom_tindex_proj.gpkg"):
    os.remove("nrw_ndom_tindex_proj.gpkg")
