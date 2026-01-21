############################################################################
#
# MODULE:      DOP_tileindex_BE_BB
# AUTHOR(S):   Johannes Halbauer, Anika Weinmann
#
# PURPOSE:     Creates a DOP tile index for Brandenburg and Berlin based on the
#              file names of DOPs from hhttps://data.geobasis-bb.de/geobasis/
#              daten/dop/rgbi_tif/.
# SPDX-FileCopyrightText: (c) 2023-2025 by mundialis GmbH & Co. KG
# SPDX-License-Identifier: GPL-3.0-or-later.
#
#############################################################################


# import required packages
import os
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

URL = "https://data.geobasis-bb.de/geobasis/daten/dop/rgbi_tif/"
OUTPUT_FILE = "DOP20_tileindex_BE_BB.gpkg.gz"

# list of DOPs
GET_DOP_CMD = (
    f"lynx -dump -nonumbers -listonly {URL} | grep {URL} | grep 'dop_' | "
    "sed 's+^+/vsizip/vsicurl/+g'"
)
stream = os.popen(GET_DOP_CMD)
DOP_str = stream.read()
DOP_list = DOP_str.split()

# create lists for GeoDataframe
attr_url = []
polygons = []

print("Extracting coordinates of DOP tiles...")
for dop_url in DOP_list:

    dop_name = Path(dop_url).stem

    # extract coordinates of lower left corner (sw), write them to list
    x, y = dop_name.split("_")[-1].split("-")
    east_sw = (int(x) - 33000) * 1000
    north_sw = int(y) * 1000
    corner_sw = (east_sw, north_sw)

    # calculate coordinates for remaining corners (DOP = 1000 x 1000 m)
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
    attr_url.append(f"{dop_url}/{dop_name}.tif")


print("Creating dataframe and write it to GeoPackage...")

# create dataframe including tile URL and corner coordinates
columns = ["coordinates", "location"]
df = pd.DataFrame(list(zip(polygons, attr_url)), columns=columns, index=None)


# create GeoDataFrame out of DataFrame
gdf = gpd.GeoDataFrame(df, geometry="coordinates", crs="EPSG:25833")

# write GeoDataFrame to GeoPackage
tindex_gpkg = OUTPUT_FILE.rsplit(".", 1)[0]
gdf.to_file(tindex_gpkg, layer="geoportalBB_DOP20_tileindex", driver="GPKG")

# package
if Path(OUTPUT_FILE).is_file():
    Path(OUTPUT_FILE).unlink()
stream = os.popen(f"gzip {tindex_gpkg}")
stream.read()
print(f"<{OUTPUT_FILE}> created")

print("Done!")
