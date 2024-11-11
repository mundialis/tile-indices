############################################################################
#
# NAME:         openNRW_DTM_tindex.py
#
# AUTHOR(S):    Victoria-Leandra Brunn
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of openNRW DTM .tif files
#
# Data source:  https://www.opengeodata.nrw.de/produkte/geobasis/hm/dgm1_tiff/dgm1_tiff/
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
#   python3 DTM/NW/openNRW_DTM_tindex.py
# Output:
#   DTM/NW/nrw_DTM_tindex_proj.gpkg.gz

import os
import json

# Digitales Geländemodell - Rasterweite 1 m (GeoTIFF) - Paketierung: Einzelkacheln
URL = "https://www.opengeodata.nrw.de/produkte/geobasis/hm/dgm1_tiff/dgm1_tiff/"

os.chdir("DTM/NW/")

# check if we have lynx tool
stream = os.popen("which lynx")
output = stream.read()
if output is None or output == "":
    raise Exception("lynx required, please install lynx first")

# full tile index with NW DTM
get_dtm_cmd = f"lynx -dump -nonumbers -listonly {URL} | grep https://www.opengeodata.nrw.de/produkte/geobasis/hm/dgm1_tiff/dgm1_tiff/ | grep 'tif$'"
stream = os.popen(get_dtm_cmd)
dtm_str = stream.read()
dtm_list = dtm_str.split()

# create GeoJson
num_dtms = len(dtm_list)
geojson_dict = {
  "type": "FeatureCollection",
  "name": "tindex",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
  "features": []
}

for num, dtm in enumerate(dtm_list):
    splitted_dtm_name = os.path.basename(dtm).split("_")
    print(splitted_dtm_name)
    x1 = int(splitted_dtm_name[2]) * 1000
    y1 = int(splitted_dtm_name[3]) * 1000
    x2 = x1 + 1000
    y2 = y1 + 1000
    feat = {
        "type": "Feature", "properties": {
            "fid": num + 1,
            "location": dtm
        },
        "geometry": {
            "type": "Polygon", "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
        }
    }
    geojson_dict["features"].append(feat)
print(geojson_dict)

with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr nw_dtm_tindex_proj.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al nw_dtm_tindex_proj.gpkg")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile("nw_dtm_tindex_proj.gpkg.gz"):
    os.remove("nw_dtm_tindex_proj.gpkg.gz")
stream = os.popen("gzip nw_dtm_tindex_proj.gpkg")
create_gz = stream.read()
print("<nw_dtm_tindex_proj.gpkg.gz> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("nw_dtm_tindex_proj.gpkg"):
    os.remove("nw_dtm_tindex_proj.gpkg")
