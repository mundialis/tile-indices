############################################################################
#
# MODULE:      MV_iDSM_tindex
# AUTHOR(S):   Kim Kaiser
# PURPOSE:     Creates a tile index of Mecklenburg-Vorpommern iDSM files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json

from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET


# Parameter for MV gtiff files
URL = (
    "https://www.geodaten-mv.de/dienste/"
    "bdom20_atom?type=dataset&id=fafe490e-f9ff-4738-ac2a-7cb190cda49b"
)
EPSG_CODE = 25833
TILE_SIZE = 2000
OUTPUT_FILE = []
os.chdir("iDSM/MV/")


def create_tindex_by_filename(data_list):

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

    # get coordinates from filename
    for num, file_url in enumerate(data_list):
        filename = os.path.splitext(
            parse_qs(urlparse(file_url).query)["file"][0]
        )[0]
        splitted_data_name = filename.split("_")
        x1 = int(splitted_data_name[2]) * 1000
        y1 = int(splitted_data_name[3]) * 1000
        x2 = x1 + TILE_SIZE
        y2 = y1 + TILE_SIZE
        feat = {
            "type": "Feature",
            "properties": {
                "fid": num + 1,
                "location": file_url,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [x1, y1],
                    [x2, y1],
                    [x2, y2],
                    [x1, y2],
                    [x1, y1]
                ]],
            },
        }
        geojson_dict["features"].append(feat)

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f, indent=4)

    # create GPKG from GeoJson
    tindex_gpkg = "mv_idsm_tindex_proj.gpkg"
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg


# get xml from URL
tmp_xml = "/tmp/mv_dgm_tindex.xml"
os.system(f'curl -L "{URL}" -o "{tmp_xml}"')

# create tile index list with file URLs
tree = ET.parse(tmp_xml)
root = tree.getroot()
ns = {"atom": "http://www.w3.org/2005/Atom"}
data_list = [
    link.attrib["href"]
    for link in root.findall(".//atom:link", ns)
    if "laz" in link.attrib.get("href", "")
]

# create tindex
tindex_gpkg = create_tindex_by_filename(data_list)

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
if os.path.isfile(tmp_xml):
    os.remove(tmp_xml)
