#!/usr/bin/env python3
#
################################################################################
#
# MODULE:       rlp_DOP_RGBI_tindex.py
# AUTHOR(S):    Victoria-Leandra Brunn
# PURPOSE:      Create tileindex for RGBI DOPS for Rhineland-Palatinate (RLP/RP)
#               from https://geobasis-rlp.de/data/dop20rgbi/current/meta4/dop20rgbi_jp2_07.meta4
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
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
    if item.find('.jp2') != -1:
        urls.append(item)

## --- create tileindex --- ##
parent_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#dop_name = [i.split('jp2/',1)[1] for i in urls]
num_dops = len(urls)

# create geojson and set structure
geojson_dict = {
    "type": "FeatureCollection",
    "name": "tindex",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
    "features": []
}

# set ID and define geometry
for num, dop in enumerate(urls):
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

filepath = os.path.join(parent_dir, "RLP_DOP20_tileindex.gpkg")
# create GPKG from GeoJson
stream = os.popen("ogr2ogr " + filepath + " tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al " + filepath)
tindex_verification = stream.read()
print(tindex_verification)

# zip .gpkg
# package
if os.path.isfile(filepath + ".gz"):
    os.remove(filepath + ".gz")
stream = os.popen("gzip " + filepath)
create_gz = stream.read()
print("<RLP_DOP20_tileindex.gpkg.gz> created")

# cleanup
if os.path.isfile(metadata):
    os.remove(metadata)
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("RLP_DOP20_tileindex.gpkg"):
    os.remove("RLP_DOP20_tileindex.gpkg")
