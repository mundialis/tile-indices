############################################################################
#
# MODULE:       NI_DTM_tindex.py
# AUTHOR(S):    Johannes Halbauer
# PURPOSE:      Download and modify tile index of Niedersachsen DTM files from
#               https://ni-lgln-opengeodata.hub.arcgis.com/
# SPDX-FileCopyrightText: (c) 2025 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
############################################################################
# Usage:
# Then call script like this:
#   python3 DTM/NI/NI_DTM_tindex.py
# Output:
#   DTM/NI/NI_DTM_tindex_proj.gpkg.gz


import os
import json
import wget


# parameters
URL = (
    "https://arcgis-geojson.s3.eu-de.cloud-object-storage.appdomain.cloud/"
    "dgm1/lgln-opengeodata-dgm1.geojson"
)
OUTPUT_FILE = "NI_DTM_tindex_proj.gpkg.gz"
os.chdir("DTM/NI/")

# download tileindex
wget.download(URL, "tindex_orig.geojson", bar=None)

# define geojson keys to rename
rename = {"dgm1": "location"}

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
