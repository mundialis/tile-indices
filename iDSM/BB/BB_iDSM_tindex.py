############################################################################
#
# MODULE:       BE_DSM_tindex.py
# AUTHOR(S):    Leon Louwarts
# PURPOSE:      Create tile index of Brandenburg iDSM tif files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
############################################################################


import os
import re
import json

import urllib.request

# Parameters for Brandenburg iDSM files
URL = "https://data.geobasis-bb.de/geobasis/daten/bdom/tif/"
VSI_PART = "/vsizip/vsicurl/"
TILE_SIZE = 1000
EPSG_CODE = 25833
OUTPUT_FILE = "BB_tileindex_dom_tif_proj.gpkg.gz"
os.chdir("iDSM/BB/")

html = urllib.request.urlopen(URL, timeout=60).read().decode()
names = sorted(set(re.findall(r'bdom_(\d{5})-(\d{4})\.zip', html)))
if not names:
    raise SystemExit("No tiles found - check URL")
print(f"{len(names)} tiles found")


def create_tindex_by_filename(names):
    # Create geojson
    geojson = {
            "type": "FeatureCollection",
            "name": "tindex",
            "crs": {
                "type": "name",
                "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG_CODE}"},
            },
            "features": []
        }

    for num, (x, y) in enumerate(names):
        x1 = int(x) * 1000
        y1 = int(y) * 1000
        x2 = x1 + TILE_SIZE
        y2 = y1 + TILE_SIZE
        feat = {
            "type": "Feature", "properties": {
                "fid": num + 1,
                "location": f"{VSI_PART}{URL}bdom_{x}-{y}.zip",
            },
            "geometry": {
                "type": "Polygon", "coordinates": [[
                    [x1, y1],
                    [x2, y1],
                    [x2, y2],
                    [x1, y2],
                    [x1, y1]
                ]],
            }
        }
        geojson["features"].append(feat)

    with open("tindex.geojson", "w") as f:
                json.dump(geojson, f)

    # Create gpkg from geojson
    tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg


tindex_gpkg = create_tindex_by_filename(names)

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
