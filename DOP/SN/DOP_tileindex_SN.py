############################################################################
#
# MODULE:       DOP_tileindex_SN
#
# AUTHOR(S):    Johannes Halbauer
#
# PURPOSE:      Creates a DOP tile index for Sachsen based on the file names
#               of DOPs from https://www.geodaten.sachsen.de/index.html
#
# Data source:  https://www.geodaten.sachsen.de/batch-download-4719.html
#
# COPYRIGHT:    (C) 2024 by mundialis GmbH & Co. KG
#
# REQUIREMENTS: selenium, pyperclip, gdal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#############################################################################

import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

# DOP URL
DOP_URL = "https://www.geodaten.sachsen.de/batch-download-4719.html"

os.chdir("DOP/SN/")

# initalize firefox webdriver in headless mode
options = webdriver.FirefoxOptions()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)
driver.get(DOP_URL)

print(f"Extracting DOP URLs from {DOP_URL}...")

# wait til drop down menu is visible
wait = WebDriverWait(driver, 10)

# scroll to first drop down menu (landkreis)
dropdown_landkreis_element = wait.until(
    EC.visibility_of_element_located((By.ID, "select_municipality"))
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);", dropdown_landkreis_element
)

# select option by index ("Alle (Freistaat Sachsen)")
dropdown_landkreis = Select(dropdown_landkreis_element)
dropdown_landkreis.select_by_index(1)

# scroll to second drop down menu (product)
dropdown_product_element = wait.until(
    EC.visibility_of_element_located((By.ID, "select_product"))
)
driver.execute_script(
    "arguments[0].scrollIntoView(true);", dropdown_product_element
)

# select option by index ("Digitale Orthophotos 4-Kanal (RGBI) (DOP_RGBI)")
dropdown_product = Select(dropdown_product_element)
dropdown_product.select_by_index(10)

# select and click button to copy dop URLs to clipboard
button = wait.until(
    EC.element_to_be_clickable((By.ID, "button_downloads"))
)  # Button-ID korrekt angegeben
button.click()

# close webdriver
driver.close()

# write URLs from clipboard to list and remove empty line element
urls_list = pyperclip.paste().split("\n")
urls_list.remove("")

# create GeoJson dict
geojson_dict = {
    "type": "FeatureCollection",
    "name": "tindex",
    "crs": {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:EPSG::25833"},
    },
    "features": [],
}

print("Creating tileindex from DOP names...")
# loop through URLs and create tile from dop names
for num, dop in enumerate(urls_list):
    splitted_dop_name = os.path.basename(dop).split("_")
    x1 = int(splitted_dop_name[1][2:]) * 1000
    y1 = int(splitted_dop_name[2]) * 1000
    x2 = x1 + 2000
    y2 = y1 + 2000
    feat = {
        "type": "Feature",
        "properties": {"fid": num + 1, "location": dop},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]
            ],
        },
    }
    geojson_dict["features"].append(feat)

# write dict to JSON
with open("tindex.geojson", "w") as f:
    json.dump(geojson_dict, f, indent=4)

# create GPKG from GeoJson
stream = os.popen("ogr2ogr DOP20_tileindex_SN.gpkg tindex.geojson")
ogr2ogr_out = stream.read()

# verify
print("Verifying vector tile index:")
stream = os.popen("ogrinfo -so -al DOP20_tileindex_SN.gpkg")
tindex_verification = stream.read()
print(tindex_verification)

# package
if os.path.isfile("DOP20_tileindex_SN.gpkg.gz"):
    os.remove("DOP20_tileindex_SN.gpkg.gz")
stream = os.popen("gzip DOP20_tileindex_SN.gpkg")
create_gz = stream.read()
print("<DOP20_tileindex_SN.gpkg.gz> created.")

# cleanup
if os.path.isfile("tindex.geojson"):
    os.remove("tindex.geojson")
if os.path.isfile("openNRW_DOP10_tileindex.gpkg"):
    os.remove("openNRW_DOP10_tileindex.gpkg")
