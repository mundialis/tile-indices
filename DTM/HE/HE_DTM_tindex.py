############################################################################
#
# NAME:         HE_DTM_tindex.py
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of Hessen DTM (German DGM) files
#
# Data source:  https://gds.hessen.de/downloadcenter
#
# COPYRIGHT:    (C) 2024 by Anika Weinmann, mundialis
#
# REQUIREMENTS: pip3 install requests remotezip
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

# Usage inside grass location:
#   grass -c epsg:25832 /grassdb/HE_ALKIS --exec python3 DTM/HE/HE_DTM_tindex.py
# Output:
#   DTM/HE/HE_DTM_tileindex.gpkg.gz

import json
import os
import shutil

from datetime import datetime
from time import sleep
from io import BytesIO
import ssl
from urllib.request import urlopen, HTTPError
from urllib.error import URLError
from zipfile import ZipFile

import grass.script as grass

from remotezip import RemoteZip
from requests.utils import requote_uri


"""CONSTANT VARIABLES"""

FS = "Hessen"
# Base url for Hessen DTM data
BASE_URL = (
    "https://gds.hessen.de/downloadcenter/DATE/"
    "3D-Daten/Digitales Geländemodell (DGM1)"
)
# get Kreise and Gemeinden of Hessen
URL_GERMANY_DATA = (
    "https://daten.gdz.bkg.bund.de/produkte/vg/vg5000_0101/aktuell/"
    "vg5000_01-01.utm32s.shape.ebenen.zip"
)

"""FUNCTIONS"""


def download_and_unzip(url, extract_to='.'):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        http_response = urlopen(url)
    except URLError as e:
        grass.fatal(_(f"Download error for {url}: {e}"))
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


def check_url(url):
    """Function to check if url is reachable"""
    url_today = url.replace("DATE", date)
    test_url = 400
    tries = 0
    while tries < 15 and test_url == 400:
        try:
            test_url = urlopen(url_today, timeout=600).getcode()
        except HTTPError as e:
            # HTTPError means 404
            tries = 100
            pass
        except URLError as e:
            if tries == 14:
                grass.message("URLError !!!")
                grass.message(url_today)
                grass.fatal(e)
            grass.message("RETRYING: " + url_today)
            tries += 1
            sleep(15)
            pass
        except Exception as e:
            if tries == 14:
                grass.message("Exception !!!")
                grass.message(url_today)
                grass.fatal(e)
                pass
            grass.message("RETRYING: " + url_today)
            tries += 1
            sleep(15)
    if test_url == 200:
        return True
    else:
        grass.message(_(f"{url_today} is not reachable."))
        return False


def create_urls(type, krs, gem):
    """Create possible urls for KRS data"""
    gem_vars = generate_gem_var(gem)
    type_vars = [type]
    if type == "Kreisfreie Stadt":
        type_vars.append("Stadt")
    urls = []
    for type_var in type_vars:
        for gem_var in gem_vars:
            urls.extend(
                [
                    requote_uri(f"{BASE_URL}/{type_var} {krs}/{gem_var} - DGM1.zip"),
                    requote_uri(f"{BASE_URL}/{type_var} {krs.split(' ')[0]}/{gem_var} - DGM1.zip"),
                    requote_uri(f"{BASE_URL}/{krs}/{gem_var} - DGM1.zip"),
                    requote_uri(f"{BASE_URL}/{krs}/{gem_var.split(' ')[0]} - DGM1.zip"),
                ]
            )
    return urls


def generate_gem_var(gem):
    """Generate a list with variants of the gem because of abbreviations"""
    gem_vars = [gem]
    if "v.d." in gem:
        gem_vars.append(gem.replace("v.d.", " v. d. ").replace("  ", " "))
        gem_vars.append(gem.replace("v.d.", " von der ").replace("  ", " "))
        gem_vars.append(gem.replace("v.d.", " vor der ").replace("  ", " "))
    if "i.Odw." in gem:
        gem_vars.append(gem.replace("i.Odw.", "im Odenwald"))
        gem_vars.append(gem.replace("i.Odw.", "i. Odw"))
    if "a.d." in gem:
        gem_vars.append(gem.replace("a.d.", " a. d. ").replace("  ", " "))
        gem_vars.append(gem.replace("a.d.", " a.d. ").replace("  ", " "))
        gem_vars.append(gem.replace("a.d.", " an der ").replace("  ", " "))
    if "a." in gem:
        gem_vars.append(gem.replace("a.", " a. ").replace("  ", " "))
        gem_vars.append(gem.replace("a.", " am ").replace("  ", " "))
    if gem in ["Michelbuch"]:
        gem_vars.append(f"Gemarkung {gem} (gemeindefrei)")
    if gem == "Erbach":
        gem_vars.append("Erbach (Odenwald)")
    if gem == "Neukirchen":
        gem_vars.append("Neukirchen (Knüllgebirge)")
    if gem in ["Lorch"]:
        gem_vars.append(f"{gem} am Rhein")
    return gem_vars


