#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      DOP_tileindex_HH
# AUTHOR(S):   Johannes Halbauer
#
# PURPOSE:     Creats a bDSM tile index for Hamburg based on the filenames of bDSMs stored as XYZ files in a directoy
#              downloaded from https://daten-hamburg.de/geographie_geologie_geobasisdaten/digitales_hoehenmodell_bdom/DOM1_XYZ_HH_2020_04_30.zip.
# COPYRIGHT:   (C) 2024 by mundialis GmbH & Co. KG
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

# import required packages
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

# define path to downloaded directory
files_dir = "/path/to/downloaded/directory"

# define path for output tileindex geopackage
geopackage = "/path/to/output/tileindex/geopackage.gpkg"

# create lists for GeoDataframe
attr_url = []
polygons = []

# extract filenames of downloaded directory
file_names = os.listdir(files_dir)

print("Extracting coordinates of nDSM tiles...")
for record in file_names:
    # extract coordinates of lower left corner (sw)
    east_sw = int(record[8:11]) * 1000 - 0.5
    north_sw = int(record[12:16]) * 1000 - 0.5
    corner_sw = (east_sw, north_sw)

    # calculate coordinates of remaining corner based on tile size of 1000 x 1000 m
    # lower right corner (se)
    east_se = east_sw + 1000
    north_se = north_sw
    corner_se = (east_se, north_se)

    # upper left corner (nw)
    east_nw = east_sw
    north_nw = north_se + 1000
    corner_nw = (east_nw, north_nw)

    # upper right corner (ne)
    east_ne = east_sw + 1000
    north_ne = north_sw + 1000
    corner_ne = (east_ne, north_ne)

    # create shapely polygon object
    polygon = Polygon([corner_sw, corner_se, corner_ne, corner_nw])

    # write polygon object to list
    polygons.append(polygon)

    # write download URL to list for becoming an attribute of the tileindex
    attr_url.append(record)

print("Creating dataframe and write it to GeoPackage...")

# create dataframe including tiles filenames and corner coordinates
columns = ["coordinates", "location"]
df = pd.DataFrame(list(zip(polygons, attr_url)), columns=columns, index=None)


# create GeoDataFrame out of DataFrame
gdf = gpd.GeoDataFrame(df, geometry="coordinates", crs="EPSG:25832")

# write GeoDataFrame to GeoPackage
gdf.to_file(geopackage, layer="geoportalHH_nDSM_tileindex", driver="GPKG")

print("Done!")
