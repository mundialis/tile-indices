############################################################################
#
# MODULE:      BW_DSM_tindex
# AUTHOR(S):   Kim Kaiser, Anika Weinmann
# PURPOSE:     Creates a tile index of Baden-Württemberg DSM files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json

from urllib.parse import urljoin


# Parameter for BW geotiff files
BASE_URL = "https://opengeodata.lgl-bw.de/"
TILE_URL = (
    "/tiles/vts/2x2Gitter/7/66/43.pbf",
    "/tiles/vts/2x2Gitter/7/66/44.pbf",
    "/tiles/vts/2x2Gitter/7/67/43.pbf",
    "/tiles/vts/2x2Gitter/7/67/44.pbf",
)
EPSG_CODE = 25832
TILE_SIZE = 2000
OUTPUT_FILE = []
os.chdir("DSM/BW/")


def create_tindex_by_filename(tmp_json):

    # fetch data from tmp_json
    with open("BW_DOM1.geojson", encoding="utf-8") as f:
        data = json.load(f)

    # create GeoJson
    geojson_dict = {
        "type": "FeatureCollection",
        "name": "tindex",
        "crs": {
            "type": "name",
            "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG_CODE}"},
        },
        "features": [],
    }

    num = 0

    for feature in data["features"]:
        products = feature["properties"]["metadata"]["products"]
        for product in products:
            for item in product.get("types", []):
                file_path = item.get("downloadURL", "")
                if "/dom1/" in file_path.lower():
                    filename = file_path.split("_")
                    x1 = int(filename[2]) * 1000
                    y1 = int(filename[3]) * 1000
                    x2 = x1 + TILE_SIZE
                    y2 = y1 + TILE_SIZE
                    file_url = urljoin(BASE_URL, file_path)
                    geojson_dict["features"].append(
                        {
                            "type": "Feature",
                            "properties": {
                                "fid": num + 1,
                                "location": file_url,
                            },
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [
                                    [
                                        [x1, y1],
                                        [x2, y1],
                                        [x2, y2],
                                        [x1, y2],
                                        [x1, y1],
                                    ]
                                ],
                            },
                        }
                    )
                    num += 1

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f, indent=4)

    # create GPKG from GeoJson
    tindex_gpkg = "BW_DSM_tindex_proj.gpkg"
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg

# create temporary GeoJson from PBF
for URL in TILE_URL:
    grid_url = urljoin(BASE_URL, URL)
    tmp_json = "BW_DOM1.geojson"
    os.system(f'ogr2ogr -append {tmp_json} {grid_url}')

# create tindex
tindex_gpkg = create_tindex_by_filename(tmp_json)

# verify
print("Verifying vector tile index:")
stream = os.popen(f"ogrinfo -so -al {tindex_gpkg}")
tindex_verification = stream.read()
print(tindex_verification)

# package
OUTPUT_FILE = f"{tindex_gpkg}.gz"
if os.path.isfile(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
stream = os.popen(f"gzip {tindex_gpkg}")
create_gz = stream.read()
print(f"<{OUTPUT_FILE}> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile(tindex_gpkg):
    os.remove(tindex_gpkg)
if os.path.isfile(tmp_json):
    os.remove(tmp_json)
