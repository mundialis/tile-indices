############################################################################
#
# NAME:         openNRW_DOP_tindex.py
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of openNRW DOP 10cm imagery files
#
# Data source:  https://www.opengeodata.nrw.de/produkte/geobasis/lusat/akt/dop/dop_jp2_f10/
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
#   python3 DOP/NW/openNRW_DOP_tindex.py
# Output:
#   DOP/NW/NW_DOP10_tileindex.gpkg.gz

import os
import json

# Digitale Orthophotos (10-fache Kompression) - Paketierung: Einzelkacheln
URL = "https://www.opengeodata.nrw.de/produkte/geobasis/lusat/akt/dop/dop_jp2_f10/"

os.chdir("DOP/NW/")

# check if we have lynx tool
stream = os.popen("which lynx")
output = stream.read()
if output is None or output == "":
    raise Exception("lynx required, please install lynx first")

# gdalinfo /vsicurl/https://www.opengeodata.nrw.de/produkte/geobasis/lusat/akt/dop/dop_jp2_f10/dop10rgbi_32_531_5744_1_nw_2022.jp2 # > test.txt

# test case: a few DOPs only
# echo "/vsicurl/https://www.opengeodata.nrw.de/produkte/geobasis/lusat/akt/dop/dop_jp2_f10/dop10rgbi_32_531_5744_1_nw_2022.jp2" > opengeodata_nrw_dop10_URLs.csv
# echo "/vsicurl/https://www.opengeodata.nrw.de/produkte/geobasis/lusat/akt/dop/dop_jp2_f10/dop10rgbi_32_531_5745_1_nw_2022.jp2" >> opengeodata_nrw_dop10_URLs.csv

# full tile index with 35860 NRW DOPs
get_dop_cmd = f"lynx -dump -nonumbers -listonly {URL} | grep www.opengeodata.nrw.de/produkte/geobasis/lusat/akt/dop/ | grep 'jp2$' | sed 's+^+/vsicurl/+g'"
stream = os.popen(get_dop_cmd)
DOP_str = stream.read()
DOP_list = DOP_str.split()

# create GeoJson
num_dops = len(DOP_list)
geojson_dict = {
  "type": "FeatureCollection",
  "name": "tindex",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
  "features": []
}

for num, dop in enumerate(DOP_list):
    splitted_dop_name = os.path.basename(dop).split("_")
    x1 = int(splitted_dop_name[2]) * 1000
    y1 = int(splitted_dop_name[3]) * 1000
    x2 = x1 + 1000
    y2 = y1 + 1000
    feat = {
        "type": "Feature", "properties": {
            "fid": num + 1,
            "location": dop
        },
        "geometry": {
            "type": "Polygon", "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
        }
    }
    geojson_dict["features"].append(feat)

with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr openNRW_DOP10_tileindex.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al openNRW_DOP10_tileindex.gpkg")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile("openNRW_DOP10_tileindex.gpkg.gz"):
    os.remove("openNRW_DOP10_tileindex.gpkg.gz")
stream = os.popen("gzip openNRW_DOP10_tileindex.gpkg")
create_gz = stream.read()
print("<openNRW_DOP10_tileindex.gpkg.gz> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("openNRW_DOP10_tileindex.gpkg"):
    os.remove("openNRW_DOP10_tileindex.gpkg")
