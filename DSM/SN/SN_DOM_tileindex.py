############################################################################
#
# NAME:         SN_DOM_tileindex.py
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of DOM tiff files
#
# Data source:  https://www.geodaten.sachsen.de/batch-download-4719.html
#
# COPYRIGHT:    (C) 2023 by Anika Weinmann, mundialis
#
# REQUIREMENTS: gdal, gzip
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
#   python3 DSM/SN/SN_DOM_tileindex.py
# Output:
#   DSM/SN/SN_DOM_tileindex_proj.gpkg.gz


from bs4 import BeautifulSoup
import requests as req
import json
import re
import os

SN_URL = "https://www.geodaten.sachsen.de/batch-download-4719.html"
DATA_TYPE = "DOM1_TIFF"
TILESIZE = 1000
TINDEX = "SN_DOM_tileindex_proj.gpkg.gz"

os.chdir("DSM/SN/")


def get_all_grid_ids(grid_ids):
    all_grid_ids = []
    for i in range(0, len(grid_ids), 2):
        id = grid_ids[i]
        num = grid_ids[i + 1]
        for n in range(num):
            grid_id = id + n
            all_grid_ids.append(grid_id)
    return all_grid_ids


# get HTML from SN_URL and extract js script
web = req.get(SN_URL)
html = BeautifulSoup(web.text, 'lxml')
js_scripts = html.find_all("script", type="text/javascript")
js_script = ""
for jss in js_scripts:
    if "function copyURLs" in str(jss):
        js_script = str(jss)

# extract vars from js script
## data url
data_base_url = "".join([x.strip() for x in js_script.split(
    "function createGeoCloudURL", 1
)[-1].split("}", 1)[0].split("return")[-1].split("+")]).replace(
    "(", ""
).replace(")", "").replace("'", "")
## product
batchConfig_products_str = "{" + re.findall(r"batchConfig.products={(.*?)}*\n", js_script)[0].strip()
batchConfig_products = json.loads(batchConfig_products_str)
products = batchConfig_products[DATA_TYPE]
product_id = products["share_id"]
filename_tpl = products["filename"]
# resolution = int(products["packagesize"])  / 1000.
existing_not_computed = get_all_grid_ids(products["existing_not_computed"])
computed_not_existing = get_all_grid_ids(products["computed_not_existing"])
## mapping
batchConfig_mapping_str = "{" + re.findall(r"batchConfig.mapping={(.*?)}*\n", js_script)[0].strip()
batchConfig_mapping = json.loads(batchConfig_mapping_str)

# create GeoJson
geojson_dict = {
  "type": "FeatureCollection",
  "name": "tindex",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25833"}},
  "features": []
}

# create tile urls
urls = []
fid = 0
for map in batchConfig_mapping.values():
    grid_id_list = map["grid_id"]
    for i in range(0, len(grid_id_list), 2):
        first_grid_id = grid_id_list[i]
        num = grid_id_list[i + 1]
        for n in range(num):
            grid_id = first_grid_id + n
            if (
                grid_id not in existing_not_computed
                and grid_id not in computed_not_existing
            ):
                rechtswert = str(grid_id)[:3]
                hochwert = str(grid_id)[3:]
                filename = filename_tpl.replace("$Rechtswert$", rechtswert).replace("$Hochwert$", hochwert)
                url = data_base_url.replace("productId", product_id).replace("filename", filename)
                vsi_url = f"/vsizip/vsicurl/{url}/{filename.replace('_tiff', '').replace('.zip', '.tif')}"
                if vsi_url not in urls:
                    urls.append(vsi_url)
                    fid += 1
                    x1 = int(rechtswert) * 1000
                    y1 = int(hochwert) * 1000
                    x2 = x1 + TILESIZE
                    y2 = y1 + TILESIZE
                    feat = {
                        "type": "Feature", "properties": {
                            "fid": fid,
                            "location": vsi_url
                        },
                        "geometry": {
                            "type": "Polygon", "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
                        }
                    }
                    geojson_dict["features"].append(feat)

print(f"Found {len(urls)} {DATA_TYPE} files.")

with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
gpkg_file = f"{TINDEX.split('.')[0]}.gpkg"
stream = os.popen(f"ogr2ogr {gpkg_file} tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen(f"ogrinfo -so -al {gpkg_file}")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile(TINDEX):
    os.remove(TINDEX)
stream = os.popen(f"gzip {gpkg_file}")
create_gz = stream.read()
print(f"<{TINDEX}> created")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile(gpkg_file):
    os.remove(gpkg_file)
