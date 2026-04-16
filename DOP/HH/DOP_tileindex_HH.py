############################################################################
#
# MODULE:      DOP_tileindex_HH
# AUTHOR(S):   Johannes Halbauer, Leon Louwarts
# PURPOSE:     Creates a DOP tile index for Hamburg based on the file names
#              of DOPs from https://suche.transparenz.hamburg.de/dataset/
#              luftbilder-hamburg-dop-zeitreihe-unbelaubt3
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json
import time

from osgeo import gdal

# DOP URLs
DOP_URL = [
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Altona.zip",
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Bergedorf.zip",
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Eimsbuettel.zip",
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Hamburg-Mitte.zip",
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Hamburg-Nord.zip",
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Harburg.zip",
    "https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitale_orthophotos/DOP_unbelaubt/DOP2025_unbelaubt_Hamburg_Wandsbek.zip",
]

os.chdir("DOP/HH/")

# create list and fill with tif-paths
urls_list = []

for zip_url in DOP_URL:
    vsizip_url = f"/vsizip/vsicurl/{zip_url}"

    # find subfolder in zip
    root_entries = gdal.ReadDir(vsizip_url)
    if not root_entries:
        print(f"Warning: Could not read {zip_url}.")
        continue

    subfolder = next((e for e in root_entries if not e.startswith(".")), None)
    tif_dir = f"{vsizip_url}/{subfolder}"

    # read all tifs in subfolder
    tif_entries = gdal.ReadDir(tif_dir)
    if not tif_entries:
        print(f"Warning: No files in {tif_dir}.")
        continue

    for tif_name in tif_entries:
        if tif_name.lower().endswith(".tif"):
            urls_list.append((zip_url, subfolder, tif_name))


# create GeoJson dict
geojson_dict = {
    "type": "FeatureCollection",
    "name": "tindex",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:EPSG::25832"},
    },
    "features": [],
}

print("Creating tileindex from DOP names...")

temp_dict = dict()
num = -1
# loop through URLs and create tile from dop names
for zip_url, subfolder, tif_name in urls_list:
    splitted_dop_name = tif_name.split("_")
    # dop_file_name = (
    #     os.path.basename(dop).replace("_tiff.zip", ".tif")
    # )
    x1 = int(splitted_dop_name[2]) * 1000
    y1 = int(splitted_dop_name[3]) * 1000
    x2 = x1 + 1000
    y2 = y1 + 1000
    tile_num = f"tile_{x1}_{y1}"
    location = f"/vsizip/vsicurl/{zip_url}/{subfolder}/{tif_name}"
    if tile_num in temp_dict:
        feat_idx = temp_dict[tile_num]
        geojson_dict["features"][feat_idx]["properties"]["location"].append(
            location
        )
    else:
        num += 1
        temp_dict[tile_num] = num
        feat = {
            "type": "Feature",
            "properties": {
                "fid": num + 1,
                "tile_num": tile_num,
                "location": [location],
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]
                ],
            },
        }
        geojson_dict["features"].append(feat)

# change location from list to string
for feat in geojson_dict["features"]:
    loc = feat["properties"]["location"]
    if isinstance(loc, list):
        feat["properties"]["location"] = ",".join(loc)

# write dict to JSON
with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr DOP20_tileindex_HH.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al DOP20_tileindex_HH.gpkg")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile("DOP20_tileindex_HH.gpkg.gz"):
    os.remove("DOP20_tileindex_HH.gpkg.gz")
stream = os.popen("gzip DOP20_tileindex_HH.gpkg")
create_gz = stream.read()
print("<DOP20_tileindex_HH.gpkg.gz> created.")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("DOP20_tileindex_HH.gpkg"):
    os.remove("DOP20_tileindex_HH.gpkg")
