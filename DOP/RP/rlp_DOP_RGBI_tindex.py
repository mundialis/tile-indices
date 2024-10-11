#!/usr/bin/env python3
#
################################################################################
#
# name: rlp_DOP_RGBI_tindex.py
#	    create tileindex for RGBI DOPs for Rhineland-Palatine (RLP)
#
# author: Victoria-Leandra Brunn
#       following: openNRW_DOP_tindex.py 
#                  by Anika Weinmann
#	               mundialis GmbH & Co. KG, Bonn
#	               https://www.mundialis.de
#
#
# data source: https://geobasis-rlp.de/data/dop20rgbi/current/meta4/dop20rgbi_jp2_07.meta4
#
# copyright? requirements?
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
# output: RLP_DOP20_tileindex.gpkg
##################################################################################



import ssl, wget
import sys
import os, json
from bs4 import BeautifulSoup

# douch security certificate issues and download metadata for whole RLP
ssl._create_default_https_context = ssl._create_unverified_context
metadata = wget.download('https://geobasis-rlp.de/data/dop20rgbi/current/meta4/dop20rgbi_jp2_07.meta4')

## --- extract .jp2 file urls from metadata --- ##
with open(metadata, 'r') as file:
    data = file.read() # puts file in data

Bs_data = BeautifulSoup(data, 'xml')
extracted_data = []
for tag in Bs_data.find_all():
    if tag.name == 'url' and tag.string:
        extracted_data.append(f"{tag.string.strip()}")

# keep only .jp2 files
urls = []
for item in extracted_data:
    if item.find('_rp.jp2') != -1:
        urls.append(item)

## --- create tileindex --- ##
parent_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
dop_name = [i.split('jp2/',1)[1] for i in urls]
num_dops = len(dop_name)

# create geojson and set structure
geojson_dict = {
    "type": "FeatureCollection",
    "name": "tindex",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
    "features": []
}

# set ID and define geometry
for num, dop in enumerate(dop_name):
    splitted_dop_name = os.path.basename(dop).split("_")
    x1 = int(splitted_dop_name[2]) * 1000
    y1 = int(splitted_dop_name[3]) * 1000
    x2 = x1 + 2000
    y2 = y1 + 2000

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

# fill geojson with urls and geometry
with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr " + parent_dir + "/RLP_DOP20_tileindex.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al " + parent_dir + "/RLP_DOP20_tileindex.gpkg")
tindex_verification = stream.read()
print(tindex_verification)
