#!/bin/sh

############################################################################
#
# NAME:        fetch_BE_DGM_list.sh
#
# AUTHOR(S):    Markus Neteler <neteler at mundialis.de>
#               Veronica Koess <koess at mundialis.de>
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      Fetch list of Berlin, Germany DGM (digital elevation model) xyz .zip  files
#
# Data source:  https://fbinter.stadt-berlin.de/
#
# COPYRIGHT:    (C) 2023 by Markus Neteler, mundialis
#
# REQUIREMENTS: lynx, gdal, gTILE, sed
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

# Usage:
#   sh fetch_BE_DGM_list.sh
# Output:
#   BE_DGM_tiles.csv.gz
########################################

# fail on error 
set -e 

lynx -dump -nonumbers -listonly "https://fbinter.stadt-berlin.de/fb/berlin/service_intern.jsp?id=a_dgm@senstadt&type=FEED" | grep https://fbinter.stadt-berlin.de/fb/atom/DGM1/DGM1_| sed 's+^+/vsizip/vsicurl/+g' > BE_DGM_tiles.csv

# generate download script
# cat BE_DGM_tiles.csv | sed 's+^+wget -c +g' > fetch_BE_DGM_tiles.sh

# compress ndom50 URLs list
gzip BE_DGM_tiles.csv
echo "Generated <BE_DGM_tiles.csv.gz>"

echo ""
echo "Single tile import: Import into GRASS GIS with, e.g.:
r.import input=/vsicurl/https://fbinter.stadt-berlin.de/fb/atom/DGM1/DGM1_368_5808.zip output=be_dgm1_368_5808"
echo ""
echo "For mosaics, better generate a VRT mosaic first (using <gdalbuildvrt ...>), then import the VRT file."
echo ""
echo "For a tile index, run
gdaltindex -f GPKG BE_DGM_tileindex.gpkg --optfile BE_DGM_tiles.csv"
