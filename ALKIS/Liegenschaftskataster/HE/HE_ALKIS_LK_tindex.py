############################################################################
#
# NAME:         HE_ALKIS_LK_tindex.py
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Create tile index of Hessen ALKIS Liegenschaftskataster files
#
# Data source:  https://gds.hessen.de/downloadcenter
#
# COPYRIGHT:    (C) 2023 by Anika Weinmann, mundialis
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
#   grass -c epsg:25832 /grassdb/HE_ALKIS --exec python3 ALKIS/Liegenschaftskataster/HE/HE_ALKIS_LK_tindex.py
# Output:
#   ALKIS/Liegenschaftskataster/HE/HE_ALKIS_LK_tileindex.gpkg.gz

import os
import shutil

from datetime import datetime
from io import BytesIO
import ssl
from urllib.request import urlopen, HTTPError
from urllib.error import URLError
from zipfile import ZipFile

import grass.script as grass

from remotezip import RemoteZip
from requests.utils import requote_uri


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
    try:
        test_url = urlopen(url_today).getcode()
    except HTTPError:
        pass
    except URLError:
        pass
    if test_url == 200:
        return True
    else:
        grass.message(_(f"{url_today} is not reachable."))
        return False


def create_urls(type, krs, gem):
    """Create possible urls for KRS data"""
    return [
        requote_uri(f"{BASE_URL}/{type} {krs}/{gem}.zip"),
        requote_uri(f"{BASE_URL}/{krs}/{gem}.zip"),
        requote_uri(f"{BASE_URL}/{type} {krs.split(' ')[0]}/{gem}.zip"),
        requote_uri(f"{BASE_URL}/{krs}/{gem.split(' ')[0]}.zip"),
    ]


def get_url(gem, zip_files, krs_url):
    """ Get url for gem"""
    url = None
    gem_vars = generate_gem_var(gem)
    file_gem = {
        zfile: gv for zfile in zip_files for gv in gem_vars if gv in zfile
    }
    if len(file_gem) > 1:
        for gem_f, gem in file_gem.items():
            if f"{gem}.zip" == gem_f:
                file_gem = [gem_f]
    if len(file_gem) == 1:
        url = requote_uri(f"{krs_url}{[fg for fg in file_gem][0]}")
        if not check_url(url):
            url = None
    else:
        grass.message(_(f"No url found for {gem}!"))
    return url


def generate_gem_var(gem):
    """Generate a list with variants of the gem because of abbreviations"""
    gem_vars = [gem]
    if "v.d." in gem:
        gem_vars.append(gem.replace("v.d.", " v. d. ").replace("  ", " "))
        gem_vars.append(gem.replace("v.d.", " von der ").replace("  ", " "))
        gem_vars.append(gem.replace("v.d.", " vor der ").replace("  ", " "))
    if "i.Odw." in gem:
        gem_vars.append(gem.replace("i.Odw.", "im Odenwald"))
    if "a.d." in gem:
        gem_vars.append(gem.replace("a.d.", " a. d. ").replace("  ", " "))
        gem_vars.append(gem.replace("a.d.", " an der ").replace("  ", " "))
    if "a." in gem:
        gem_vars.append(gem.replace("a.", " a. ").replace("  ", " "))
    return gem_vars


FS = "Hessen"
# Base url for Hessen ALKIS Liegenschaftskataster data
BASE_URL = (
    "https://gds.hessen.de/downloadcenter/DATE/Liegenschaftskataster/"
    "Bestandsdatenausgabe Grundriss (xml)"
)

os.chdir("/src/tile-indices/ALKIS/Liegenschaftskataster/HE/")

# get Kreise and Gemeinden of Hessen
URL_GERMANY_DATA = (
    "https://daten.gdz.bkg.bund.de/produkte/vg/vg5000_0101/aktuell/"
    "vg5000_01-01.utm32s.shape.ebenen.zip"
)

if not os.path.isdir("tmp"):
    os.makedirs("tmp")

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
)
grass.run_command("g.region", vector="lan", flags="p")

