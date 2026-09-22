############################################################################
#
# MODULE:      ST_DOP_tindex
# AUTHOR(S):   Kim Kaiser, Leon Louwarts
# PURPOSE:     Creates a tile index of Sachsen-Anhalt DOP files
# SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG and the
#                             GRASS Development Team
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################

import os
import json
import requests
import re


# Parameter for ST gtiff files
EPSG_CODE = 25832
TILE_SIZE = 2000
os.chdir("DOP/ST/")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:155.0) Gecko/20100101 Firefox/155.0",
    "Accept-Language": "de,en-US;q=0.9,en;q=0.8",
})

BASE_URL = "https://www.lvermgeo.sachsen-anhalt.de/"
AUSWAHL_URL = BASE_URL + "de/gdp-dop20-auswahl.html"

# Session-Cookie holen (Startseite)
session.get(BASE_URL)

# Auswahlseite mit eingebettetem GeoJSON holen
resp = session.get(AUSWAHL_URL)
resp.raise_for_status()

match = re.search(r"mapdownloader_content',\s*'([^']*)'", resp.text)
if not match:
    raise RuntimeError("GeoJSON-Blob nicht gefunden - hat sich die Seitenstruktur geändert?")

tiles = json.loads(match.group(1))
print(f"{len(tiles['features'])} Kacheln gefunden, CRS: {tiles['crs']['properties']['name']}")


def download_tile(session, item_id, output_dir, fmt="zip"):
    prepare_url = (
        "https://www.lvermgeo.sachsen-anhalt.de/de/mod/4,1962,501/ajax/1/prepare/"
        f"?items={item_id}&format={fmt}"
    )
    resp = session.get(prepare_url, headers={"X-Requested-With": "XMLHttpRequest"})
    resp.raise_for_status()

    download_url = resp.text.strip()
    if not download_url.startswith("http"):
        raise RuntimeError(f"Unerwartete prepare-Antwort für Item {item_id}: {download_url}")

    dl_resp = session.get(download_url)
    dl_resp.raise_for_status()

    out_path = output_dir / f"dop20_{item_id}.zip"
    with open(out_path, "wb") as f:
        f.write(dl_resp.content)
    return out_path


def create_tindex_from_features(tiles):
    geojson_dict = {
        "type": "FeatureCollection",
        "name": "tindex",
        "crs": {
            "type": "name",
            "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG_CODE}"},
        },
        "features": [],
    }

    for num, feature in enumerate(tiles["features"]):
        item_id = feature["properties"]["id"]
        label = feature["properties"].get("label", "")
        feat = {
            "type": "Feature",
            "properties": {
                "fid": num + 1,
                "item_id": item_id,
                "label": label,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": feature["geometry"]["coordinates"],
            },
        }
        geojson_dict["features"].append(feat)

    with open("tindex.geojson", "w") as f:
        json.dump(geojson_dict, f, indent=4)

    tindex_gpkg = "st_dop_tindex_proj.gpkg"
    stream = os.popen(f"ogr2ogr {tindex_gpkg} tindex.geojson")
    stream.read()
    return tindex_gpkg


tindex_gpkg = create_tindex_from_features(tiles)

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
