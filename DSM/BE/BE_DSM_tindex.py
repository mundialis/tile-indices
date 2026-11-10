############################################################################
#
# MODULE:       BE_DSM_tindex.py
# AUTHOR(S):    Anika Weinmann, Leon Louwarts
# PURPOSE:      Create tile index of Berlin DOM/DSM txt files
# SPDX-FileCopyrightText: (c) 2023-2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
############################################################################
# Usage:
# Set Parameter `GDALTINDEX`
# `GDALTINDEX=True`: using `gdaltindex` (more correct limits of the tiles)
# `GDALTINDEX=False`: creating the tiles out of the file names (only small
#                     improvement in runtime, because you still have to check
#                     with `gdalinfo` whether the tiles are valid files at all)
# Then call script like this:
#   python3 DSM/BE/BE_DSM_tindex.py
# Output:
#   DSM/BE/be_dom_tindex_proj.gpkg.gz


import os
import json

import urllib.request
import xml.etree.ElementTree as ET

from osgeo import gdal
from remotezip import RemoteZip


# Parameter for Berlin DOM txt files
URL = "https://gdi.berlin.de/data/dom/atom/0.atom"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
EPSG_CODE = 25833
FILE_EXTENSION = ".txt"
TILE_SIZE = 2000
OUTPUT_FILE = "be_dom_tindex_proj.gpkg.gz"
GDALTINDEX = False
VSI_PART = "/vsizip/vsicurl/"
os.chdir("DSM/BE/")


def create_tindex_by_filename(data_list):
    # create GeoJson
    geojson_dict = {
        "type": "FeatureCollection",
        "name": "tindex",
        "crs": {
            "type": "name",
            "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG_CODE}"},
        },
        "features": []
    }

    for num, data in enumerate(data_list):
        splitted_data_name = os.path.basename(
            data
        ).replace(FILE_EXTENSION, "").split("_")
        x1 = int(splitted_data_name[2]) * 1000
        y1 = int(splitted_data_name[3]) * 1000
        x2 = x1 + TILE_SIZE
        y2 = y1 + TILE_SIZE
        feat = {
            "type": "Feature", "properties": {
                "fid": num + 1,
                "location": data.split(".zip")[0] + ".zip",
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
        geojson_dict["features"].append(feat)

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f, indent=4)

    # create GPKG from GeoJson
    tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg


def create_tindex_by_gdaltindex(data_list):
    tiles_csv = "tiles.csv"
    tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
    with open(tiles_csv, "w") as f:
        for data in data_list:
            f.write(f"{data}\n")
    # create tile index
    tindex_cmd = (
        f"gdaltindex -f GPKG -t_srs EPSG:{EPSG_CODE} {tindex_gpkg} "
        f"--optfile {tiles_csv}"
    )
    stream = os.popen(tindex_cmd)
    stream.read()
    os.remove(tiles_csv)
    return tindex_gpkg


def inner_name(zip_url):
    # DOM1_372_5828.zip -> dom1_33_372_5828_2_be.txt
    base = os.path.basename(zip_url).replace(".zip", "")
    _, x, y = base.split("_")
    return f"dgm1_33_{x}_{y}_2_be{FILE_EXTENSION}"


# get tile URLs from the atom feed
with urllib.request.urlopen(URL, timeout=60) as response:
    root = ET.fromstring(response.read())

zip_urls = [
    link.attrib["href"]
    for link in root.findall(".//atom:link", ATOM_NS)
    if link.attrib.get("href", "").lower().endswith(".zip")
]
data_list = [f"{VSI_PART}{x}/{inner_name(x)}" for x in zip_urls]
if not data_list:
    raise SystemExit("Not tiles found - check URL/feed structure")
print(f"{len(data_list)} tiles found")

# create tindex
if GDALTINDEX:
    tindex_gpkg = create_tindex_by_gdaltindex(data_list)
else:
    tindex_gpkg = create_tindex_by_filename(data_list)

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