# importing Gemeinden and Kreise of Hessen
grass.run_command(
    "v.in.ogr",
    input=os.path.join(file_path, "VG5000_KRS.shp"),
    output="krs",
    flags="r",
    quiet=True,
)
grass.run_command(
    "v.in.ogr",
    input=os.path.join(file_path, "VG5000_GEM.shp"),
    output="gem",
    flags="r",
    quiet=True,
)

# overlay of GEM and KRS
overlay_tmp = f"{FS}_ALKIS_Liegenschaftskataster_tmp"
overlay = f"{FS}_ALKIS_Liegenschaftskataster"
grass.run_command(
    "v.overlay",
    ainput="krs",
    binput="gem",
    output=overlay_tmp,
    operator="and",
    quiet=True,
)
grass.run_command(
    "v.clip", input=overlay_tmp, output=overlay, clip="lan", quiet=True
)
vals = grass.vector_db_select(overlay, columns="a_BEZ,a_GEN,b_GEN")["values"]
# cleanup columns of overlay
columns = grass.vector_db_select(overlay)["columns"]
columns.remove("cat")
grass.run_command("v.db.dropcolumn", map=overlay, columns=columns)
grass.run_command("v.db.addcolumn", map=overlay, columns="location TEXT")
# find urls for each gem
date = datetime.now().strftime("%Y%m%d")
ALKIS_urls = {}
krs_gem = {}
krs_base_urls = {}
num_HE_gem = len(vals)
i = 0
for cat, val in vals.items():
    i += 1
    if i % 10 == 0:
        grass.message(_(f"{i}/{num_HE_gem} ..."))
    krs_type = val[0]
    krs = val[1]
    gem = val[2]
    if krs not in krs_gem:
        url = None
        krs_urls = [
            requote_uri(
                f"{BASE_URL}/{krs_type} {krs}/PKT_{krs_type} {krs}.zip"
            ),
            requote_uri(f"{BASE_URL}/{krs}/PKT_{krs}.zip"),
        ]
        if krs == "Offenbach am Main":
            krs_urls.append(requote_uri(
                f"{BASE_URL}/{krs_type} Offenbach/PKT_{krs_type} Offenbach.zip"
            ))
        for krs_url in krs_urls:
            if check_url(krs_url):
                zip = RemoteZip(krs_url.replace("DATE", date))
                zip_files = [zip_info.filename for zip_info in zip.infolist()]
                krs_gem[f"{krs_type}_{krs}"] = zip_files
                krs_base_url = krs_url.split('PKT')[0]
                krs_base_urls[f"{krs_type}_{krs}"] = krs_base_url
                url = get_url(gem, zip_files, krs_base_url)
    else:
        url = get_url(
            gem,
            krs_gem[f"{krs_type}_{krs}"],
            krs_base_urls[f"{krs_type}_{krs}"],
        )
    if not url:
        grass.message(_(f"Not found: {krs_type} {krs} - {gem}"))
    grass.run_command(
        "v.db.update",
        map=overlay,
        column="location",
        where=f"cat = {cat}",
        value=url,
        quiet=True,
    )

grass.message(_("Exporting tindex as <HE_ALKIS_LK_tindex.gpkg>"))
grass.run_command(
    "v.out.ogr",
    input=overlay,
    output="HE_ALKIS_LK_tindex.gpkg",
    overwrite=True,
)

# package
if os.path.isfile("HE_ALKIS_LK_tindex.gpkg.gz"):
    os.remove("HE_ALKIS_LK_tindex.gpkg.gz")
stream = os.popen("gzip HE_ALKIS_LK_tindex.gpkg")
create_gz = stream.read()
grass.message(_("<HE_ALKIS_LK_tindex.gpkg.gz> created"))

# cleanupy
if os.path.isfile("HE_ALKIS_LK_tindex.gpkg"):
    os.remove("HE_ALKIS_LK_tindex.gpkg")
if os.path.isdir("tmp"):
    shutil.rmtree("tmp")
grass.message(_("Tindex creating done"))
