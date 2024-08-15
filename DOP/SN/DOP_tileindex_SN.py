############################################################################
#
# MODULE:       DOP_tileindex_SN
#
# AUTHOR(S):    Johannes Halbauer
#
# PURPOSE:      Creates a DOP tile index for Sachsen based on the file names
#               of DOPs from https://www.geodaten.sachsen.de/index.html
#               stored in a .csv file.
#               
# Data source:  https://www.geodaten.sachsen.de/batch-download-4719.html
#
# COPYRIGHT:    (C) 2023 by mundialis GmbH & Co. KG
#
# REQUIREMENTS: pandas, geopandas, shapely
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


import gzip
import os
import shutil
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

#os.chdir("DOP/SN/")

# define csv file with DOP URLs
csv_file = "SN_DOP20_URLs.csv"

# define path for tileindex GeoPackage
geopackage = "DOP20_tileindex_SN.gpkg"
geopackage_compr = f"{geopackage}.gz"

# import csv of DOP URLs as list
URLs = open(csv_file).readlines()

# create lists for GeoDataframe
attr_url = []
polygons = []

print("Extracting coordinates of DOP tiles...")

for record in URLs:
    #extract coordinates of lower left corner (sw), write them to list
    east_sw = (int(record[113:117]) * 1000)
    north_sw = (int(record[107:112]) * 1000)
    corner_sw = (east_sw, north_sw)

    # calculate coordinates for remaining corners (DOP = 2000 x 2000 m)
    # lower right corner (se)
    east_se = east_sw + 2000
    north_se = north_sw
    corner_se = (east_se, north_se)

    # upper left corner (nw)
    east_nw = east_sw
    north_nw = north_se + 2000
    corner_nw = (east_nw, north_nw)

    # upper right corner (ne)
    east_ne = east_sw + 2000
    north_ne = north_sw + 2000
    corner_ne = (east_ne, north_ne)

    # create shapely polygon object
    polygon = Polygon([corner_sw, corner_se, corner_ne, corner_nw])

    # write polygon object to list
    polygons.append(polygon)

    # write download URL to list for becoming an attribute of the tileindex
    attr_url.append(record)

print("Creating dataframe and write it to GeoPackage...")

# create dataframe including tile URL and corner coordinates
columns = ["coordinates", "location"]
df = pd.DataFrame(list(zip(polygons, attr_url)), columns=columns, index=None)

# create GeoDataFrame out of DataFrame
gdf = gpd.GeoDataFrame(df, geometry="coordinates", crs="EPSG:25833")

# write GeoDataFrame to GeoPackage
gdf.to_file(geopackage, layer="geoportalSN_DOP20_tileindex", driver="GPKG")

# compress GeoPackage
if os.path.isfile(geopackage_compr):
    os.remove(geopackage_compr)
with open(geopackage, "rb") as f_in:
    with gzip.open(geopackage_compr, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

# cleanup
if os.path.isfile(geopackage):
    os.remove(geopackage)

print("<DOP20_tileindex_SN.gpkg.gz> created")