############################################################################
#
# NAME:         NI_DOP_tindex.py
#
# AUTHOR(S):    Johannes Halbauer
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Download and modify tile index of Niedersachsen DOP files
#
# Data source:  https://ni-lgln-opengeodata.hub.arcgis.com/
#
# COPYRIGHT:    (C) 2025 Johannes Halbauer, mundialis
#
# REQUIREMENTS: wget
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
# Then call script like this:
#   python3 DOP/NI/NI_DOP_tindex.py
# Output:
#   DOP/NI/NI_DOP_tindex_proj.gpkg.gz


import os
import json
from datetime import datetime
import wget


# parameters
URL = (
    "https://arcgis-geojson.s3.eu-de.cloud-object-storage.appdomain.cloud/"
    "dop20/lgln-opengeodata-dop20.geojson"
)
OUTPUT_FILE = "NI_DOP_tindex_proj.gpkg.gz"
os.chdir("DOP/NI/")

# define geojson keys to rename
rename = {"rgbi": "location"}

# define geojson keys to keep
keep = ["location"]

# download tileindex
wget.download(URL, "tindex_orig.geojson", bar=None)

# read geojson
with open("tindex_orig.geojson", "r") as f:
    geojson = json.load(f)

# only keep latest tiles from overlapping tiles
latest_tiles = {}
for feature in geojson.get("features", []):
    props = feature.get("properties", {})
    tile_id = props.get("tile_id")
    aktualitaet_str = props.get("Aktualitaet")

    if not tile_id or not aktualitaet_str:
        continue

    try:
        aktualitaet = datetime.strptime(aktualitaet_str[:10], "%Y-%m-%d")
    except ValueError as e:
        print(f"An error while parsing date string: {e}")
        continue

    # compare and possibly replace
    if tile_id not in latest_tiles or aktualitaet > latest_tiles[tile_id][0]:
        latest_tiles[tile_id] = (aktualitaet, feature)

filtered_features = [entry[1] for entry in latest_tiles.values()]

for feature in filtered_features:
    properties = feature.get("properties", {})

    # rename
    for old, new in rename.items():
        if old in properties:
            properties[new] = properties.pop(old)

    # remove keys except defined ones
    delete_keys = set(properties.keys()) - set(keep)
    for key in delete_keys:
        del properties[key]

# update features
geojson["features"] = filtered_features

# write updated geojson
with open("tindex.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

# create GPKG from GeoJson
tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
stream.read()

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
if os.path.isfile("tindex_orig.geojson"):
    os.remove("tindex_orig.geojson")
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile(tindex_gpkg):
    os.remove(tindex_gpkg)
