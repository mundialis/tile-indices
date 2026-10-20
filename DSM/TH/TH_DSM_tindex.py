############################################################################
#
# MODULE:      TH_DSM_tindex
# AUTHOR(S):   Kim Kaiser, Leon Louwarts
# PURPOSE:     Creates a tile index of Thüringen DSM files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import re
import json
import subprocess
from collections import Counter

import xml.etree.ElementTree as ET


# Parameter for TH gtiff files
SERVICE_URL = (
    "https://geoportal.geoportal-th.de/dienste/"
    "atom_th_hoehendaten_dom?type=service&id=597871e8-45ef-4436-b747-ddba363251e8"
)
EPSG_CODE = 25832
TILE_SIZE = 1000
NS = {"atom": "http://www.w3.org/2005/Atom"}
# e.g. dom1_32_561_5609_1_th_2020-2025.zip  (older years without "32", e.g. dom1_561_5609_1_th_2014-2019.zip)
TILE_RE = re.compile(r"dom\d_(?:32_)?(\d+)_(\d+)_\d+_th_(\d{4})-(\d{4})\.zip$")


def fetch_xml(url, path):
    subprocess.run(["curl", "-sSL", url, "-o", path], check=True)
    return ET.parse(path).getroot()


def get_tile_urls(root_service):
    """Gets URLs of dataset feed"""
    ds_urls= [
        link.attrib["href"]
        for link in root_service.findall("atom:entry/atom:link", NS)
        if link.attrib.get("rel") == "alternate"
    ]
    return ds_urls


def parse_dataset_feed(root):
    """Choose newest year for each tile"""
    newest = {}
    for link in root.findall("atom:entry/atom:link", NS):
        href = link.attrib.get("href", "")
        m = TILE_RE.search(href)
        if not m:
            continue
        x, y = int(m.group(1)), int(m.group(2))
        years = (int(m.group(3)), int(m.group(4)))
        # tuple comparison: (2020, 2025) > (2014, 2019)
        if (x, y) not in newest or years > newest[(x, y)][0]:
            newest[(x, y)] = (years, href)
    return newest


def create_tindex_by_filename(newest):

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
    for num, ((x, y), (years, file_url)) in enumerate(sorted(newest.items())):
        x1 = x * 1000
        y1 = y * 1000
        x2 = x1 + TILE_SIZE
        y2 = y1 + TILE_SIZE
        geojson_dict["features"].append({
            "type": "Feature",
            "properties": {
                "fid": num + 1,
                "location": file_url,
                "year_from": years[0],
                "year_to": years[1],
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
        })

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f)


def main():
    os.chdir("DSM/TH/")
    tmp_service = "/tmp/th_dgm_service.xml"
    tmp_dataset = "/tmp/th_dgm_dataset.xml"

    ds_urls = get_tile_urls(fetch_xml(SERVICE_URL, tmp_service))
    if not ds_urls:
        raise RuntimeError("Not dataset service found in service feed")
    # Data feed currently provides data for 2010-2013, 2014-2019 and 2020-2025.
    # For each tile the newest DSM is selected
    newest = parse_dataset_feed(fetch_xml(ds_urls[0], tmp_dataset))
    if not newest:
        raise RuntimeError("No tiles found - check regex/feed structure")
    print(f"{len(newest)} tiles found")
    for years, count in sorted(Counter(v[0] for v in newest.values()).items()):
        print(f"  {years[0]}-{years[1]}: {count} Kacheln")

    create_tindex_by_filename(newest)

    tindex_gpkg = "th_dsm_tindex_proj.gpkg"
    if os.path.isfile(tindex_gpkg):
        os.remove(tindex_gpkg)
    subprocess.run(
        ["ogr2ogr", "-f", "GPKG", "-a_srs", f"EPSG:{EPSG_CODE}",
         "-nln", "tindex", tindex_gpkg, "tindex.geojson"],
        check=True,
    )

    print("Verifying vector tile index.")
    print(subprocess.run(["ogrinfo", "-so", "-al", tindex_gpkg],
                         capture_output=True, text=True, check=True).stdout)

    # Package
    output_file = f"{tindex_gpkg}.gz"
    if os.path.isfile(output_file):
        os.remove(output_file)
    subprocess.run(["gzip", tindex_gpkg], check=True)
    print(f"<{output_file}> created")

    # Cleanup: remove temp/intermediate files, only .gpkg.gz is kept
    for f in ("tindex.geojson", tindex_gpkg, tmp_service, tmp_dataset):
        if os.path.isfile(f):
            os.remove(f)

if __name__ == "__main__":
    main()
