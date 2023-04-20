
# AUTHOR:   Johannes Halbauer
# PURPOSE:  creating a DOP tile index for Brandenburg (and Berlin)
#
# All DOP download URLs stored in a .csv file are required. Each URL is
# stored in a new line without any seperator between the lines.
# Depending on the URLs length the indexing in line 33 and 34 should be adjusted.


# import required packages
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import csv


# define csv file with DOP URLs
csv_file = "/path/to/csv/file"

# define path for tileindex GeoPackage
geopackage = "/path/to/output/tileindex/geopackage"

# import csv of DOP URLs as list
URLs = open(csv_file).readlines()

# create lists for GeoDataframe
attr_url = []
polygons = []

print("Extracting coordinates of DOP tiles...")
for record in URLs[:4]:
    #extract coordinates of lower left corner (sw), write them to list
    east_sw = int(record[97:100]) * 1000
    north_sw = int(record[101:105]) * 1000
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

    # create list of polygon coordinates
    #polygon = [corner_sw, corner_se, corner_nw, corner_ne]

    # create shapely polygon object
    polygon = Polygon([corner_sw, corner_se, corner_ne, corner_nw])

    # write polygon object to list
    polygons.append(polygon)

    # write download URL to list for becoming an attribute of the tileindex
    attr_url.append(record)


print("Creating dataframe and write it to GeoPackage...")

# create dataframe including tile URL and corner coordinates
columns = ["coordinates", "URL"]
df = pd.DataFrame(list(zip(polygons, attr_url)), columns=columns, index=None)


# create GeoDataFrame out of DataFrame
gdf = gpd.GeoDataFrame(df, geometry="coordinates", crs="EPSG:25833")

# write GeoDataFrame to GeoPackage
gdf.to_file(geopackage, layer="geoportalBB_DOP20_tileindex", driver="GPKG")

print("Done!")