"""MAIN PART"""

os.chdir("/src/tile-indices/DTM/HE/")
# os.chdir("DTM/HE/")

if not os.path.isdir("tmp"):
    os.makedirs("tmp")

"""GET PARTS OF HESSEN (KREISE + GEMEINDEN)"""

# downloading germany boundaries
download_and_unzip(URL_GERMANY_DATA, "tmp")

# importing Hessen
file_path = os.path.join(
    "tmp",
    "vg5000_01-01.utm32s.shape.ebenen",
    "vg5000_ebenen_0101",
)
grass.run_command(
    "v.in.ogr",
    input=os.path.join(file_path, "VG5000_LAN.shp"),
    output="lan",
    where=f"GEN='{FS}'",
    quiet=True,
    overwrite=True,
)
grass.run_command("g.region", vector="lan", flags="p")

# importing Gemeinden and Kreise of Hessen
grass.run_command(
    "v.in.ogr",
    input=os.path.join(file_path, "VG5000_KRS.shp"),
    output="krs",
    flags="r",
    quiet=True,
    overwrite=True,
)
grass.run_command(
    "v.in.ogr",
    input=os.path.join(file_path, "VG5000_GEM.shp"),
    output="gem",
    flags="r",
    quiet=True,
    overwrite=True,
)

# overlay of GEM and KRS
overlay_tmp = f"{FS}_DTM_tmp"
overlay = f"{FS}_DTM"
grass.run_command(
    "v.overlay",
    ainput="krs",
    binput="gem",
    output=overlay_tmp,
    operator="and",
    quiet=True,
    overwrite=True,
)
grass.run_command(
    "v.clip",
    input=overlay_tmp,
    output=overlay,
    clip="lan",
    quiet=True,
    overwrite=True,
)
vals = grass.vector_db_select(overlay, columns="a_BEZ,a_GEN,b_GEN")["values"]
# cleanup columns of overlay
columns = grass.vector_db_select(overlay)["columns"]
columns.remove("cat")
grass.run_command("v.db.dropcolumn", map=overlay, columns=columns)
grass.run_command("v.db.addcolumn", map=overlay, columns="location TEXT")

"""CREATE DICT WITH TILES FOR"""

# create GeoJson
geojson_dict = {
  "type": "FeatureCollection",
  "name": "tindex",
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::25832"}},
  "features": []
}

# find urls for each gem
date = datetime.now().strftime("%Y%m%d")
ALKIS_urls = {}
krs_gem = {}
krs_base_urls = {}
num_HE_gem = len(vals)
i = 0
count = 0
for cat, val in vals.items():
    i += 1
    if i % 10 == 0:
        grass.message(_(f"{i}/{num_HE_gem} ..."))
    krs_type = val[0]
    krs = val[1]
    gem = val[2]

    # create url for krs and gem
    print(type, krs, gem)
    poss_krs_urls = create_urls(krs_type, krs, gem)

    url = None
    for poss_krs_url in set(poss_krs_urls):
        if check_url(poss_krs_url):
            zip = RemoteZip(poss_krs_url.replace("DATE", date), timeout=600)
            zip_files = [zip_info.filename for zip_info in zip.infolist() if zip_info.filename.endswith(".tif")]
            for zip_file in zip_files:
                url = f"/vsizip/vsicurl/{poss_krs_url}/{zip_file}"
                splitted_file_name = zip_file.split("_")
                x1 = int(splitted_file_name[2]) * 1000
                y1 = int(splitted_file_name[3]) * 1000
                x2 = x1 + 1000
                y2 = y1 + 1000
                feat = {
                    "type": "Feature", "properties": {
                        "fid": count + 1,
                        "location": url
                    },
                    "geometry": {
                        "type": "Polygon", "coordinates": [[[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]]
                    }
                }
                geojson_dict["features"].append(feat)
                count += 1
    if url is None:
        grass.fatal(f"No url found for {krs_type, krs, gem}!")

"""CREATE TILE INDEX AS .gpkg.gz FILE"""

# create GeoJson tile index
geojson_name = "tindex.geojson"
with open(geojson_name, "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
gpkg_name = "HE_DTM_tindex.gpkg"
stream = os.popen(f"ogr2ogr {gpkg_name} {geojson_name}")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen(f"ogrinfo -so -al {gpkg_name}")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile(f"{gpkg_name}.gz"):
    os.remove(f"{gpkg_name}.gz")
stream = os.popen(f"gzip {gpkg_name}")
create_gz = stream.read()
print(f"<{gpkg_name}.gz> created")

# cleanup
if os.path.isdir("tmp"):
    shutil.rmtree("tmp")
if os.path.isfile(geojson_name):
    os.remove(geojson_name)
if os.path.isfile(gpkg_name):
    os.remove(gpkg_name)
