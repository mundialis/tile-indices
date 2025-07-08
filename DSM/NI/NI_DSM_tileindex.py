############################################################################
#
# NAME:         NI_DSM_tindex.py
#
# AUTHOR(S):    Johannes Halbauer
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Download and modify tile index of Niedersachsen DSM files
#
# Data source:  https://daten-hamburg.de/geographie_geologie_geobasisdaten/
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
#   python3 DSM/NI/NI_DSM_tindex.py
# Output:
#   DSM/NI/NI_DSM_tindex_proj.gpkg.gz


import os
import json
import wget


# parameters
URL = (
    "https://arcgis-geojson.s3.eu-de.cloud-object-storage.appdomain.cloud/"
    "dom1/lgln-opengeodata-dom1.geojson"
)
OUTPUT_FILE = "NI_DSM_tindex_proj.gpkg.gz"
os.chdir("DSM/NI/")

# download tileindex
wget.download(URL, "tindex_orig.geojson", bar=None)

# define geojson keys to rename
rename = {"dom1": "location"}

# define geojson keys to keep
keep = ["location"]

# read geojson
with open("tindex_orig.geojson", "r") as f:
    geojson = json.load(f)

for feature in geojson.get("features", []):
    properties = feature.get("properties", {})

    # rename
    for old, new in rename.items():
        if old in properties:
            properties[new] = properties.pop(old)

    # remove keys except defined ones
    delete_keys = set(properties.keys()) - set(keep)
    for key in delete_keys:
        del properties[key]

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
